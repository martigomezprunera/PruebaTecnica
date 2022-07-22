# PruebaTecnica
# COMANDOS PARA INICIAR LA API
1. Comprobación de la instalación de Python, FLASK y Postman en el PC donde se realice la ejecucion de la prueba.
    - En caso de no tener instalado Python iremos a la ruta: https://www.python.org/ e instalaremos la version de Python.
    - Comprobaremos si se ha instalado Python desde cmd. (Para abrir el cmd, vamos al buscador de windows, escribimos cmd y ejecutamos como administrador)
    - Una vez dentro pondremos el comando python -V. En caso que lo tengamos instalado saldrá por pantalla la version que tenemos instalada.
    - Seguidamente tengamos la versión instalada de Python, en el cmd pondremos lo siguiente: pip install flask.
    - Una vez tengamos instalado FLASK, instalaremos Postman, para ello nos dirigiremos a la siguiente ruta: https://www.postman.com/
    - Una vez instalado Postman, lo abiremos e importaremos lo siguiente: Prueba_Tecnica_Deale.postman_collection.

2. Una vez instalado todos los requisitos previos, entraremos otra vez en el cmd (Para abrir el cmd, vamos al buscador de windows, escribimos cmd y ejecutamos como administrador) y realizaremos lo siguiente:
    - cd (ruta donde se encuentre el main.py) -> set FLASK_APP=main.py -> flask run

3. Nos dirigiremos a los servicios en postman importados y podremos consultar cada uno de estos servicios.
    - 3.1 AvailableBusiness -> Mostrará una lista de todas las empresas disponibles
    - 3.2 AddNewBusiness -> Permite añadir una nueva empresa, para ello se tiene que introducir lo siguiente en el body en formato JSON:
    Ejemplo:{
                "name": "Amazon", -> Nombre de la empresa
                "country": "Brasil" -> País
            }
    - 3.3 AddFavourite -> Permite añadir una empresa como favorita, para ello se tiene que introducir lo siguiente en el body en formato JSON:
    Ejemplo:{
                "org_id": 2,    -> Empresa la cual quiere añadir la otra empresa
                "favourite_org_id": 13  -> Empresa que se quiere añadir
            }
    - 3.4 ListFavourites -> Permite visualizar las empresas marcadas como favoritas, para ello se tiene que introducir en la seccion Params:
    Ejemplo: idBusiness 2
    - 3.5 DeleteFavourite -> Permite borrar una empresa de la lista de favoritos de una empresa, para ello se tiene que introducir en la seccion Params:
    Ejemplo: org_id 2
             favourite_org_id 10