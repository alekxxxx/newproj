import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_connection():
    for _ in range(10):
        try:
            return psycopg2.connect(
                host="db",
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                dbname=os.environ["POSTGRES_DB"]
            )
        except psycopg2.OperationalError:
            time.sleep(2)
    raise Exception("Error: Не удалось подключиться к базе данных")

@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    cur.close()
    conn.close()
    return f"Соединение с базой установлено! Версия: {version[0]}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
