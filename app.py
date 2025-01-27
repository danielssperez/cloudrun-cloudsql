import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Configuración de conexión a PostgreSQL
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")  # Formato: proyecto:región:instancia

def connect_to_cloudsql():
    """Conecta con la base de datos en Cloud SQL (PostgreSQL)"""
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=f"{INSTANCE_CONNECTION_NAME}",
            port="5432"
        )
        print(connection)
        return connection
    except Exception as e:
        print(f"Error conectando a Cloud SQL: {e}")
        return None

@app.route("/")
def index():
    """Verifica_la conexión a la base de datos"""
    connection = connect_to_cloudsql()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT NOW();")
            result = cursor.fetchone()
        connection.close()
        return jsonify({"status": "success", "server_time": result[0]})
    else:
        return jsonify({"status": "error", "message": "No se pudo conectar a Cloud SQL"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
