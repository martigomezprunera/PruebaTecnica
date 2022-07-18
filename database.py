import os
from colorama import Cursor
from multiprocessing import connection
from datetime import date
import sqlite3

def initialDatabase():

    dbExists = os.path.exists('./business.db')
    
    if not dbExists: 
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
        print("Lista de empresas:" + str(results))
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
        return message

    cursor.execute("SELECT * FROM business where id_business =" + str(favourite_org_id))
    resultFavourite_org_id = cursor.fetchall()
    if len(resultFavourite_org_id)==0:
        message = "No hay ninguna empresa con este favourite_org_id"
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

        connection.commit()
        connection.close()
    else:
        return "Ya tienes esta empresa en favoritos" 

def listFavouritesBusiness(org_id):
    connection = sqlite3.connect('business.db')
    cursor = connection.cursor()

    cursor.execute("SELECT org_id, favourite_org_id, date_favourite, name" 
                    + " FROM favourite_business" 
                    + " INNER JOIN business"
                    + " ON business.id_business = favourite_business.favourite_org_id"
                    + " WHERE org_id =" + str(org_id))
    dataSelectList = cursor.fetchall()

    #Creamos el esqueleto de la consulta
    listFavourites = "{\"ListFavourites\":["
    #En caso que solo haya una en favoritos
    if len(dataSelectList) == 1:
        for row in dataSelectList:
            listFavourites += "{"
            listFavourites += "\"name\": " + "\"" + str(row[3]) + "\", "
            listFavourites += "\"org_id\": " + str(row[0]) + ", "
            listFavourites += "\"favourite_org_id\": " + "" +str(row[1]) + ", "
            listFavourites += "\"date_favourite\": " + "\"" + str(row[2]) + "\""
            listFavourites += "}"
        listFavourites += "]}"
        resultListFavourites = listFavourites

    if len(dataSelectList) > 1:
        for row in dataSelectList:
            listFavourites += "{"
            listFavourites += "\"name\": " + "\"" + str(row[3]) + "\", "
            listFavourites += "\"org_id\": " + str(row[0]) + ", "
            listFavourites += "\"favourite_org_id\": " + "" +str(row[1]) + ", "
            listFavourites += "\"date_favourite\": " + "\"" + str(row[2]) + "\""
            listFavourites += "},"
        resultListFavourites = listFavourites.rstrip(listFavourites[-1])
        resultListFavourites += "]}"

    print(resultListFavourites)
    connection.commit()
    connection.close()

    if len(dataSelectList) > 0:
        return resultListFavourites
    else:
        return "No tienes empresas en tu lista de favoritos"

def deleteFavouriteOnList(org_id, favourite_org_id):
    connection = sqlite3.connect('business.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM favourite_business where org_id =" + str(org_id) + " AND favourite_org_id=" + str(favourite_org_id))
    deleteFavouriteResult = cursor.fetchall()

    if len(deleteFavouriteResult) == 1:
        cursor.execute("DELETE FROM favourite_business where org_id =" + str(org_id) + " AND favourite_org_id=" + str(favourite_org_id))
        connection.commit()
        connection.close()
        return "Se ha eliminado la empresa favorita"
    else:
        return "No existe esa empresa favorita para la empresa seleccionada"

def availableBusiness():
    connection = sqlite3.connect('business.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM business")
    dataSelectList = cursor.fetchall()

    #Creamos el esqueleto de la consulta
    listBusiness = "{\"AvailableBusiness\": ["
    #En caso que solo haya una empresa
    if len(dataSelectList) == 1:
        for row in dataSelectList:
            listBusiness += "{"
            listBusiness += "\"id_business\": " +  str(row[0]) + ", " 
            listBusiness += "\"name\": " + "\"" + str(row[1]) + "\", "
            listBusiness += "\"country\": " + "\"" + str(row[2]) + "\""
            listBusiness += "}"
        listBusiness += "]}"
        resultlistBusiness = listBusiness

    if len(dataSelectList) > 1:
        for row in dataSelectList:
            listBusiness += "{"
            listBusiness += "\"id_business\": " +  str(row[0]) + ", " 
            listBusiness += "\"name\": " + "\"" + str(row[1]) + "\", "
            listBusiness += "\"country\": " + "\"" + str(row[2]) + "\""
            listBusiness += "},"
        resultlistBusiness = listBusiness.rstrip(listBusiness[-1])
        resultlistBusiness += "]}"

    connection.close()
    if len(dataSelectList) > 0:
        return resultlistBusiness
    else:
        return "No tienes empresas en tu lista de favoritos"

def addNewBusiness(name, country):
    connection = sqlite3.connect('business.db')
    cursor = connection.cursor()

    #Comprobaremos que no exista este registro en la BD
    print("SELECT * FROM business WHERE name = '" + str(name) + "'")
    cursor.execute("SELECT * FROM business WHERE name = '" + str(name) + "'")
    dataExists = cursor.fetchone()

    if dataExists is None:
        cursor.execute("INSERT INTO business(name, country)"
                        + "VALUES(" + "'" + str(name) + "', " + "'" + str(country) + "')")

        print("INSERT INTO business(name, country)"
                        + "VALUES(" + "'" + str(name) + "', " + "'" + str(country) + "')")
        connection.commit()
        connection.close()
        return "Se ha añadido la nueva empresa"
    else:
        return "Ya existe esta empresa" 
