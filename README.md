# asap-api

## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).

## local development

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Now you can open your browser and interact with these URLs:

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

Static form page to validate the member id: https://localhost/member_id/validate

To check the logs, run:

```bash
docker-compose logs
```

There are two implementation for the member id. The first one I tested is a two-way encryption, which allows to
decode the id back into attribute values. To make 100% sure this system created the id there is a validation string attached.
But the generated ID are very long and ugly keys, so I changed it to a MD5 hash that has a defined format, e.g. xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.
There is a random number added to the values when hashing, which makes it almost 100% sure there will never be a duplicate id generated.

## Cloud deployment

The docker container is currently running in the Google cloud. It only has one instance to keep cost low. Google has a new UI with new
functionality to deploy docker containers.

The docs:

https://asap-qjb3pwf5ba-uc.a.run.app/doc

https://asap-qjb3pwf5ba-uc.a.run.app/redoc

And the same validation form:
https://asap-qjb3pwf5ba-uc.a.run.appvalidate

## Backend local development, additional details

You can also start the uvicorn app directly and it keeps checking for changes and restarting the app
```bash
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 80
```

### Backend tests

To test the backend run:

```console
sh ./scripts/test.sh
```
The file `./scripts/test.sh` has the commands to generate a docker container, start the stack and test it.

The tests run with Pytest, modify and add tests to `./backend/app/tests/`.

#### Test Coverage

Because the test scripts forward arguments to `pytest`, you can enable test coverage HTML report generation by passing `--cov-report=html`.

To run the local tests with coverage HTML reports:

```Bash
sh ./scripts/test-local.sh --cov-report=html
```




## Project generation and updating, or re-generating

This project was generated using https://github.com/tiangolo/full-stack-fastapi-postgresql with:

```bash
pip install cookiecutter
cookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql
```

But that created a lot more stuff than was necessary and so most of it was removed.
Anyway FastAPI seems really easy and convenient.
