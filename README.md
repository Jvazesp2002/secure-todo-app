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

## 🏗️ Arquitectura

La aplicación está compuesta por los siguientes servicios:

- **Flask (Python)**  
  Backend web y renderizado de vistas.

- **MySQL**  
  Base de datos relacional para usuarios y tareas.

- **Docker & Docker Compose**  
  Aislamiento de servicios y despliegue reproducible.

Los servicios se comunican a través de una **red interna de Docker**, evitando la exposición innecesaria de la base de datos.

---

## 📂 Estructura del proyecto

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

## 🚧 Estado del proyecto

🟡 **En desarrollo**

Actualmente el proyecto se encuentra en una fase inicial con:
- Estructura definida
- Preparación del entorno
- Base para el desarrollo seguro

Las siguientes fases incluirán:
- Implementación de la lógica de negocio
- Autenticación completa
- Persistencia de datos
- Pruebas de seguridad
- Despliegue completo con Docker

---

## 📌 Nota académica

Este proyecto ha sido desarrollado con fines **formativos**, como parte de un máster en ciberseguridad, aplicando criterios de **puesta en producción segura**.

---

## 👤 Autor

Proyecto desarrollado por Jorge Vázquez Espinosa, estudiante de ciberseguridad.
