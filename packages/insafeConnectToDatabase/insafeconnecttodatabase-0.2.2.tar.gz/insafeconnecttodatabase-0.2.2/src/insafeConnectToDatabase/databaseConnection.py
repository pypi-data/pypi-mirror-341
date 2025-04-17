import psycopg2
import subprocess

from util.wait_for_proxy import wait_for_proxy

# Database connection string
CLOUD_SQL_CONNECTION_NAME = "cntxt-product-work-permit:me-central2:work-permit-development"
SERVICE_ACCOUNT_KEY_PATH = "./sql_service_account_key.json"


def connect_to_db():
    try:
        if CLOUD_SQL_CONNECTION_NAME:
            print("Starting Cloud SQL Proxy...")

            # Run the Cloud SQL Proxy as a subprocess
            proxy_process = subprocess.Popen(
                [
                    "./cloud-sql-proxy",
                    CLOUD_SQL_CONNECTION_NAME,
                    f"--credentials-file={SERVICE_ACCOUNT_KEY_PATH}"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            wait_for_proxy()
            print("Cloud SQL Proxy started.")

        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="staging",
            user="staging",
            password="Y1TEJLTd2QKFeQ",
            host="127.0.0.1",
            port="5432"
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Example: Execute a query
        # cursor.execute("SELECT NOW();")
        # query="SELECT id, name, status, dynamicData FROM WorkflowInstance;"
        cursor.execute("SET search_path TO public;")

        query = """
        SELECT id, name, status, "dynamicData"
        FROM "WorkflowInstance";
        """

        cursor.execute(query)
        result = cursor.fetchone()

        print("Database time:", result)

        # Close the cursor and the connection when done
        cursor.close()
        connection.close()
        return result[1]

    except Exception as e:
        print("Error connecting to the database:", e)

    finally:
        # Ensure the Cloud SQL Proxy subprocess is terminated
        if 'proxy_process' in locals() and proxy_process.poll() is None:
            proxy_process.terminate()
            print("Cloud SQL Proxy terminated.")

connect_to_db()