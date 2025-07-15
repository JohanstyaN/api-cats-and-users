# 🐾 Cats & Users API

Una API RESTful desarrollada con **FastAPI** que combina dos dominios:

1. **Breeds**: consume la API pública de gatos (TheCatAPI).  
2. **Users**: gestiona usuarios almacenados en MongoDB con autenticación.

Incluye:
- Contenedores Docker (FastAPI + MongoDB)  
- Suite de tests automatizados con **pytest**  
- Colección Postman para pruebas manuales  
- Script `run_tests.sh` para lanzar todo en un solo comando  

---

## 🚀 Características

### Breeds (Gatos)
- **GET** `/breeds`  
  Lista todas las razas de gatos.  
- **GET** `/breeds/search?q={término}&attach_image={true|false}`  
  Busca razas por texto, opcionalmente incluye datos de imagen.  
- **GET** `/breeds/{breed_id}`  
  Devuelve detalle de una raza.

### Users (Usuarios)
- **GET** `/users`  
  Lista todos los usuarios (sin contraseña).  
- **POST** `/users`  
  Crea un usuario: recibe `name`, `last_name`, `password`; genera `username` único y guarda la contraseña hasheada.  
- **GET** `/users/login?username={u}&password={p}`  
  Autentica credenciales y devuelve datos del usuario.

---

## 📦 Requisitos
- Docker & Docker Compose  
- (Opcional) Python 3.9+ y pip para ejecución local  

---

## 🔧 Variables de entorno

Crea un fichero `.env` en la raíz del proyecto y añade:

~~~dotenv
MONGO_URI=mongodb://mongodb:27017
MONGO_DB=api_db
CAT_API_KEY=live_JBT0Ah0Nt12iyl2IpjQVLDWjcLk0GQwf4zI9wBMfmfejKmcC31mOJp4yJz5TsOUP
CAT_API_URL=https://api.thecatapi.com/v1
~~~


## 🏗️ Instalación y ejecución con Docker Compose

~~~bash
# 1. Clona el repositorio
git clone https://github.com/JohanstyaN/api-cats-and-users.git
cd api-cats-and-users

# 2. Construye y levanta los contenedores en segundo plano
docker-compose up --build -d

# 3. Verifica que estén corriendo
docker-compose ps
# Debes ver algo como:
# cats_users_mongo  Up   0.0.0.0:27017->27017/tcp
# cats_users_api    Up   0.0.0.0:8001->80/tcp

# 4. (Opcional) Visualiza logs
docker-compose logs -f api
~~~

## 📡 Documentación interactiva

~~~text
Swagger UI → http://localhost:8001/docs  
ReDoc       → http://localhost:8001/redoc
~~~

---

## 🔍 Probar con curl

~~~bash
# Razas
curl  http://localhost:8001/breeds
curl  "http://localhost:8001/breeds/search?q=siam&attach_image=true"
curl  http://localhost:8001/breeds/aege

# Usuarios
curl  http://localhost:8001/users
curl -X POST http://localhost:8001/users \
     -H "Content-Type: application/json" \
     -d '{"name":"Test","last_name":"User","password":"secret123"}'
curl  "http://localhost:8001/users/login?username=test.user&password=secret123"
~~~

---

## 📋 Colección Postman

~~~text
1. Importa el fichero api/CatsUsers.postman_collection.json  
2. Importa el fichero api/LocalEnvironment.postman_environment.json  
3. Selecciona el Environment “Local (8001)”  
4. Ejecuta los requests de las carpetas “Cats” y “Users”
~~~

---

## 🧪 Tests automatizados

~~~bash
# 1) Ejecutar manual dentro del contenedor API:
docker exec -it cats_users_api bash
pytest -q
exit

# 2) Automatizado con el script:
chmod +x run_tests.sh
./run_tests.sh
~~~

> El script realiza:
> 1. `docker-compose up --build -d`  
> 2. Espera a que `/breeds` responda  
> 3. Ejecuta `pytest -q`  
> 4. `docker-compose down -v` (borra volúmenes)

---

## 📁 Estructura del proyecto

~~~text
api-cats-and-users/
├── api/                              # Colección Postman
│   ├── CatsUsers.postman_collection.json
│   └── LocalEnvironment.postman_environment.json
├── app/                              # Código fuente
│   ├── config/settings.py
│   ├── models/
│   │   ├── cat.py
│   │   └── user.py
│   ├── routers/
│   │   ├── cats.py
│   │   └── users.py
│   ├── services/
│   │   ├── cats_service.py
│   │   └── users_services.py
│   └── utils/
│       ├── generate_user.py
│       └── notifier.py
├── tests/                            # Tests con pytest
│   ├── conftest.py
│   ├── test_cats.py
│   └── test_users.py
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
└── run_tests.sh
~~~

---

## ⚠️ Notas importantes

- En producción: **HTTPS** obligatorio para exponer tu `CAT_API_KEY`.  
- El login viaja por **query params** (`GET`) por requisito; en otros casos se recomienda **POST + body**.  
- Para cambiar puertos, edita `docker-compose.yml`.

---

## 👤 Autor

Desarrollado por **Johan Sebastian Cañon**  
GitHub: [@JohanstyaN](https://github.com/JohanstyaN)
