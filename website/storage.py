import sqlite3 as sql

def storeData(data, databaseName):
    with sql.connect(databaseName) as con:
        cur = con.cursor()
        
        if cur.execute("select 1 from storage where (itemName, barcode) == (?,?) ", (data[0],data[1])).fetchone():
            cur.execute(
                "update storage set amount = amount + 1 where (itemName, barcode) == (?,?)", (data[0], data[1]))
        else:
            cur.execute("INSERT INTO storage (itemName, barcode, amount) VALUES (?,?, 1)", (data[0], data[1]))
        con.commit()
        print("Data inserted")
    con.close()
    

def loadData(data, databaseName):
    with sql.connect(databaseName) as con:
        cur = con.cursor()

        if cur.execute("select 1 from storage where (barcode) == (?)", (data[1],)).fetchone():
            result = cur.execute("select * from storage where barcode == ? ", (data[1],)).fetchall()

        else :
            result = "The data you are looking for does not exist!"

    return result

def getAll(databaseName):
    with sql.connect(databaseName) as con:
        cur = con.cursor()
        return cur.execute("select * from storage").fetchall()