import pandas as pd
import oracledb

# connect to the Oracle database
dsn = oracledb.makedsn("localhost", 1521, sid='xe')
conn = oracledb.connect(user="system", password="PLACEHOLDER", dsn=dsn)
cursor = conn.cursor()

def split_name(full_name):
    parts = full_name.strip().split(" ", 1)
    return parts[0], parts[1] if len(parts) > 1 else ""

def prepare_employees(df):
    return pd.DataFrame({
        "first_name": df["Name"].apply(lambda x: split_name(x)[0]),
        "last_name": df["Name"].apply(lambda x: split_name(x)[1]),
        "email": df["Email"].str.lower(),
        "grade": None,
        "line_manager": None,
        "du": None,
        "discipline": None
    }).drop_duplicates(subset=["email"])

# load the CSV files
df_24 = pd.read_csv("june_24th.csv", sep="\t", encoding="utf-16")
df_25 = pd.read_csv("june_25th.csv", sep="\t", encoding="utf-16")
df_26 = pd.read_csv("june_26th.csv", sep="\t", encoding="utf-16")

emp_24 = prepare_employees(df_24)
emp_25 = prepare_employees(df_25)
emp_26 = prepare_employees(df_26)

# first insert from our first training session on June 24th
for _, row in emp_24.iterrows():
    cursor.execute("""
        MERGE INTO employees e
        USING (SELECT :email AS email FROM dual) d
        ON (e.email = d.email)
        WHEN NOT MATCHED THEN
        INSERT (first_name, last_name, email, grade, line_manager, du, discipline)
        VALUES (:first_name, :last_name, :email, :grade, :line_manager, :du, :discipline)
    """, row.to_dict())

# then insert from june_25 and june_26 only if not already in the table
for df in [emp_25, emp_26]:
    for _, row in df.iterrows():
        email = row["email"]
        cursor.execute("SELECT 1 FROM employees WHERE email = :email", {"email": email})
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO employees (first_name, last_name, email, grade, line_manager, du, discipline)
                VALUES (:first_name, :last_name, :email, :grade, :line_manager, :du, :discipline)
            """, row.to_dict())

conn.commit()
cursor.close()
conn.close()

print("employees table populated successfully.")
