import sqlite3

class NoodcentraleAppModel:

    def  __init__(self, db_name):
        self.__db_name = db_name
        self.create_tables()

    #DB NAME
    def get_dbnaam(self):
        return self.__db_name
    
    def connect(self):
        """Maak verbinding met de database."""
        return sqlite3.connect(self.get_dbnaam())
    
    def create_tables(self):
        """Maak de vereiste tabellen aan als ze nog niet bestaan."""
        with self.connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS personen (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    naam TEXT NOT NULL,
                    telefoon_nummer TEXT NOT NULL
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS scenarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    naam TEXT NOT NULL,
                    icoon TEXT
                )
            """)

        conn.commit()
        cur.close()

    #voer een SQL Query uit op deze databank.
    #als je resultaten wil ophalen (bijv select), dan zet je fetch op True
    #in het andere geval zet je fetch op False (bij insert, update, delete) en geef je None terug
    def executeQuery(self, sqlQuery, params=(), fetch=False):
        conn = sqlite3.connect(self.get_dbnaam())
        c = conn.cursor()
        c.execute(sqlQuery, params)
        result = c.fetchall() if fetch else None
        conn.commit()
        conn.close()
        return result


    #PERSONEN
    #Voeg een nieuwe persoon toe.
    def add_persoon(self, naam, telefoon_nummer):
        """
            with self.connect() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (naam, telefoon_nummer) VALUES (?, ?)", (naam, telefoon_nummer))
                conn.commit()
                cur.close()
        """
        self.executeQuery("INSERT INTO personen (naam, telefoon_nummer) VALUES (?, ?)", (naam, telefoon_nummer))

    def get_personen(self):
        return self.executeQuery("SELECT id, naam, telefoon_nummer FROM personen",fetch=True)
    

   #SCENARIO's
    #Voeg een nieuw scenario toe.
    def add_scenario(self, naam, icoon):
        self.executeQuery("INSERT INTO scenarios (naam, icoon) VALUES (?, ?)", (naam, icoon))

    def get_scenarios(self):
        return self.executeQuery("SELECT id, naam, icoon FROM scenarios",fetch=True)
    
    