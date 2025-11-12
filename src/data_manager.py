import sqlite3

class DBManager:
    @staticmethod
    def db(db, table, coluns, data):
        with sqlite3.connect(f"{db}.sqlite") as conn:
            cols_def = ", ".join(f"{c} TEXT" for c in coluns)
            cols_join = ", ".join(coluns)
            placeholders = ", ".join("?" for _ in coluns)

            conn.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, {cols_def})")
            conn.executemany(f"INSERT INTO {table} ({cols_join}) VALUES ({placeholders});", data)
