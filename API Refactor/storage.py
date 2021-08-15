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
                cur.execute("Insert Into storage (name, barcode, amount) values (?, ?)", (data.Name,data.Barcode, data.Amount))

            con.commit()
            print("Data Inserted")
        con.close()
        
    @classmethod
    def ReadItem(self, product : Product, databasePath : str = "storage.db"):
        with sql.connect(databasePath) as con:
            cur = con.cursor()
            try:
                data = cur.execute("SELECT * FROM storage WHERE barcode == (?) OR NAME == (?)", (product.barcode, product.name)).fetchall()
            except:
                data = "No Data Found"
            
        
        
        return {
            "products" : [ item.GetProductData() for item in data ] if type(data) != str else data,
        }

    @classmethod
    def UpdateItem():
        pass

    @classmethod
    def DeleteItem():
        pass
