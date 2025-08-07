import pandas as pd
import oracledb
from datetime import datetime

# connect to the Oracle database
dsn = oracledb.makedsn("localhost", 1521, sid="xe")
conn = oracledb.connect(user="system", password="PLACEHOLDER", dsn=dsn)
cursor = conn.cursor()

# load the CSV file
df = pd.read_csv("trainings_filtered.csv")

# prepare the format
insert_rows = []
for i, row in df.iterrows():
    try:
        training_name = row["Subject"]
        session_date = datetime.strptime(row["Start Date"], "%m/%d/%Y").date()
        start_time_obj = datetime.strptime(row["Start Time"], "%I:%M:%S %p").time()
        end_time_obj = datetime.strptime(row["End Time"], "%I:%M:%S %p").time()

        # convert time objects to type INTERVAL string for Oracle
        start_interval = f"+00 {start_time_obj.strftime('%H:%M:%S')}"
        end_interval = f"+00 {end_time_obj.strftime('%H:%M:%S')}"

        insert_rows.append((
            i + 1,  # training_id
            training_name,
            None,  # discipline to be completed later
            session_date,
            start_interval,
            end_interval
        ))
    except Exception as e:
        print(f"Skipping row {i} due to error: {e}")

# insert into the table
cursor.executemany("""
    INSERT INTO trainings (
        training_id, training_name, discipline, session_date, 
        session_start_time, session_end_time
    )
    VALUES (
        :1, :2, :3, :4, 
        TO_DSINTERVAL(:5), TO_DSINTERVAL(:6)
    )
""", insert_rows)

conn.commit()
cursor.close()
conn.close()

print("trainings table populated successfully.")
