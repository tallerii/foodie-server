# foodie-server

[![Build Status](https://travis-ci.org/tallerii/foodie-server.svg?branch=master)](https://travis-ci.org/tallerii/foodie-server)
[![Coverage Status](https://coveralls.io/repos/github/tallerii/foodie-server/badge.svg?branch=master)](https://coveralls.io/github/tallerii/foodie-server?branch=master)

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Estructura de la aplicacion

La aplicacion esta dividida en tres grandes modulos:

- **foodie.users**: Contiene toda la logica de usuarios, incluyendo los tres tipos de usuario: staff, cliente y delivery.

- **foodie.orders**: Contiene toda la logica para realizar y asignar pedidos.

- **foodie.reputation**: Contiene la logica para realizar reviews de los pedidos ya realizados.
