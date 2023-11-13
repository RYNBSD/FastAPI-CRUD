from mysql.connector import connect


def connectDB():
    return connect(host="127.0.0.1", username="root", password="", database="fastapi")


def closeDB(con, cur):
    cur.close()
    con.close()


def createTables():
    con = connectDB()
    cur = con.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS blogs (
      id INTEGER PRIMARY KEY AUTO_INCREMENT,
      title VARCHAR(255) NOT NULL,
      description VARCHAR(255) NOT NULL,
      createsAt DATETIME NOT NULL DEFAULT NOW(),
      updatedAt DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW()
    )"""
    )

    closeDB(con, cur)
