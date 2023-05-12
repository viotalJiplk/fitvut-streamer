# VUT FIT video records downloader
This project is based on *nginx:alpine* so it is not going to run on Windows.

What it does? It periodicaly downloads last x streams from specified course.
## How to run the project
1. Install **Docker**
2. Clone this repository
3. Rename .env_template -> .env `cp .env_template .env`
4. Put proper values to .env file
5. Run `docker compose up -d`

The application is going to run on the adress `http://localhost:port`.