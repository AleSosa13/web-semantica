# Semantic-Python
Repositorio para el proyecto de el grupo 49 (rdflib y Python) en la asignatura CBD.

## Como lanzar el proyecto (local):
Clona el repositorio en la carpeta que desees.

Crea un entorno virtual (opcional):

    python -m venv venv

Activa el entorno virtual:

    · source venv/bin/activate (Linux)
    · venv\Scripts\activate.bat (Windows)

Instala las dependencias:

    pip install -r requirements.txt

Realiza las migraciones:

    cd semantic_site
    python manage.py migrate

Lanza el proyecto:

    python manage.py runserver

El proyecto debería lanzarse correctamente. Por defecto, se lanza en la dirección "http://localhost:8000/".