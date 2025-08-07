import pandas as pd
import oracledb
from datetime import datetime

# connect to the Oracle database
dsn = oracledb.makedsn("localhost", 1521, sid="xe")
conn = oracledb.connect(user="system", password="PLACEHOLDER", dsn=dsn)
cursor = conn.cursor()

# load the CSV file
df = pd.read_csv("adjusted_absences.csv")

# get employee_id based on name
def get_employee_id(full_name):
    parts = full_name.strip().split(" ", 1)
    first = parts[0]
    last = parts[1] if len(parts) > 1 else ""
    cursor.execute("""
        SELECT employee_id FROM employees
        WHERE LOWER(first_name) = :first AND LOWER(last_name) = :last
    """, {"first": first.lower(), "last": last.lower()})
    result = cursor.fetchone()
    return result[0] if result else None

# prepare the format
records = []
for i, row in df.iterrows():
    emp_name = row["Employee"]
    employee_id = get_employee_id(emp_name)
    if not employee_id:
        print(f"Skipping row {i}: Employee not found -> {emp_name}")
        continue

    try:
        date_str = row["Start Date"]
        session_date = datetime.strptime(date_str, "%m/%d/%Y").date()

        start_time = datetime.strptime(row["Start Time"], "%I:%M:%S %p").time()
        end_time = datetime.strptime(row["End Time"], "%I:%M:%S %p").time()

        start_interval = f"+00 {start_time.strftime('%H:%M:%S')}"
        end_interval = f"+00 {end_time.strftime('%H:%M:%S')}"

        all_day_flag = 'Y' if row["All day event"] else 'N'
        info = row.get("Information", None)

        records.append((
            i + 1, employee_id, info, session_date,
            start_interval, end_interval, all_day_flag
        ))
    except Exception as e:
        print(f"Skipping row {i} due to error: {e}")

# insert into the table
cursor.executemany("""
    INSERT INTO absences (
        absence_id, employee_id, information, session_date,
        session_start_time, session_end_time, all_day_event
    )
    VALUES (
        :1, :2, :3, :4,
        TO_DSINTERVAL(:5), TO_DSINTERVAL(:6), :7
    )
""", records)

conn.commit()
cursor.close()
conn.close()

print("absences table populated successfully.")
