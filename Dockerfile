# Imagen base
FROM python:3.10

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos al contenedor
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto si tu app lo usa (ajústalo según tu proyecto)
EXPOSE 7860

# Comando de inicio
CMD ["python", "src/main.py"]
