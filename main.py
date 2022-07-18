import json
from json.decoder import JSONDecodeError
from flask import Flask, jsonify, request

#DATABASE
from database import *
 
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.before_first_request
def initialize_app_on_first_request():
    initialDatabase()

@app.route("/")
def main():
    app.logger.info("Index Html")
    return "Aquí se encontraría la página inicial!"

@app.route('/addFavourite', methods=['POST'])
def addFavourite():
    try:
        req_Json = json.loads(request.data)
    except JSONDecodeError:
        return jsonify({"response": "El JSON no es correcto"})
    except TypeError:
        return jsonify({"response": "Error inesperado"})
        
    #Control de variables pasadas desde POSTMAN
    if len(req_Json) > 2:
        return jsonify({"response": "Hay mas parametros de los necesarios"})
    if 'org_id' not in req_Json:
        return jsonify({"response": "org_id es obligatorio"})
    if 'favourite_org_id' not in req_Json:
        return jsonify({"response": "favourite_org_id es obligatorio"}) 

    #En caso que se pasen los dos parametros buscamos si estas dos empresas existen
    resultSearch = searchIfBusinessExists(req_Json['org_id'], req_Json['favourite_org_id'])

    #Controlamos respuesta y la mostramos
    if resultSearch == "No hay ninguna empresa con este org_id":
        return jsonify({"response": str(resultSearch)})
    if resultSearch == "No hay ninguna empresa con este favourite_org_id":
        return jsonify({"response": str(resultSearch)})

    #Si existen las dos empresas añadiremos a la empresa que pide el servicio su nueva empresa favorita
    resultNewFavourite = newFavouriteBusiness(req_Json['org_id'], req_Json['favourite_org_id'])

    if resultNewFavourite == "Ya tienes esta empresa en favoritos":
        return jsonify({"response": str(resultNewFavourite)})
    if resultNewFavourite == "No puedes añadir tu propia empresa a favoritas":
        return jsonify({"response": str(resultNewFavourite)})

    return jsonify({"response": "Se ha añadido la empresa a tu lista de favoritos"})

@app.route('/listFavourites', methods=['GET'])
def listFavourites():
    idBusiness = request.args.get('idBusiness')

    if len(request.args) > 1:
       return jsonify({"response": "Solo necesitas el org_id"})

    if idBusiness is None:
       return jsonify({"response": "No has introducido el idBusiness de la empresa"})
    
    listFavourite = listFavouritesBusiness(idBusiness)
    if listFavourite == "No tienes empresas en tu lista de favoritos":
        return jsonify({"response": str(listFavourite)})
    else:
        print("Estoy entrando en cargar JSON")
        return json.loads(str(listFavourite))

@app.route('/deleteFavourite', methods=['DELETE'])
def deleteFavourite():
    org_id = request.args.get('org_id')
    favourite_org_id = request.args.get('favourite_org_id')

    if len(request.args) > 2:
       return jsonify({"response": "Hay mas parametros de los necesarios"})

    if org_id is None:
       return jsonify({"response": "No has introducido el org_id de la empresa"})
    if favourite_org_id is None:
       return jsonify({"response": "No has introducido el favourite_org_id de la empresa"})

    deleteResult = deleteFavouriteOnList(org_id, favourite_org_id)
    return jsonify({"response": str(deleteResult)})

@app.route('/availableBusiness', methods=['GET'])
def listBusiness():

    if len(request.args) > 0:
       return jsonify({"response": "Hay mas parametros de los necesarios"})

    listBusiness = availableBusiness()
    return json.loads(listBusiness)   

@app.route('/addNewBusiness', methods=['POST'])
def newBusiness():
    try:
        req_Json = json.loads(request.data)
    except JSONDecodeError:
        return jsonify({"response": "El JSON no es correcto"})
    except TypeError:
        return jsonify({"response": "Error inesperado"})

    #Control de variables pasadas desde POSTMAN
    if len(req_Json) > 2:
        return jsonify({"response": "Hay mas parametros de los necesarios"})
    if 'name' not in req_Json:
        return jsonify({"response": "name es obligatorio"})
    if 'country' not in req_Json:
        return jsonify({"response": "country es obligatorio"}) 

    newBusinessResult = addNewBusiness(req_Json['name'], req_Json['country'])
    return jsonify({"response": str(newBusinessResult)})