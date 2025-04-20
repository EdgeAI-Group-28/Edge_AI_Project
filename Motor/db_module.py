import os

import psycopg2  # Change this if you're using a different database like MySQL

def send_delta_to_rds(delta_rows):
    # AWS RDS credentials and connection details
    rds_host = os.getenv('RDS_HOST', 'edgeai.cf048y4sc3o2.ap-south-1.rds.amazonaws.com')
    db_name = os.getenv('DB_NAME', 'EdgeAI')
    user = os.getenv('DB_USER', 'admin')
    password = os.getenv('DB_PASSWORD', 'PerfLog55')
    port = os.getenv('DB_PORT', '3306')



    try:
        # Connect to the RDS PostgreSQL database
        connection = psycopg2.connect(
            host=rds_host,
            dbname=db_name,
            user=user,
            password=password,
            port=port
        )
        cursor = connection.cursor()

        # Insert delta rows into the database
        for row in delta_rows:
            # Assuming your table has columns 'time', 'analog', 'celsius', 'kelvin', 'fahrenheit'
            cursor.execute("""
                INSERT INTO temperature_data (time, analog, celsius, kelvin, fahrenheit)
                VALUES (%s, %s, %s, %s, %s)
            """, (row['time'], row['analog'], row['celsius'], row['kelvin'], row['fahrenheit']))

        # Commit the transaction
        connection.commit()

        print(f"Delta rows have been successfully sent to the RDS database {db_name}.")
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error sending data to RDS: {e}")
