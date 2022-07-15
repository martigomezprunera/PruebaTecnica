from colorama import Cursor
from multiprocessing import connection
from datetime import date
import sqlite3

def initialDatabase():
    connection = sqlite3.connect('business.db')
    cursor = connection.cursor()
    # --- INITIAL DATABASE (TABLES) ---
    #Create business table
    #Empresas disponibles
    command1 = """CREATE TABLE IF NOT EXISTS 
    business(id_business INTEGER PRIMARY KEY NOT NULL, name VARCHAR(50), country VARCHAR(50))"""
    cursor.execute(command1)
    #Create favourite business
    #Lista de empresas favoritas
    command2 = """CREATE TABLE IF NOT EXISTS
    favourite_business(org_id INTEGER, favourite_org_id INTEGER, date_favourite VARCHAR(10),
    FOREIGN KEY(org_id) REFERENCES business(id_business),
    FOREIGN KEY(favourite_org_id) REFERENCES business(id_business))"""
    cursor.execute(command2)
    #Initial inserts table business
    cursor.execute("INSERT INTO business VALUES (1, 'Deale', 'España')")
    cursor.execute("INSERT INTO business VALUES (2, 'Everis', 'Alemania')")
    cursor.execute("INSERT INTO business VALUES (3, 'NTTData', 'Francia')")
    cursor.execute("INSERT INTO business VALUES (4, 'Maustec', 'Andorra')")
    cursor.execute("INSERT INTO business VALUES (5, 'Abylight', 'Inglaterra')")
    cursor.execute("INSERT INTO business VALUES (6, 'Indra', 'Bélgica')")
    cursor.execute("INSERT INTO business VALUES (7, 'Ingram', 'España')")
    cursor.execute("INSERT INTO business VALUES (8, 'Cisco', 'Italia')")
    cursor.execute("INSERT INTO business VALUES (9, 'Accenture', 'Alemania')")
    cursor.execute("INSERT INTO business VALUES (10, 'Ubisoft', 'Turquia')")
    #get results
    cursor.execute("SELECT * FROM business")
    results = cursor.fetchall()
    print(results)
    connection.commit()
    connection.close()

def searchIfBusinessExists(org_id, favourite_org_id):
    connection = sqlite3.connect('business.db')
    cursor = connection.cursor()

    #Buscamos si las dos empresas existen 
    cursor.execute("SELECT * FROM business where id_business=" + str(org_id))

    resultOrgId = cursor.fetchall()
    if len(resultOrgId)==0:
        message = "No hay ninguna empresa con este org_id"
        print(message)
        return message

    cursor.execute("SELECT * FROM business where id_business =" + str(favourite_org_id))
    resultFavourite_org_id = cursor.fetchall()
    if len(resultFavourite_org_id)==0:
        message = "No hay ninguna empresa con este favourite_org_id"
        print(message)
        return message

    connection.close()
    return "Existen las dos empresas"

def newFavouriteBusiness(org_id, favourite_org_id):
    connection = sqlite3.connect('business.db')
    cursor = connection.cursor()

    #Una empresa no puede añadirse como favorita asi misma
    if org_id == favourite_org_id:
        return "No puedes añadir tu propia empresa a favoritas" 

    #Comprobaremos que no exista este registro en la BD
    cursor.execute("SELECT * FROM favourite_business where org_id =" + str(org_id) + " AND favourite_org_id=" + str(favourite_org_id))
    dataSelectFavouriteBusiness = cursor.fetchone()

    if dataSelectFavouriteBusiness is None:
        #Actual date
        today = date.today()
        # dd/mm/YY
        d1 = today.strftime("%d/%m/%Y")

        cursor.execute("INSERT INTO favourite_business(org_id, favourite_org_id, date_favourite)"
                        + "VALUES(" + str(org_id) + "," + str(favourite_org_id) + ", '" + str(d1) + "')")

        #get results
        cursor.execute("SELECT * FROM favourite_business")
        favourite_business = cursor.fetchall()
        print(favourite_business)

        connection.commit()
        connection.close()
    else:
        return "Ya tienes esta empresa en favoritos" 









