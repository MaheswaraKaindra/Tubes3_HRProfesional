import mysql.connector, string

def get_applicant_by_cv_path(cv_path: string):
    db = {
        "host":     "localhost",
        "user":     "root",
        "password": "meteor",
        "database": "HRProfesional_schema",
        "charset":  "utf8mb4"
    }
    try:
        connection_configs = [
            {**db, "auth_plugin": "mysql_native_password", "use_pure": True},
            {**db, "use_pure": True},
            db
        ]
        
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
            print("Gagal koneksi ke database.")
            return

        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT ap.applicant_id, ap.first_name, ap.last_name, ap.date_of_birth, ap.address, ap.phone_number,
                   ad.detail_id, ad.application_role, ad.cv_path
            FROM ApplicantProfile ap
            LEFT JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
            WHERE ad.cv_path = %s
        """, (cv_path,))

        result = cur.fetchall()
        cur.close()
        conn.close()

        if result:
            for row in result:
                print("Data Pelamar:")
                print(f"ID: {row['applicant_id']}")
                print(f"Nama: {row['first_name']} {row['last_name']}")
                print(f"Tanggal Lahir: {row['date_of_birth']}")
                print(f"Alamat: {row['address']}")
                print(f"No. HP: {row['phone_number']}")
                print(f"Role: {row['application_role']}")
                print(f"CV Path: {row['cv_path']}")
            return result
        else:
            print(f"Tidak ditemukan pelamar dengan path {cv_path}")
            return None

    except mysql.connector.Error as err:
        print(f"Kesalahan Database: {err}")
    except Exception as e:
        print(f"Kesalahan lain: {e}")

if __name__ == "__main__":
    get_applicant_by_cv_path(r"data\Teacher\17311685.pdf")
