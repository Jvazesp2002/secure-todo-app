# Secure Todo App 

Aplicación web desarrollada como proyecto académico para un **Máster en Ciberseguridad**, enfocada en **Puesta en Producción Segura**.

El objetivo es construir una aplicación funcional, dockerizada y securizada, aplicando buenas prácticas de:
- desarrollo seguro
- despliegue con contenedores
- control de accesos
- pruebas de seguridad básicas


##  Descripción del proyecto

La aplicación consiste en un **gestor de tareas (ToDo)** con las siguientes características:

- Registro y login de usuarios con políticas de cookies seguras.
- Autenticación robusta y gestión de sesiones cifradas.
- Dashboard individual con aislamiento de datos por usuario.
- Usuario administrador con privilegios elevados (RBAC).
- **Tráfico íntegramente cifrado mediante TLS/SSL**.
- Arquitectura de microservicios protegida por un **Proxy Inverso**.

Cada usuario solo puede acceder y gestionar **sus propias tareas**, mientras que el usuario administrador puede gestionar las tareas de todos los usuarios.


##  Arquitectura y Tecnologías

La aplicación utiliza un stack moderno y seguro:

* **Frontend:** HTML5, Jinja2 y **Tailwind CSS**.
* **Backend:** **Flask (Python)** protegido con `ProxyFix` para terminación SSL.
* **Proxy Inverso:** **Nginx** actuando como escudo perimetral y gestor de certificados.
* **Base de Datos:** **MySQL 8.0** (aislada de la red pública).
* **ORM:** SQLAlchemy (parametrización nativa contra SQL Injection).
* **Orquestación:** **Docker Compose** con redes internas segmentadas.


##  Funcionalidades Implementadas

###  Cifrado de Extremo a Extremo (HTTPS)
* **Certificados SSL:** Uso de certificados (auto-firmados para desarrollo) que garantizan la privacidad del tráfico.
* **Redirección Forzosa:** El puerto 80 (HTTP) redirige automáticamente al 443 (HTTPS) mediante código de estado 301.
* **Protocolos Seguros:** Configuración de Nginx limitada a **TLS 1.2 y 1.3** para evitar ataques de degradación de protocolo.

###  Protección contra Ataques Web
* **Defensa CSRF:** Protección global mediante tokens contra *Cross-Site Request Forgery* en todos los formularios.
* **Validación de Referer:** Control estricto de cabeceras en peticiones HTTPS para asegurar el origen legítimo del tráfico.
* **Hardening de Cookies:** Uso de flags `Secure`, `HttpOnly` y `SameSite=Lax` para mitigar el secuestro de sesiones (Session Hijacking).

###  Infraestructura DevSecOps
* **Aislamiento de Puertos:** El contenedor de Flask ha sido retirado del mapeo público (puerto 5000 cerrado), exponiéndose únicamente de forma interna hacia Nginx.
* **Proxy Inverso Seguro:** Nginx actúa como única puerta de enlace, ocultando la topología interna y la tecnología del backend.


##  Capas de Seguridad Aplicadas

* **Protección de Credenciales:** Hashing de contraseñas mediante `PBKDF2` con salt (vía `werkzeug.security`).
* **Seguridad en Sesiones:** Firma de cookies mediante `SECRET_KEY` gestionada por entorno.
* **Principio de Menor Privilegio:** Roles diferenciados para limitar el radio de acción de los usuarios en caso de compromiso.
* **Validación de Entradas:** Filtrado de datos en servidor antes de procesar cambios en la DB.

##  Cómo ejecutar el proyecto

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

* https://localhost
---

