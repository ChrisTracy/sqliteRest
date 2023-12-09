# sqliteRest
This project is a simple Fast API endpoint that sits directly on top of a sqlite database file. In its current capacity, items can only be read from the database.

## Examples
Use the table name in the route and then define all queries after the '?'. Every column in the database can be queried and wilcards (*) are allowed.
```http
GET /api/{table_name}?field1=value*&field2=value2
```
By defualt, the api only returns fields that are not empty. If you want to return all fields, use the all_fields parameter.
```http
GET /api/{table_name}?field1=value&field2=value2&all_fields=true
```

## Quick Setup

1. Install Docker and Docker-Compose

- [Docker Install documentation](https://docs.docker.com/install/)
- [Docker-Compose Install documentation](https://docs.docker.com/compose/install/)

2. Create a docker-compose.yml file:

```yml
version: '3'

services:
  sqliterest:
    image: christracy/sqliterest
    volumes:
      - /path/to/database:/databases
```

3. Bring up your stack by running

```bash
docker-compose up -d

# If using docker-compose-plugin
docker compose up -d

```
