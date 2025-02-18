# onai_tech_task

## Overview

This project is a FastAPI-based application that processes webhook requests and interacts with OpenAI's GPT model to generate responses. The application also includes a chat history feature to store and retrieve chat messages.

## Features

- **Webhook Processing**: Handles incoming webhook requests, processes messages using OpenAI's GPT model, and sends responses to a callback URL.
- **Chat History**: Stores chat messages in a PostgreSQL database and provides endpoints to manage chat histories.
- **Rate Limiting**: Implements rate limiting using SlowAPI to prevent abuse of the API.
- **Task Queue**: Uses Redis and RQ (Redis Queue) to handle background tasks for processing webhook requests.

## Project Structure

```
.
├── alembic
│   ├── versions
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── app
│   ├── core
│   │   ├── crud
│   │   ├── models
│   │   ├── schemas
│   ├── routers
│   ├── services
│   ├── db.py
│   ├── config.py
│   └── main.py
├── tests
│   ├── test_crud.py
│   ├── test_models.py
│   └── conftest.py
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/onai_tech_task.git
cd onai_tech_task
```

2. Create a `.env` file in the root directory with the following content:

```sh
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://postgres:postgres@db/postgres
REDIS_URL=redis://redis:6379/0
```

3. Build and start the Docker containers:

```sh
docker-compose up --build
```

4. Apply the database migrations:

```sh
docker-compose exec web alembic upgrade head
```

## Running the Application

The application will be available at [http://localhost:8000](http://localhost:8000).

## API Endpoints

### Webhook Request
- `POST /webhook`: Handles incoming webhook requests and processes messages using OpenAI's GPT model.

### Chat Histories
- `GET /chat_histories`: Retrieve all chat histories.
- `GET /chat_histories/{chat_history_id}`: Retrieve a specific chat history by ID.
- `POST /chat_histories`: Create a new chat history.
- `PUT /chat_histories/{chat_history_id}`: Update an existing chat history.
- `DELETE /chat_histories/{chat_history_id}`: Delete a chat history by ID.

## Running Tests

To run the tests, use the following command:

```sh
docker-compose exec web pytest
```

## Acknowledgements

This project was built using:

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://openai.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Redis](https://redis.io/)
- [RQ (Redis Queue)](https://python-rq.org/)
- [SlowAPI](https://pypi.org/project/slowapi/)