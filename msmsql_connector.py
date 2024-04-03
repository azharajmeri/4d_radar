import pymssql


def get_connection():
    try:
        conn = pymssql.connect(server="192.168.40.200:1435", user="VASDTEST", password="1234567890", database="KNR_ATMS")
        return conn
    except Exception as e:
        print("\nERROR:", e)
        return None


def insert_record(rec_id, frame_number, speed, time, lane_number, image, location):
    print(rec_id, frame_number, speed, time, lane_number, image, location)
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO SpeedRecord (id, frame_number, speed, time, lane_number, image, location)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute("SET IDENTITY_INSERT SpeedRecord ON")
        cursor.execute(insert_query, (rec_id, frame_number, speed, time, lane_number, image, location))
        conn.commit()
    except Exception as e:
        print("\nERROR during insertion:", e)
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()


def select_all_records():
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        select_query = "SELECT * FROM SpeedRecord"
        cursor.execute(select_query)
        records = cursor.fetchall()
        return records
    except Exception as e:
        print("\nERROR during selection:", e)
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()


def delete_all_records():
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        delete_query = "DELETE FROM SpeedRecord"
        cursor.execute(delete_query)
        conn.commit()
        print("All records deleted successfully.")
    except Exception as e:
        print("\nERROR during deletion:", e)
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()


def main():
    # Get database connection
    conn = get_connection()
    if conn is None:
        exit(-1)

    try:
        cursor = conn.cursor()

        # Create table if not exists
        create_table_query = """
        IF OBJECT_ID('SpeedRecord', 'U') IS NULL
        BEGIN
            CREATE TABLE SpeedRecord (
                id INT PRIMARY KEY IDENTITY,
                frame_number NVARCHAR(255),
                speed FLOAT,
                time DATETIME,
                lane_number INT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                image NVARCHAR(255) NULL,
                location NVARCHAR(255) NULL
            )
        END
        """
        cursor.execute(create_table_query)
        conn.commit()  # Commit the table creation

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()


main()
