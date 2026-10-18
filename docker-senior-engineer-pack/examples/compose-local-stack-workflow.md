# Worked example: a local stack that starts in the right order

Synthetic scenario for the `build-compose-environment` prompt and the compose-environments skill.

## Problem

A web API, PostgreSQL and Redis run from a `docker-compose.yml` with `version: "3.8"`. The API crashes on first start because PostgreSQL is not ready; developers restart it by hand. The database password is a literal in `environment`, PostgreSQL is published on `0.0.0.0:5432`, and the API's source is bind-mounted including `node_modules`, which breaks native modules built on macOS.

## Discovery

`docker compose version` shows a release that supports `include`, `watch` and `depends_on.required`. The real invocation is `docker compose up` from the repository root with an untracked `.env`. `docker compose config --quiet` succeeds; the rendered config is not pasted because it contains the password.

## Changes

- Rename to `compose.yaml` and remove the `version` key.
- PostgreSQL healthcheck with `pg_isready`, with `start_period` covering initialisation; a `migrate` one-shot service that runs the API image's migration command; the API depends on `db: service_healthy` and `migrate: service_completed_successfully`. The API keeps its own connection retries, because ordering only applies at startup.
- The password moves to a top-level secret from `./secrets/db_password.txt` (ignored by git); PostgreSQL reads `POSTGRES_PASSWORD_FILE` and the API reads `DATABASE_PASSWORD_FILE`. `.env.example` documents the remaining variables, with `${API_PORT:-8080}` defaults and `${JWT_ISSUER:?set JWT_ISSUER}` for a required one.
- Ports: the API on `127.0.0.1:${API_PORT:-8080}:8080`; PostgreSQL and Redis are no longer published, and an `admin` profile adds a database UI bound to 127.0.0.1 only when asked for.
- Development loop: `build.target: dev` and `develop.watch` with `sync` for `src/` and `rebuild` on lockfile changes, instead of bind-mounting the whole tree.
- Data in a named volume `db-data`, which `docker compose down` keeps.

## Validation

- `docker compose config --quiet` passes with the same env file.
- `docker compose -p task-stack up --wait` returns once all services are healthy; `docker compose -p task-stack ps` shows them healthy and `migrate` exited 0.
- `docker compose -p task-stack exec api` runs a one-line database query successfully.
- `docker compose -p task-stack down -v` removes only the task project, including its own volume. The developers' existing project and its `db-data` volume are untouched.

## Report

Migration note for developers: the old project's volume is not reused automatically because the project name and file changed; moving existing local data is their choice, and deleting the old volume is left to them.