##  Estructura del proyecto
```
secure-todo-app/
├── .github/workflows/
│   └── pipeline.yml          # Pipeline CI/CD (Testing & Linting automatizado)
├── app/
│   ├── static/               # Activos estáticos
│   │   ├── css/              # Estilos procesados (output.css)
│   │   ├── fonts/            # Tipografías locales (Inter, etc.)
│   │   ├── js/               # Lógica de cliente (tasks.js)
│   │   └── src/              # Archivos fuente de Tailwind (input.css)
│   ├── templates/            # Vistas HTML (Diseño Industrial/Earth Tone)
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── tasks.html
│   ├── tests/                # Suite de pruebas de seguridad
│   │   ├── conftest.py       # Configuración de fixtures de Pytest
│   │   ├── test_auth.py      # Pruebas de vectores de autenticación
│   │   ├── test_rate_limit.py# Verificación de protección contra fuerza bruta
│   │   └── test_security.py  # Tests de cabeceras y protección OWASP
│   ├── app.py                # Punto de entrada y configuración de Flask
│   ├── auth.py               # Blueprint de Autenticación y Lógica de Sesión
│   ├── forms.py              # Definición de formularios seguros (Flask-WTF)
│   ├── models.py             # Esquema de DB (SQLAlchemy)
│   ├── tasks.py              # Blueprint de gestión de activos (Tareas)
│   ├── tailwind.config.js    # Configuración de diseño y paleta de colores
│   ├── requirements.txt      # Dependencias del stack de seguridad
│   └── Dockerfile            # Definición de contenedor para la aplicación
├── nginx/
│   ├── default.conf          # Configuración de Hardening de Proxy Inverso
│   ├── selfsigned.crt        # Certificado SSL (Transport Layer Security)
│   └── selfsigned.key        # Llave privada del certificado
├── .env                      # Variables de entorno críticas (Secret Keys, DB URLs)
├── .gitignore                # Exclusión de activos sensibles del versionado
├── docker-compose.yml        # Orquestación de servicios (App + Nginx)
└── README.md                 # Documentación técnica del sistema
```


##  Enfoque de seguridad

El proyecto está diseñado teniendo en cuenta principios básicos de seguridad:

- Hash de contraseñas (nunca en texto plano)
- Separación de servicios
- Variables sensibles gestionadas mediante entorno
- Control de acceso por roles (usuario / administrador)
- Protección frente a accesos no autorizados
- Pruebas unitarias enfocadas a autenticación y permisos


##  Security Testing & Evidence

Para validar la seguridad de la aplicación, se han realizado las siguientes pruebas:

### 1. Validación de Cabeceras (Hardening)
Se ha verificado mediante `curl -I https://localhost` que el servidor responde con las cabeceras de seguridad configuradas:
- `Strict-Transport-Security`: Activo.
- `Content-Security-Policy`: Restrictiva.

### 2. Prueba de Resiliencia CSRF
Intentos de realizar peticiones `POST` (como creación de tareas) desde herramientas externas sin el token `csrf_token` resultan en un código de estado `400 Bad Request`.

### 3. Aislamiento de Red
Se ha comprobado mediante escaneo de puertos que el puerto **5000 (Flask)** y el **3306 (MySQL)** son inaccesibles desde el exterior de la red Docker, reduciendo la superficie de ataque solo al puerto **443 (Nginx)**.


##  Pruebas

Se incluirán pruebas unitarias con **pytest**, enfocadas principalmente en:

- Login correcto e incorrecto
- Acceso no autorizado a rutas protegidas
- Control de permisos entre usuarios y administrador

##  Cumplimiento de Seguridad (OWASP Top 10:2025)

Este ecosistema ha sido diseñado y auditado bajo los estándares de **OWASP**, implementando controles técnicos específicos para mitigar las amenazas más críticas identificadas en el panorama de ciberseguridad actual (2025-2026).

