import glob, re, mysql.connector
from faker import Faker
from pdf_to_string import pdf_to_string

def extract_role(text: str) -> str:
    pattern = r"(?m)^(?P<role>[A-Z0-9 &/]+)\s*Summary"
    match = re.search(pattern, text)

    if match is not None:
        role_raw = match.group("role")
        role_clean = role_raw.title()      
        return role_clean
    else:
        lines = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped:                   
                lines.append(stripped)

        if lines:
            first_line = lines[0]
            return first_line.title()
        else:
            return None

def process_pdf(pdf_path: str, db: dict):
    text = pdf_to_string(pdf_path)
    if not text:
        print(f"[SKIP] kosong: {pdf_path}")
        return

    # generate data dummy
    role  = extract_role(text)
    fake  = Faker()
    first = fake.first_name()
    last  = fake.last_name()

    try:
        # Try multiple connection approaches
        connection_configs = [
            {**db, "auth_plugin": "mysql_native_password", "use_pure": True},
            {**db, "use_pure": True},
            db
        ]
        
        conn = None
        for config in connection_configs:
            try:
                print(f"Trying connection with config: {list(config.keys())}")
                conn = mysql.connector.connect(**config)
                print("Connection successful!")
                break
            except mysql.connector.Error as e:
                print(f"Connection attempt failed: {e}")
                continue
        
        if not conn:
            print("All connection attempts failed")
            return
            
        cur = conn.cursor(prepared=True)

        # insert ke ApplicantProfile
        cur.execute(
            "INSERT INTO ApplicantProfile (first_name, last_name) VALUES (%s, %s)",
            (first, last)
        )
        applicant_id = cur.lastrowid

        cur.execute(
            "INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path) "
            "VALUES (%s, %s, %s)",
            (applicant_id, role, pdf_path)
        )

        conn.commit()
        cur.close()
        conn.close()

        print(f"{pdf_path} dengan id={applicant_id} dan role='{role}'")
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return

if __name__ == "__main__":
    db = {
        "host":     "localhost",
        "user":     "root",
        "password": "",
        "database": "HRProfesional_schema",
        "charset":  "utf8mb4"
    }

    for file in glob.glob("data/**/*.pdf"):
        process_pdf(file, db)