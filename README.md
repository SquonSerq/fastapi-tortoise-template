# FastAPI + Tortoise ORM template

## Application start

### Install dependencies:
```
python -m venv .venv
source .venv/bin/activate
poetry install
```

### Template start via docker:
```
make build
make start_db
make start_dev
```

### Template stop via docker:

`make stop`

### Template start locally:

`uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload`

### Supported local commands:

Init DB: `make initdb`

Create migrations: `make makemigrations`

Apply migrations: `make migrate`

## Project access:

Go to [https://localhost:5000/](https://localhost:5000/) to access FastAPI swagger.

## Template status:

I am open for suggestions/reports in issues on Github.

I am sure that template needs some tuning but should work from the box already.

**NOT READY FOR PRODUCTION.** If you want to use this template in production you need to tune it yourself for your needs.

## TODO:

- [ ] Add tests templates with pytest
