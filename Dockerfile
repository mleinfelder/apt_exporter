# Use uma imagem base com Python
FROM python:3.8

# Instale as dependências
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y debian-goodies

# Defina o diretório de trabalho
WORKDIR /app

# Copie o script Python para o contêiner
COPY prometheus_exporter.py .

# Exponha a porta 9091
EXPOSE 9091

# Comando para iniciar o exporter
CMD ["/usr/bin/python3", "prometheus_exporter.py"]
