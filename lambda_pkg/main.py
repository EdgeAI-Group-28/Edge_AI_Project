import json
import pymysql
import base64

# RDS MySQL connection details
rds_host = "edgeai.cf048y4sc3o2.ap-south-1.rds.amazonaws.com"
db_user = "admin"
db_password = "PerfLog55"
db_name = "edgeai"

# Lambda handler function
def lambda_handler(event, context):
    # Connect to the MySQL database
    connection = pymysql.connect(
        host=rds_host,
        user=db_user,
        passwd=db_password,
        db=db_name,
        connect_timeout=5
    )

    try:
        with connection.cursor() as cursor:
            for record in event['Records']:
                # Decode the base64-encoded Kinesis data
                payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
                print(f"Decoded Payload: {payload}")

                # Assuming the payload is JSON
                data = json.loads(payload)

                # Extract fields (customize as per your payload and table schema)
                device_id = data.get('device_id')
                temperature = data.get('temperature')
                timestamp = data.get('timestamp')

                # Insert into MySQL table (assumes table named `iot_data`)
                sql = """
                    INSERT INTO iot_data (device_id, temperature, timestamp)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (device_id, temperature, timestamp))

            connection.commit()

    except Exception as e:
        print(f"ERROR: {e}")

    finally:
        connection.close()

    return {
        'statusCode': 200,
        'body': json.dumps('Data inserted successfully!')
    }
