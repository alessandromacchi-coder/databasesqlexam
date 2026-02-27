import sqlite3

dbpath="f1.db"
conn=sqlite3.connect(dbpath)

with conn: 
    #non mettiamo driver ref perché è come se fosse un cognome univoco
    #non mettiamo neanche constructor ref per la stessa ragione, idem circuitref
    conn.execute("""
    CREATE TABLE drivers 
        (driverid INTEGER PRIMARY KEY,
        name TEXT NOT NULL, 
        surname TEXT NOT NULL,
        number INT CHECK(number>1 AND number<100),
        code TEXT CHECK(length(code) = 3 AND code = UPPER(code)),
        dob DATE,
        nationality TEXT,
        url TEXT
                 );
                 """)


    conn.execute("""
    CREATE TABLE constructors (
                 constructorid INTEGER PRIMARY KEY,
                 name TEXT NOT NULL, 
                 nationality TEXT,
                 url TEXT
                 );
                 """)
    
    conn.execute("""
    CREATE TABLE circuits (
        circuitid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT,
        country TEXT,
        lat REAL,
        lng REAL,
        alt REAL,
        url TEXT
    );
    """)
    
    conn.execute("""
    CREATE TABLE status (
    statusid INTEGER PRIMARY KEY,
    status TEXT NOT NULL
                 );
                 """)
    
    conn.execute("""
    CREATE TABLE races (
    raceid INTEGER PRIMARY KEY,
    year INTEGER NOT NULL,
    round INTEGER NOT NULL,
    circuitid INTEGER,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time_race TEXT,
    url TEXT,
    fp1_date TEXT,
    fp1_time TEXT,
    fp2_date TEXT,
    fp2_time TEXT,
    fp3_date TEXT,
    fp3_time TEXT,
    quali_date TEXT,
    quali_time TEXT,
    sprint_date TEXT,
    sprint_time TEXT,
    FOREIGN KEY (circuitid) REFERENCES circuits(circuitid)
    );
    """)

    conn.execute("""
    CREATE TABLE results (
    resultid INTEGER PRIMARY KEY,
    raceid INTEGER,
    driverid INTEGER,
    constructorid INTEGER,
    statusid INTEGER,
    number INTEGER,
    grid INTEGER,
    position INTEGER,
    positionText TEXT,
    positionOrder INTEGER NOT NULL,
    points REAL,
    laps INTEGER,
    time_result TEXT,
    milliseconds INTEGER,
    fastestLap INTEGER,
    rank INTEGER,
    fastestLapTime TEXT,
    fastestLapSpeed REAL,
    FOREIGN KEY (raceid) REFERENCES races(raceid),
    FOREIGN KEY (driverid) REFERENCES drivers(driverid),
    FOREIGN KEY (constructorid) REFERENCES constructors(constructorid),
    FOREIGN KEY (statusid) REFERENCES status(statusid)
        );
                 """)