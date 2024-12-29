# FASTAPI Basic Auth + PostgreSQL + JWT

Create Postgres container :
```bash
docker run --name postgres-outer-wilds -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=outer-wilds-db -p 5432:5432 postgres:17.2
```

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

```bash
fastapi dev
```