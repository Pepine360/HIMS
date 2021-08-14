import sqlite3 as sql
from typing import Tuple, List, Dict
from product import Product

class Storage:
    @classmethod
    def CreateItem(self, data : Product, databasePath : str = "storage.db"):
        with sql.connect(databasePath) as con:
            cur = con.cursor()

            if cur.execute("SELECT 1 FROM storage WHERE barcode == (?)", ( data.barcode,)).fetchone():
                cur.execute("UPDATE storage SET amount = amount + ? where barcode == ?", (data.amount, data.barcode))

            else:
                cur.execute("Insert Into storage (barcode, amount) values (?, ?)", (data.barcode, data.amount))

            con.commit()
            print("Data Inserted")
        con.close()
        
    @classmethod
    def ReadItem():
        pass

    @classmethod
    def UpdateItem():
        pass

    @classmethod
    def DeleteItem():
        pass
