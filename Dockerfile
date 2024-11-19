# Use uma imagem base Python oficial
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /usr/src/app

# Copia os arquivos do projeto para o container
COPY api.py ./
COPY requirements.txt ./

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar o script
CMD ["python", "./api.py"]
