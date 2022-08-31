import sqlite3 as sl
import hashlib
import pandas as pd

class FinanceManager:
    """docstring for FinanceManager."""
    def __init__(self):
        self.filename = 'comprovativo.csv'
        self.skiprows = 6
    
    def setFileName(self, filename: str) -> None:
        self.filename = filename
    
    def setSkipRows(self, rows: int) -> None:
        self.skiprows = rows

    def getFileName(self) -> str:
        return self.filename
        
    def fetchDataFrame(self) -> None:
        try:
            df = pd.read_csv(self.filename, sep=';', skiprows=self.skiprows, encoding='latin-1')
            df = df.iloc[:-1,:-1]
            sql = 'INSERT INTO TRANSACTIONS ( description, valueIn, valueOut, date, category, hash) values( ?, ?, ?, ?, ?, ?)'
            data = []
            con = sl.connect('my-finances.db')
        except Exception as e:
            print(f"Error: {e}")
            raise e
        
        with con:
            for _ , row in df.iterrows():
                cur = con.cursor()
                parse = row.to_numpy()
                if(parse[4]!=parse[4]):
                    hash_object = hashlib.md5((parse[2] + '0.0' + parse[3].replace(',','.') + parse[0]).encode())
                    cur.execute("SELECT * FROM TRANSACTIONS WHERE hash=?", (hash_object.hexdigest(),))
                    if(cur.fetchone() is None):
                        data1 = (parse[2],0.0,float(parse[3].replace(',','.')),parse[0],parse[7],hash_object.hexdigest())
                        data.append(data1)
                    
                else:
                    hash_object = hashlib.md5((parse[2] + parse[4].replace(',','.') + '0.0' + parse[0]).encode())   
                    cur.execute("SELECT * FROM TRANSACTIONS WHERE hash=?", (hash_object.hexdigest(),))
                    if(cur.fetchone() is None):              
                        data1 = (parse[2],float(parse[4].replace(',','.')),0.0,parse[0],parse[7],hash_object.hexdigest())
                        data.append(data1)
        
            con.executemany(sql, data)
        print(f"Added {len(data)} new transaction/s!")
        con.close()

    