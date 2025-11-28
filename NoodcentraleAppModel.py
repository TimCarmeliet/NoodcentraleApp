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

            cur.execute("""
                        CREATE TABLE IF NOT EXISTS scenario_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        scenario_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (scenario_id) REFERENCES scenarios(id),
                        FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

#actie TEXT NOT NULL,  #Sturen/Opvragen
#volgorde INTEGER,   #<<Loc>>
#bericht TEXT NOT NULL #<<naam>>

            cur.execute("""

                        CREATE TABLE IF NOT EXISTS scenario_stappen(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        scenario_id INTEGER,
                        actie TEXT NOT NULL,  
                        volgorde INTEGER, 
                        bericht TEXT NOT NULL
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

    def delete_persoon(self, id):
        self.excecuteQuery("DELETE from personen WHERE id=" + str(id))

    def get_personen(self):
        return self.executeQuery("SELECT id, naam, telefoon_nummer FROM personen",fetch=True)
    
    def get_persoon_naam(self, id):
        query = "SELECT naam from personen WHERE id ="+ str(id)
        return self.executeQuery(query, fetch=True)

   #SCENARIO's
    #Voeg een nieuw scenario toe.
    def add_scenario(self, naam, icoon):
        self.executeQuery("INSERT INTO scenarios (naam, icoon) VALUES (?, ?)", (naam, icoon))

    def delete_scenario(self, id):
        self.executeQuery("DELETE from scenarios WHERE id=" + str(id))

    def get_scenarios(self):
        return self.executeQuery("SELECT id, naam, icoon FROM scenarios",fetch=True)
    
    def get_scenario_id(self, naam):
        query = "SELECT id from scenarios WHERE naam=\"" + str(naam) + "\""
        return self.executeQuery(query, fetch=True)
        
    
    def get_scenario_naam(self, id):
        query = "SELECT naam from scenarios WHERE id ="+ str(id)
        return self.executeQuery(query, fetch=True)
    
    #STAPPEN
    #Voeg een nieuwe stappen toe.
    def add_stappen(self, scenario_id, actie, volgorde, bericht):
        self.executeQuery("INSERT INTO scenario_stappen (scenario_id, actie, volgorde, bericht) VALUES (?, ?, ?, ?)", (scenario_id, actie, volgorde, bericht))

    def delete_stappen(self, scenario_id):
        self.excecuteQuery("DELETE from scenario_stappen WHERE scenario_id=" + str(scenario_id))

    def get_stappen(self):
        return self.executeQuery("SELECT id, scenario_id, actie, volgorde, bericht FROM scenario_stappen",fetch=True)
    
    def get_stappen_from_scenario(self, scenario_id):
        stappen = "SELECT * FROM scenario_stappen WHERE scenario_id=" + str(scenario_id) + " order BY volgorde asc"
        print(stappen)
        return self.executeQuery(stappen, fetch=True)
    
    def get_scenario_naam(self, id):
        query = "SELECT naam from scenarios WHERE id ="+ str(id)
        return self.executeQuery(query, fetch=True)
    
    
    #SCENARIO_USERS
    #Voeg een nieuwe scenario gebruikers toe.
    def add_scenario_users(self, scenario_id, user_id):
        self.executeQuery("INSERT INTO scenario_users (scenario_id, user_id) VALUES (?, ?)", (scenario_id, user_id))

    def get_scenario_users(self):
        return self.executeQuery("SELECT id, scenario_id, user_id FROM scenario_users",fetch=True)
    
    def get_users_from_scenario(self, scenario_id):
        users = "SELECT * FROM scenario_users WHERE scenario_id=" + str(scenario_id)
        return self.executeQuery(users, fetch=True)