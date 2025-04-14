import sqlite3

def create_db():
    conn = sqlite3.connect('databaseB.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE "studenti" (
	"id"	INTEGER NOT NULL,
	"nome"	VARCHAR(20) NOT NULL,
	"cognome"	VARCHAR(20) NOT NULL,
	"eta"	INTEGER CHECK(eta>0),
	PRIMARY KEY("id" AUTOINCREMENT)
                );''')
    conn.commit()
    var = cur.fetchall()



def data():
    conn = sqlite3.connect("./databaseB.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM studenti")
    var = cur.fetchall()
    print(var)

if __name__ == "__main__":
    data()