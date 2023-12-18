# Select Docker python image from Docker registry
FROM python:3.7-alpine 

# Select file called 'app' as the docker working directory
WORKDIR /app

# Copy all contents of file 'app' into the docker working directory
COPY . /app

# Copy the .env file into the docker working directory
COPY .env .env

# Install build dependencies
RUN apk --no-cache add build-base libffi-dev openssl-dev

# Installing dependencies 
RUN pip install -r requirements.txt

# Port which app will be run on
EXPOSE 5000

# Terminal commands run to deploy app
CMD ["sh", "-c", "cd app/ && python app.py"]