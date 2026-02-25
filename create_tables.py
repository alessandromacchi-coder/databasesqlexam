import sqlite3

dbpath="f1.db"
conn=sqlite3.connect(dbpath)

with conn: 
    #non mettiamo driver ref perché è come se fosse un cognome univoco

    conn.execute("""
    CREATE TABLE drivers 
        (driverid INTEGER PRIMARY KEY,
        name TEXT NOT NULL, 
        surname TEXT NOT NULL,
        number INT CHECK(number>1 AND <100),
        code TEXT CHECK(lenght(code) = 3 AND code = UPPER(code)),
        dob DATE,
        nationality TEXT,
        url TEXT
                 )
                 """)
