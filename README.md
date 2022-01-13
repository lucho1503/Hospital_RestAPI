# Hospital_RestAPI

## Descripcion

Servicio web (API REST) que sirve endpoints para un sistema de gestion de historia clinica centralizada, utilizando python con Flaks y PostgreSQL como motor de base de datos.

## Como instalar

* Base de datos:
  * `/modelos/engine/dbstorage.py`
  * configurar el mmetodo `__init__` en la linea `self.__enfine = db.create_engine('postgresql://usuario:password@localhost/API_REST_HOSPITAL')`,
  poner su usuario y password de postgres.
  
* Dependencias:
  * `requeriments.txt`
  * para instalar todos los paquetes necesarios para correr la API recomiendo instalar un entorno virtual:
  `python3 -m venv <nombre del entorno>` luego `source <nombre del entorno>/bin/activate`
  * luego dentro del entorno virtual ejecutar `pip install -r requeriments.txt`
  * variables de entorno: para poder enviar los correos de confirmacion, es necesario ajustar las variables de entorno con `mail:correo que envia`
  y `password:password del correo`
  
## Modulos y archivos:

  * `/modelos`: En este paquete e encuentran declaradas todas las clases usadas en la API.
  * `/modelos/engine`: Aqui se encuentra el modulo `dbstorage.py` encargado de conectarse con la base de datos y gestionar todos los objetos en ella.
  * `/api/v1`: Se encuentra el modulo `app.py` en el que se inicia la API, y se conecta con todas las blueprints y metodos de la API.
  
## Ejecutar:

  * En linux desde la carpeta raiz del proyecto ejecutar `python3 -m api.v1.app`
  
## Metodos/rutas

  * Registrar usuarios: de entrada a la API permite registrar dos tipos de usuario
  `hospital` y `paciente`, ademas crea un link para autenticar el registro por medio del correo.
  
  * Registrar paciente:
  ```http
  POST /api/v1/register
  ```
  Recibe los siguientes parametros:
  ```JSON
  {
  "usuario" : "paciente",
  "formulario": {
                "nombre": string,
                "id": string,
                "password": string,
                "correo": string,
                "telefono": string,
                "direccion": string,
                "fecha de nacimiento": string
                }
  }
  ```
  
  * Registrar hospital:
  ```http
  POST /api/v1/register
  ```
  Recibe los siguientes paremetros:
  ```JSON
  {
  "usuario": "hospital",
  "formulario" : {
                 "nombre": string,
                 "id": string,
                 "password": string,
                 "correo": string,
                 "telefono": string,
                 "direccion": string
                 },
  "servicios": ["string", "string", ...]
  }
  ```
  * Login usuarios: para hacer login es necesario haberse verificado con el correo.
  ```http
  POST /api/v1/login
  ```
  Recibe los siguientes parametros:
  ```JSON
  {
  "id": string,
  "password": string
  }
  ```
  Retorna un token para el acceso al sistema.
  ```
  {
  "id": "token"
  }
  ```
  
  * Reiciniar password: crea un enlace para reiniciar el password con el correo.
  ```http
  POST /api/v1/reset_password
  ```
  Recibe los siguientes parametros:
  ```JSON
  {
  "correo": string
  }
  ```

## Metodos/rutas con el uso del token o con usuario autenticado

Cada que un usuario hace login y este es exitoso la API reotrna un token
que se debe enviar en los headers como:
  `"Authorization": Bearer token`
todos los metodos que acontinuacion utilizan este token para funcionar.

  * Registrar medicos: solo los usuarios de tipo hospital pueden registrar
  un nuveo medico.
  ```http
  POST /api/v1/registrar_medico
  ```
  Recibe los siguientes parametros:
  ```JSON
  {
  "usuario": "paciente",
  "formulario": {
                "nombre": string,
                "id": string,
                "password": string,
                "correo": string,
                "telefono": string,
                "direccion": string,
                "especialidad": string
                }
  }
  ```
  
  * Registrar observacion: solo los usuarios de tipo medico pueden registrar una
  observacion de sus pacientes.
  ```http
  PUT /api/v1/registrar_observacion
  ```
  Recibe los siguientes parametros:
  ```JSON
  {
  "formulario": {
                "paciente_id": string,
                "registro": string
                }
  }
  ```
  
  * Consultar registros: un usuario de tipo paciente puede consultar solo sus
  regisros, uno de tipo Medico solo puede consultar los registros realizados por
  el mismo y un usuario de tipo Hospital solo puede consultar los registros realizados
  por sus medicos.
  ```http
  GET /api/v1/consultar
  ```
  Retorna un diccionario tipo JSON con los registros.
  
  * Descargar registros: un usuario de tipo medico puede descargar todas las observaciones 
  registradas a un paciente en formato csv.
  ```http
  GET /descargar_consulta/<paciente_id>
  ```
  Retorna un archivo en formato csv.
  
  * cambiar password:
  ```http
  POST api/v1/change_password
  ```
  Recibe los siguientes parametros:
  ```JSON
  {
    "old_password": string,
    "new_password": string
  }
  ```
  
## Status codigos

La API retorna los siguientes codigos de status:

| Status code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 401 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |


  
