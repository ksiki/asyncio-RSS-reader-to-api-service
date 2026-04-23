# asyncio-RSS-reader-to-api-service

Asynchronous reading of several RSS feeds at once and uploading them to the database. Through the FastAPI service, you can get all the news from different sources, filtered by many parameters.

## How it works

- The client sends a POST request.
- api-service — throws a message to RabbitMQ.
- RabbitMQ — just keeps a queue of messages while the reader is busy.
- rss-reader — performs parsing.
- Redis — this is where the worker saves the final result (a JSON report).
- api-service — when the client asks "is it ready?", the API will return the data.

## Technologies used

- **python**
- **asyncio**
- **fastapi**
- **redis**
- **rabbitmq**
- **docker compose**
- **poetry**
