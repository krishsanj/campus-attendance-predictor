
# database.py
import sqlite3

DATABASE = "campus.db"


def get_connection():
    """Connect to the SQLite database."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """Create the students table safely."""
    connection = get_connection()

    table = connection.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='students'"
    ).fetchone()

    if table:
        columns = connection.execute(
            "PRAGMA table_info(students)"
        ).fetchall()

        # Check whether USN is already the primary key.
        usn_is_primary_key = any(
            column["name"] == "usn" and column["pk"] == 1
            for column in columns
        )

        if not usn_is_primary_key:
            # Preserve the old table rather than deleting its records.
            backup_name = "students_backup"
            number = 1

            while connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name=?",
                (backup_name,)
            ).fetchone():
                number += 1
                backup_name = f"students_backup_{number}"

            connection.execute(
                f'ALTER TABLE students RENAME TO "{backup_name}"'
            )

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            usn TEXT PRIMARY KEY
                CHECK(length(usn) = 10),
            name TEXT NOT NULL,
            attendance REAL NOT NULL DEFAULT 0
                CHECK(attendance BETWEEN 0 AND 100),
            internal_marks REAL NOT NULL DEFAULT 0
                CHECK(internal_marks BETWEEN 0 AND 100),
            assignment_completion REAL NOT NULL DEFAULT 0
                CHECK(assignment_completion BETWEEN 0 AND 100),
            previous_performance REAL NOT NULL DEFAULT 0
                CHECK(previous_performance BETWEEN 0 AND 100)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("Database and tables are ready.")
