# NuxGame API Test Task

## First install Docker and Docker Compose

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)

## Very fast start
 -  **Linux:**
    ```bash
    git clone https://github.com/whoisn3kk/nuxgame-test-task.git &&
    cd nuxgame-test-task &&
    mv .env.example .env &&
    docker-compose up --build -d
    ```

 -  **Windows CMD:**
    ```bash
    git clone https://github.com/whoisn3kk/nuxgame-test-task.git && cd nuxgame-test-task && move .env.example .env && docker-compose up --build -d
    ```

 -  **Windows PowerShell:**
    ```bash
    git clone https://github.com/whoisn3kk/nuxgame-test-task.git; cd nuxgame-test-task; mv .env.example .env; docker-compose up --build -d
    ```

    [`Go to Description and Test`](#dev)


## Fast start

1.  **Clone repo:**
    ```bash
    git clone https://github.com/whoisn3kk/nuxgame-test-task.git
    cd nuxgame-test-task
    ```

2.  **Change `.env` file:**
    Remove `.example` from `.env.example` file and fill fields with correct values:
    ```ini
    SECRET_KEY='your-super-secret-key'
    DEBUG=1
    ```

3.  **Run project:**
    Execute docker compose command to build project:
    ```bash
    docker-compose up --build -d
    ```

<h2 id="dev"> Description and Test </h2>

Server avaliable at `http://localhost:8081`.

> If you are using Windows PowerShell, please use `curl.exe` instead of plain `curl` command.

### 1. User registration
`POST /user/register`
**Body:**
```json
{
    "username": "user",
    "phone_number": "+380440001122"
}
```
**Example `curl`:**
```bash
curl -X POST http://localhost:8081/user/register \
-H "Content-Type: application/json" \
-d '{"username": "user", "phone_number": "+380440001122"}'
```

> next replace `00000000-dead-0bad-babe-ca1109110000` with received `token`

### 2. Retrieve user info
`GET /game/{token}`
**Example `curl`:**
```bash
curl http://localhost:8081/game/00000000-dead-0bad-babe-ca1109110000
```

### 3. Game
`POST /game/{token}/play`
**Example `curl`:**
```bash
curl -X POST http://localhost:8081/game/00000000-dead-0bad-babe-ca1109110000/play
```

### 4. Історія ігор
`GET /game/{token}/history`
**Example `curl`:**
```bash
curl http://localhost:8081/game/00000000-dead-0bad-babe-ca1109110000/history
```

### 5. Update token
`POST /game/{token}/renew`
**Example `curl`:**
```bash
curl -X POST http://localhost:8081/game/00000000-dead-0bad-babe-ca1109110000/renew
```

### 6. Deactivate token
`POST /game/{token}/deactivate`
**Example `curl`:**
```bash
curl -X POST http://localhost:8081/game/00000000-dead-0bad-babe-ca1109110000/deactivate
```