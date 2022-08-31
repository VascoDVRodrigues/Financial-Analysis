import sqlite3 as sl

class DatabaseManager:
    """docstring for DatabaseManager."""

    def __init__(self):
        self.databaseName = 'my-finances'
    
    def setDatabaseName(self, dbn: str) -> None:
        self.databaseName = dbn

    def getDatabaseName(self) -> str:
        return self.databaseName + '.db'

    def createTransactionTable(self) -> None:
        con = sl.connect(self.databaseName + '.db')

        with con:
            try:
                con.execute("""CREATE TABLE TRANSACTIONS (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,description TEXT,valueIn REAL, valueOut REAL, date TEXT, category TEXT, hash TEXT);""")
                print('Transaction table created successfully.')
            except Exception as e:
                print(f"Error: {e}")
        con.close()

    def deleteTransactionTable(self) -> None:
        con = sl.connect(self.databaseName + '.db')

        with con:
            try:
                cursor = con.cursor()
                cursor.execute("DROP TABLE TRANSACTIONS")
                print("Transaction Table dropped")
                con.commit()
            except Exception as e:
                print(f"Error: {e}")
        con.close()