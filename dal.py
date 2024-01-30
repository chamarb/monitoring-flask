import mysql.connector as my
from typing import Any
import time

class Database:
    con: Any = None

    @staticmethod
    def getConnection(retries=3, delay=5) -> Any:
        for _ in range(retries):
            try:
                if Database.con is None:
                    Database.con = my.connect(
                        user='root',
                        password='1234',
                        database='db_hosts',
                        host='db'
                    )
                    print("Connection successful")
                    return Database.con
            except Exception as e:
                print(f"Error connecting to the database: {e}")
                time.sleep(delay)
        return Database.con
    
    @staticmethod
    def close_connection():
        try:
            if Database.con:
                Database.con.close()
                Database.con = None
                print("Connection closed")
        except Exception as e:
            print(f"Error closing the database connection: {e}")


    @staticmethod
    def execute_script(script_path: str):
        con = Database.getConnection()
        try:
            with open(script_path, 'r') as script_file:
                script = script_file.read()
                cursor = con.cursor()
                cursor.execute(script, multi=True)
                con.commit()
                print("Script executed successfully.")
        except Exception as e:
            print(f"Error executing script: {e}")
        finally:
            if cursor:
                cursor.close()
            Database.close_connection()

class IotDao:
    @staticmethod
    def getAllTemp():
        con = Database.getConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM iot_device')
        return cursor.fetchall()

    @staticmethod
    def getAllEndDevices():
        con = Database.getConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM end_device')
        return cursor.fetchall()
    
    @staticmethod
    def add(device):
        con = Database.getConnection()
        cursor = con.cursor()
        # Assuming 'device' is a tuple with (mac, temp, time)
        cursor.execute('INSERT INTO iot_device (mac, temp, time) VALUES (%s, %s, %s)', device)
        con.commit()

    @staticmethod
    def update(device_id, new_temp):
        con = Database.getConnection()
        cursor = con.cursor()
        cursor.execute('UPDATE iot_device SET temp = %s WHERE id = %s', (new_temp, device_id))
        con.commit()

    @staticmethod
    def delete(device_id):
        con = Database.getConnection()
        cursor = con.cursor()
        cursor.execute('DELETE FROM iot_device WHERE id = %s', (device_id,))
        con.commit()

    @staticmethod
    def addEndDevice(name, ip_address, mac_address, longitude, latitude):
        con = Database.getConnection()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO end_device (name, ip_address, mac_address, longitude, latitude) VALUES (%s, %s, %s, %s, %s)",
            (name, ip_address, mac_address, longitude, latitude)
        )
        con.commit()
    
#####
    @staticmethod
    def getAllClients():
        con = Database.getConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM end_device')
        return cursor.fetchall()

    @staticmethod
    def getClientDetails(client_id):
        con = Database.getConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM end_device WHERE id = %s', (client_id,))
        return cursor.fetchone()

    @staticmethod
    def getAllIoTData():
        con = Database.getConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM iot_device')
        return cursor.fetchall()

    @staticmethod
    def getIoTDataForClient(client_id):
        con = Database.getConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM iot_device WHERE client_id = %s', (client_id,))
        return cursor.fetchall()

    @staticmethod
    def deleteClient(client_id):
        con = Database.getConnection()
        cursor = con.cursor()
        cursor.execute('DELETE FROM end_device WHERE id = %s', (client_id,))
        con.commit()

    @staticmethod
    def updateClient(client_id, updated_data):
        try:
            con = Database.getConnection()
            cursor = con.cursor()

            # Extract updated information from the form data
            name = updated_data.get('name')
            ip_address = updated_data.get('ip_address')
            mac_address = updated_data.get('mac_address')
            longitude = updated_data.get('longitude')
            latitude = updated_data.get('latitude')

            # Build the SQL query based on the provided data
            update_query = "UPDATE end_device SET "
            update_data = []

            if name:
                update_query += "name = %s, "
                update_data.append(name)

            if ip_address:
                update_query += "ip_address = %s, "
                update_data.append(ip_address)

            if mac_address:
                update_query += "mac_address = %s, "
                update_data.append(mac_address)

            if longitude is not None:
                update_query += "longitude = %s, "
                update_data.append(longitude)

            if latitude is not None:
                update_query += "latitude = %s, "
                update_data.append(latitude)

            # Remove the trailing comma and execute the query
            update_query = update_query.rstrip(', ')
            update_query += " WHERE id = %s"
            update_data.append(client_id)

            cursor.execute(update_query, update_data)
            con.commit()
            print(f"Client with ID {client_id} updated successfully.")
        except my.Error as e:
            print(f"MySQL Error: {e}")
        finally:
            cursor.close()
            con.close()
