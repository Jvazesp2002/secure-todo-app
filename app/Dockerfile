# --- ETAPA 1: Descargar y ejecutar Tailwind Standalone ---
FROM debian:bookworm-slim AS builder
WORKDIR /build

# Instalamos curl para bajar el binario
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Descargamos el binario oficial de Tailwind (arquitectura x64)
RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64 && \
    chmod +x tailwindcss-linux-x64 && \
    mv tailwindcss-linux-x64 /usr/local/bin/tailwindcss

# Copiamos tus archivos
COPY tailwind.config.js .
COPY templates ./templates
COPY static/src ./static/src

# Generamos el CSS (Sin npx, sin node_modules, sin problemas)
RUN tailwindcss -i ./static/src/input.css -o ./static/css/output.css --minify

# --- ETAPA 2: Python ---
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Traemos el CSS generado
COPY --from=builder /build/static/css/output.css ./static/css/output.css

ENV FLASK_ENV=production
CMD ["python", "-m", "app"]