| Categoría | Implementación Técnica en Secure ToDo | Archivos Relacionados |
| :--- | :--- | :--- |
| **A01:2025-Broken Access Control** | Control de acceso basado en roles (**RBAC**) y aislamiento de objetos. Se verifica que un usuario solo pueda operar sobre su propio `user_id`. | `app/tasks.py`, `app/models.py` |
| **A02:2025-Cryptographic Failures** | Implementación de **BCrypt** para el salting/hashing de credenciales. Tráfico cifrado mediante **TLS 1.3** configurado en el proxy inverso. | `app/auth.py`, `nginx/default.conf` |
| **A03:2025-Injection** | Uso de **SQLAlchemy ORM** para consultas parametrizadas. Sanitización estricta de entradas para evitar SQLi y XSS persistente. | `app/forms.py`, `app/models.py` |
| **A04:2025-Insecure Design** | Arquitectura de "Privilegio Mínimo". Los flujos de autenticación y recuperación siguen patrones de diseño seguro desde la base. | `app/app.py` |
| **A05:2025-Security Misconfiguration** | Hardening de cabeceras de seguridad (**HSTS, X-Frame-Options, CSP**). Despliegue en contenedores Docker con usuarios no-root. | `nginx/default.conf`, `Dockerfile` |
| **A06:2025-Vulnerable and Outdated Components** | Gestión centralizada de dependencias y escaneo de vulnerabilidades en la cadena de suministro mediante el pipeline de CI/CD. | `requirements.txt`, `pipeline.yml` |
| **A07:2025-Identification and Authentication Failures** | Protección contra fuerza bruta mediante **Rate Limiting**. Cookies de sesión con flags `HttpOnly`, `Secure` y `SameSite`. | `app/app.py`, `app/auth.py` |
| **A08:2025-Software and Data Integrity Failures** | Validación de integridad en el despliegue. Protección contra ataques de des-serialización y uso de tokens **CSRF** en formularios. | `app/forms.py`, `pipeline.yml` |
| **A09:2025-Security Logging and Monitoring Failures** | Registro estructurado de eventos de autenticación y errores críticos para facilitar la auditoría y respuesta ante incidentes. | `app/app.py` |
| **A10:2025-Server-Side Request Forgery (SSRF)** | Restricción de red a nivel de Docker-Compose y validación de peticiones salientes para proteger la infraestructura interna. | `docker-compose.yml` |

---

##  Estándar de Verificación de Seguridad (OWASP ASVS 5.0)

Este proyecto ha sido desarrollado bajo los controles del **ASVS 5.0 (Nivel 1 y 2)**, garantizando una defensa en profundidad mediante la verificación técnica de los siguientes dominios:

| Categoría | Requisitos Verificados (L1/L2) | Implementación en Secure ToDo |
| :--- | :--- | :--- |
| **V1: Arquitectura** | Seguridad por diseño y modelado de amenazas. | Arquitectura segregada (Proxy + App + DB) mediante Docker. |
| **V2: Autenticación** | Gestión de contraseñas y antifuerza bruta. | Hashing BCrypt, políticas de longitud mínima y Flask-Limiter. |
| **V3: Gestión de Sesión** | Atributos de cookies y tiempos de expiración. | Cookies con flags `Secure`, `HttpOnly` y `SameSite=Lax`. |
| **V4: Control de Acceso** | Principio de privilegio mínimo y denegación por defecto. | Verificación de propiedad de recursos en cada endpoint (`user_id`). |
| **V5: Validación e Inyección** | Sanitización de entradas y parametrización de queries. | Uso estricto de **Flask-WTF** y **SQLAlchemy ORM**. |
| **V6: Criptografía Estática** | Almacenamiento seguro de secretos y hashes. | Protección de claves privadas en `.env` (no versionado). |
| **V7: Registro y Errores** | Prevención de fuga de info en errores y logs de auditoría. | Páginas de error personalizadas y logs de eventos críticos. |
| **V8: Protección de Datos** | Protección de datos sensibles en tránsito y memoria. | Eliminación de buffers innecesarios y uso de TLS 1.3. |
| **V9: Comunicaciones** | Configuración segura de TLS y cabeceras HTTP. | Hardening en Nginx (HSTS, CSP, X-Content-Type-Options). |
| **V14: Configuración** | Endurecimiento de la plataforma y dependencias. | Ejecución en Docker con usuario no-root y escaneo de SBOM. |

##  Autor

Proyecto desarrollado por Jorge Vázquez Espinosa, estudiante de ciberseguridad.
