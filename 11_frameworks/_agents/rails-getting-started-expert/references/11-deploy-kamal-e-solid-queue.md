# 11 - Deploy with Kamal and Solid Queue (RGS p.68-70)

## Kamal (RGS p.68-70)
A deploy tool that ships with Rails; it uses Docker containers and deploys with zero downtime (p.68). The production-ready Dockerfile is used by Kamal to build the image; it uses **Thruster** to compress and serve assets (p.68).

Listed requirements (p.68): an Ubuntu LTS server with 1 GB of RAM or more (Hetzner, DigitalOcean etc.); a Docker Hub account and token; a Docker Hub repository named "store".

Steps (p.68-70):
1. In `config/deploy.yml`, replace `192.168.0.1` with the server IP and `your-user` with the Docker Hub user (`service: store`, `image: your-user/store`, `servers: web:`, `registry: username:`) (p.68-69).
2. Optional: under `proxy:` use `ssl: true` and `host: app.example.com`; DNS must point to the server and Kamal uses **LetsEncrypt** for the certificate (p.69).
3. Create an access token on Docker with read and write permission; export it: `export KAMAL_REGISTRY_PASSWORD=your-access-token` (p.69).
4. `bin/kamal setup` configures the server and performs the first deploy (p.69).
5. New deploys: `bin/kamal deploy` (p.70).
6. User in production: `bin/kamal console` and `User.create!(...)` (p.70).

Operational security [inference from p.69]: the token is a secret; the guide exports it as an environment variable and the `.kamal/` folder holds secrets and hooks (p.4). The agent never asks the user for the real token and does not repeat it in replies.

## Solid Queue and Active Job (RGS p.70)
Background jobs run in a separate process so they do not block the user experience (p.70). In development the adapter is `:async` (pending jobs stay in memory and are lost on restart) (p.70). In production Rails uses `solid_queue`, which stores jobs in the database and runs them in a separate process (p.70). With Kamal deploys, the variable `SOLID_QUEUE_IN_PUMA: true` in `config/deploy.yml` makes Puma start/stop Solid Queue (p.70). With `deliver_later`, emails go through Active Job, with automatic retry on failure and jobs preserved across restarts (p.70).

## [DATED]
Requirements (Ubuntu LTS, 1 GB), Docker Hub, Thruster, LetsEncrypt and the cited flags hold for the PDF (Rails 8.1.x). Current values may have changed: check the current Kamal documentation.

## Limits
NOT COVERED: multiple servers/roles, a production database beyond the default, `accessories`, Kamal rollback, other registries (the `deploy.yml` comment merely mentions DigitalOcean/ghcr.io, p.69), production environment variables beyond those shown. Docker/DNS in depth: devops agents.
