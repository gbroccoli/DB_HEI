import psycopg2
from envdatareader import EnvDataReader
from typing import TypedDict


class database(TypedDict):
    host: str
    port: int
    user: str
    passwd: str
    dbName: str


env = EnvDataReader()

# основные чуствительные элементы
DB_CONNECT: database = {
    "host": env.get_value("DB_HOST", "localhost"),
    "port": int(env.get_value("DB_PORT")),
    "user": env.get_value("DB_USER", "postgres"),
    "passwd": env.get_value("DB_PASSWD"),
    "dbName": env.get_value("DB_NAME", "postgres")
}


engien = psycopg2.connect(
    dbname=DB_CONNECT.get("dbName"),
    user=DB_CONNECT.get("user"),
    password=DB_CONNECT.get("passwd"),
    host=DB_CONNECT.get("host"),
    port=DB_CONNECT.get("port")
)

cursor = engien.cursor()

print(DB_CONNECT)


def login(username: str):
    try:
        cursor.execute("SELECT * FROM users WHERE login = %s", (username,))  # noqa

        user = cursor.fetchone()  # Получение первой строки результата запроса

        print(user)

        if user:
            print("Авторизация успешна.")
        else:
            print("Неверный логин.")

    except Exception as e:
        print("Ошибка при выполнении запроса:", e)


login("broccoli")

