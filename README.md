/mi_proyecto_fastapi
│── /app
│   │── /api              # Routers (endpoints)
│   │   │── /v1
│   │   │   │── auth.py   # Endpoints para autenticación
│   │   │   │── users.py  # Endpoints para usuarios
│   │   │   │── routines.py # Endpoints de rutinas fitness
│   │   │   │── health.py # Endpoints de historial médico
│   │   │   └── exercises.py # Endpoints de ejercicios
│   │── /core             # Configuraciones globales
│   │   │── config.py     # Variables de entorno y settings
│   │   │── security.py   # Configuración de JWT y OAuth
│   │── /models           # Definiciones de modelos SQLAlchemy
│   │── /schemas          # Pydantic schemas para validaciones
│   │── /services         # Lógica de negocio y conexión con BD
│   │── /db               # Configuración de conexión con MySQL
│   │   │── database.py   # Configuración de conexión
│   │── main.py           # Punto de entrada de la aplicación
│── /tests                # Pruebas unitarias e integración
│── .env                  # Variables de entorno
│── requirements.txt      # Dependencias del proyecto
│── Dockerfile            # Configuración para Docker
│── README.md             # Documentación del proyecto


🚀 Requisitos Previos
Asegúrate de tener instalado:

Python 3.10+
MySQL 8.0+
pip y venv para manejar dependencias

📦 Instalación

1️⃣ Clonar el repositorio
    git clone https://github.com/tu_usuario/mi_proyecto_fastapi.git
    cd mi_proyecto_fastapi

2️⃣ Crear y activar un entorno virtual
    python -m venv venv
    source venv/bin/activate  # En Mac/Linux
    venv\Scripts\activate      # En Windows

3️⃣ Instalar dependencias
    pip install -r requirements.txt
    pip freeze > requirements.txt
4️⃣ Configurar las variables de entorno - Crea un archivo .env en la raíz del proyecto con la siguiente estructura:
    DATABASE_URL=mysql+pymysql://usuario:password@host:puerto/nombre_bd
    SECRET_KEY=tu_clave_secreta
    GOOGLE_CLIENT_ID=tu_google_client_id
    GOOGLE_CLIENT_SECRET=tu_google_client_secret

▶️ Ejecutar la Aplicación
    uvicorn app.main:app --reload

🔍 Pruebas - Para ejecutar pruebas unitarias:
    pytest tests/

🐳 Docker (Opcional) - Si quieres correr la aplicación en Docker, ejecuta:
    docker build -t app .
    docker run -p 10000:10000 --env-file .env app


http://127.0.0.1:8000/docs
http://127.0.0.1:8000/v1/users


📜 Licencia
    MIT © 2025 - INTEGRADOR II
