import pandas as pd
import oracledb
from datetime import datetime

# connect to the Oracle database
dsn = oracledb.makedsn("localhost", 1521, sid="xe")
conn = oracledb.connect(user="system", password="PLACEHOLDER", dsn=dsn)
cursor = conn.cursor()

# get employee names
cursor.execute("SELECT employee_id, LOWER(first_name), LOWER(last_name) FROM employees")
name_to_id = {
    f"{fn.strip()} {ln.strip()}": eid
    for eid, fn, ln in cursor.fetchall()
}
employee_ids = list(name_to_id.values())

# load trainings
cursor.execute("""
    SELECT training_id, session_date,
           EXTRACT(HOUR FROM session_start_time)*3600 + EXTRACT(MINUTE FROM session_start_time)*60 + EXTRACT(SECOND FROM session_start_time),
           EXTRACT(HOUR FROM session_end_time)*3600 + EXTRACT(MINUTE FROM session_end_time)*60 + EXTRACT(SECOND FROM session_end_time)
    FROM trainings
""")
trainings = pd.DataFrame(cursor.fetchall(), columns=["training_id", "session_date", "start_sec", "end_sec"])
trainings["session_date"] = pd.to_datetime(trainings["session_date"]).dt.date

# load absences
cursor.execute("""
    SELECT employee_id, session_date,
           EXTRACT(HOUR FROM session_start_time)*3600 + EXTRACT(MINUTE FROM session_start_time)*60 + EXTRACT(SECOND FROM session_start_time),
           EXTRACT(HOUR FROM session_end_time)*3600 + EXTRACT(MINUTE FROM session_end_time)*60 + EXTRACT(SECOND FROM session_end_time)
    FROM absences
""")
absences = pd.DataFrame(cursor.fetchall(), columns=["employee_id", "session_date", "start_sec", "end_sec"])
absences["session_date"] = pd.to_datetime(absences["session_date"]).dt.date

# load the CSV files
attendance_files = {
    18: pd.read_csv("june_24th.csv", sep="\t", encoding="utf-16"),
    19: pd.read_csv("june_25th.csv", sep="\t", encoding="utf-16"),
    20: pd.read_csv("june_26th.csv", sep="\t", encoding="utf-16")
}

present_lookup = set()
for tid, df in attendance_files.items():
    for _, row in df.iterrows():
        name = row["Name"].strip().lower()
        emp_id = name_to_id.get(name)
        if emp_id:
            present_lookup.add((emp_id, tid))

# prepare the format
records = []
attendance_id = 1

for emp_id in employee_ids:
    for _, train in trainings.iterrows():
        tid = train["training_id"]
        validated = None

        # check if there is an absence during a training
        overlaps = absences[
            (absences["employee_id"] == emp_id) &
            (absences["session_date"] == train["session_date"])
        ]
        for _, ab in overlaps.iterrows():
            if max(ab["start_sec"], train["start_sec"]) < min(ab["end_sec"], train["end_sec"]):
                validated = 'N'
                break

        # check if we can validate the presence based on the attendance files
        if validated is None and (emp_id, tid) in present_lookup:
            validated = 'Y'

        # if neither confirmed nor denied, put a placeholder
        validated = validated if validated in ('Y', 'N') else '-'

        records.append((
            int(attendance_id),
            int(emp_id),
            int(tid),
            validated
        ))
        attendance_id += 1

# insert into the table
cursor.executemany("""
    INSERT INTO training_attendance (
        attendance_id, employee_id, training_id, validated
    ) VALUES (:1, :2, :3, :4)
""", records)

conn.commit()
cursor.close()
conn.close()

print("training_attendance table populated successfully.")