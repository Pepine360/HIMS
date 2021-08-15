import sqlite3 as sql
import click
import string

def scrub(text):
    return "".join( char for char in text if char.isalnum() or char ==  '_')

@click.command()
@click.option('--path', help="Database path")
@click.option('--name', help="Table name")
def databaseCreator(name, path = "storage.db"):
    con = sql.connect(path)
    print("Database created!")

    sqlCommand = f"create table {scrub(name)} (barcode STRING NOT NULL, amount INTERGER)"

    con.execute(sqlCommand)
    print("Table has been made!")
    con.close()

if __name__ == "__main__":
    databaseCreator()
