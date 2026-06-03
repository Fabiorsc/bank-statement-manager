from database.connection import get_connection


class SchemaInspector:

    @staticmethod
    def get_columns(table_name):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = [
            row["name"]
            for row in cursor.fetchall()
        ]

        conn.close()

        return columns

    @staticmethod
    def get_rows(table_name):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT * FROM {table_name}"
        )

        rows = cursor.fetchall()

        conn.close()

        return rows