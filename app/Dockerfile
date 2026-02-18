# Descargar y ejecutar Tailwind Standalone
FROM debian:bookworm-slim AS builder
WORKDIR /build

# Instalamos curl para bajar el binario
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Descargamos el binario oficial de Tailwind
RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64 && \
    chmod +x tailwindcss-linux-x64 && \
    mv tailwindcss-linux-x64 /usr/local/bin/tailwindcss

# Copiamos los archivos
COPY tailwind.config.js .
COPY templates ./templates
COPY static/src ./static/src

# Generamos el CSS con Tailwind
RUN tailwindcss -i ./static/src/input.css -o ./static/css/output.css --minify

# Python
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Copiamos el CSS generado en la etapa anterior
COPY --from=builder /build/static/css/output.css ./static/css/output.css

ENV FLASK_ENV=production
CMD ["python", "-m", "app"]