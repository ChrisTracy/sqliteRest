# sqliteRest

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
