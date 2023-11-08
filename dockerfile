# Usar a imagem base oficial do Python
FROM python:3.12.0

# Definir o diretório de trabalho dentro do container para /app
WORKDIR /app

# Copiar o arquivo de requisitos primeiro para aproveitar o cache das camadas do Docker
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto dos arquivos do projeto para o diretório de trabalho dentro do container
COPY . .

# Expõe a porta 5000 para que possa ser acessada de fora do container
EXPOSE 5000

# Definir variáveis de ambiente para o modo de produção
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Usar o Gunicorn para rodar a aplicação em produção
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

