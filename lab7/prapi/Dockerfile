# Using lightweight alpine image
FROM 3.7.7-alpine3.10
# Defining working directory and copy the requriments file
WORKDIR /usr/src/myapp
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3","app.py"]