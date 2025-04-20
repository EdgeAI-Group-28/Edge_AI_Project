import csv
import os
import time
import io
from datetime import date
from aws_rds import send_delta_to_rds  # Assuming you have this defined

def get_delta_from_today_csv():
    today_str = date.today().isoformat()  # Format: YYYY-MM-DD
    file_name = f"temperature_log_{today_str}.csv"
    
    if not os.path.exists(file_name):
        print(f"[{time.ctime()}] File '{file_name}' not found in current directory.")
        return

    delta_rows = []
    updated_rows = []

    try:
        with open(file_name, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames

            if 'db_check' not in fieldnames:
                print(f"[{time.ctime()}] 'db_check' column not found.")
                return

            for row in reader:
                if row['db_check'].strip().upper() == 'FALSE':
                    delta_row = {key: value for key, value in row.items() if key != 'db_check'}
                    delta_rows.append(delta_row)
                    row['db_check'] = 'TRUE'
                updated_rows.append(row)

        if not delta_rows:
            print(f"[{time.ctime()}] No delta rows found.")
            return

        # Send to RDS
        send_delta_to_rds(delta_rows)

        # Save delta CSV string (optional)
        output_csv = io.StringIO()
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames[:-1])
        writer.writeheader()
        writer.writerows(delta_rows)
        output_csv.seek(0)

        print(f"\n[{time.ctime()}] Delta CSV:\n{output_csv.getvalue()}")

        # Write updated rows back to file
        with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

        print(f"[{time.ctime()}] File '{file_name}' updated with 'db_check' set to TRUE.\n")

    except Exception as e:
        print(f"[{time.ctime()}] Error: {e}")

if __name__ == "__main__":
    while True:
        get_delta_from_today_csv()
        print(f"[{time.ctime()}] Waiting 5 minutes...\n")
        time.sleep(300)