# Secure Todo App 🛡️📝

Aplicación web desarrollada como proyecto académico para un **Máster en Ciberseguridad**, enfocada en **Puesta en Producción Segura**.

El objetivo es construir una aplicación funcional, dockerizada y securizada, aplicando buenas prácticas de:
- desarrollo seguro
- despliegue con contenedores
- control de accesos
- pruebas de seguridad básicas

---

## 🎯 Descripción del proyecto

La aplicación consiste en un **gestor de tareas (ToDo)** con las siguientes características:

- Registro y login de usuarios
- Autenticación segura
- Dashboard individual por usuario
- Gestión de tareas personales
- Usuario administrador con permisos globales
- Persistencia en base de datos MySQL
- Arquitectura basada en contenedores Docker

Cada usuario solo puede acceder y gestionar **sus propias tareas**, mientras que el usuario administrador puede gestionar las tareas de todos los usuarios.

---

## 🏗️ Arquitectura y Tecnologías

La aplicación utiliza un stack moderno y seguro:

* **Frontend:** HTML5, Jinja2 y **Tailwind CSS**.
* **Backend:** **Flask (Python)** utilizando Blueprints para una arquitectura modular.
* **Base de Datos:** **MySQL 8.0** con persistencia de datos.
* **ORM:** SQLAlchemy (previene ataques de SQL Injection).
* **Orquestación:** **Docker & Docker Compose** para aislamiento de servicios.

---

## 🔐 Funcionalidades Implementadas

### ✅ Autenticación y Autorización
* Registro de usuarios con validación de integridad.
* Login con gestión de sesión segura mediante `Flask-Login`.
* **Protección contra IDOR:** Un usuario normal no puede visualizar ni eliminar tareas de terceros mediante manipulación de IDs.
* **Vista de Admin:** Etiquetado dinámico de tareas según el propietario original.

### ✅ Interfaz de Usuario (UI)
* **Dashboard Dinámico:** Lista de tareas con descripciones colapsables mediante JavaScript nativo.
* **Diseño Adaptativo:** Totalmente compatible con dispositivos móviles (Responsive Design).
* **Sistema de Alertas:** Feedback visual mediante mensajes flash para errores y confirmaciones.

### ✅ Infraestructura DevSecOps
* **Dockerfile Optimizado:** Basado en Python Slim para reducir la superficie de ataque.
* **Wait-for-DB:** Lógica de espera activa para asegurar la disponibilidad de MySQL antes del arranque del servidor web.
* **Aislamiento de Red:** La base de datos opera en una red interna privada, inaccesible desde el exterior del stack de Docker.

---

## 🔒 Capas de Seguridad Aplicadas

* **Protección de Credenciales:** Hashing de contraseñas mediante `PBKDF2` con salt (vía `werkzeug.security`).
* **Seguridad en Sesiones:** Firma de cookies mediante `SECRET_KEY` gestionada por entorno.
* **Principio de Menor Privilegio:** Roles diferenciados para limitar el radio de acción de los usuarios en caso de compromiso.
* **Validación de Entradas:** Filtrado de datos en servidor antes de procesar cambios en la DB.

---

## ▶️ Cómo ejecutar el proyecto

1. Clonar el repositorio
2. Crear archivo `.env` con las variables necesarias

```text
# Configuración de Flask
FLASK_SECRET_KEY=super-secret-key-change-me


# Configuración de Base de Datos (MySQL)
MYSQL_DATABASE=secure_todo
MYSQL_USER=secure_user
MYSQL_PASSWORD=secure_password
MYSQL_ROOT_PASSWORD=root_password
MYSQL_HOST=db

```

3. Ejecutar:

```bash
docker compose up --build
```

4. Acceder desde el navegador a:

* http://localhost:5000
---

## 📂 Estructura del proyecto
```
secure-todo-app/
├── app/
│ ├── app.py # Punto de entrada de Flask
│ ├── models.py # Modelos de base de datos
│ ├── auth.py # Autenticación y registro
│ ├── tasks.py # Gestión de tareas
│ ├── requirements.txt # Dependencias Python
│ ├── Dockerfile # Imagen Docker de la app
│ ├── templates/ # Vistas HTML
│ └── static/ # Recursos estáticos
│
├── tests/
│ ├── test_auth.py # Pruebas de autenticación
│ └── test_permissions.py # Pruebas de autorización
│
├── docker-compose.yml # Orquestación de contenedores
├── .env # Variables de entorno (no versionado)
└── README.md
```

---

## 🔐 Enfoque de seguridad

El proyecto está diseñado teniendo en cuenta principios básicos de seguridad:

- Hash de contraseñas (nunca en texto plano)
- Separación de servicios
- Variables sensibles gestionadas mediante entorno
- Control de acceso por roles (usuario / administrador)
- Protección frente a accesos no autorizados
- Pruebas unitarias enfocadas a autenticación y permisos

---

## 🧪 Pruebas

Se incluyen pruebas unitarias con **pytest**, enfocadas principalmente en:

- Login correcto e incorrecto
- Acceso no autorizado a rutas protegidas
- Control de permisos entre usuarios y administrador

---

## 🧪 Estado actual del proyecto

### 🟢 FASE COMPLETADA
- Infraestructura Docker
- Conexión Flask ↔ MySQL
- Autenticación segura y persistente
- Gestión de sesiones
- CRUD de tareas con lógica de permisos(RBAC)
- Estilos con TailwindCSS

---

## 👤 Autor

Proyecto desarrollado por Jorge Vázquez Espinosa, estudiante de ciberseguridad.
