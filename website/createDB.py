import sqlite3 as sql
import click


@click.command()
@click.option('--path', help="database path")
def databaseCreator(path):
    con = sql.connect(path)
    print("Database created!")

    con.execute("create table storage (itemName TEXT NOT NULL, barcode INTEGER, amount INTERGER)")
    print("Table has been made!")
    con.close()

if __name__ == "__main__":
    databaseCreator()