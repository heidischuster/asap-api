# Start from the official Python base image.
FROM python:3.9 as base

#Set the current working directory to /backend.
WORKDIR /backend

#Copy the file with the requirements to the /backend directory.
COPY ./requirements.txt /backend/requirements.txt

#Install the package dependencies in the requirements file.
# Original this was using poetry but the latest version has some depency conflicts with FastAPI
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

#Copy the ./app directory inside the /code directory.
COPY . /backend

#Set the command to run the uvicorn server.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
