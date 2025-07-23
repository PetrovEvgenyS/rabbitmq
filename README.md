# RabbitMQ: примеры запуска и работы

В этом репозитории собраны примеры для быстрого запуска RabbitMQ в Docker (одиночный контейнер и кластер), а также скрипт установки RabbitMQ на сервер и примеры кода для отправки/приёма сообщений.

## Структура репозитория

```
.
├── Cluster/                # Примеры запуска RabbitMQ-кластера через docker-compose
│   ├── .env
│   ├── README.md
│   └── docker-compose.yml
├── consumer.py             # Пример consumer на Python (читает сообщения из очереди)
├── docker-compose.yml      # Пример запуска одиночного контейнера RabbitMQ
├── publisher.py            # Пример publisher на Python (отправляет сообщения в очередь)
├── setup_rabbitmq.sh       # Bash-скрипт для установки RabbitMQ на Ubuntu/AlmaLinux
└── README.md               # Этот файл
```

## Быстрый старт

### 1. Одиночный контейнер RabbitMQ

Запуск RabbitMQ в Docker одной командой:
```
docker run -d \
    --name rmq \
    -p 15672:15672 \
    -p 5672:5672 \
    rabbitmq:4-management
```
- Web-интерфейс: http://localhost:15672  
- Логин/пароль по умолчанию: `guest` / `guest`

Или через docker-compose:
```
docker-compose up -d
```
(см. [docker-compose.yml](./docker-compose.yml))

### 2. Кластер RabbitMQ (3 узла)

В папке [Cluster](./Cluster) есть готовый пример для запуска кластера из 3 узлов через docker-compose.  
Подробности и инструкция — в [Cluster/README.md](./Cluster/README.md).

### 3. Скрипт установки RabbitMQ на сервер

Скрипт [setup_rabbitmq.sh](./setup_rabbitmq.sh) позволяет быстро установить RabbitMQ на Ubuntu или AlmaLinux.  
Запускать через `sudo`:
```
sudo ./setup_rabbitmq.sh
```

### 4. Примеры кода

- [publisher.py](./publisher.py) — пример отправки сообщений в очередь RabbitMQ на Python
- [consumer.py](./consumer.py) — пример получения сообщений из очереди RabbitMQ на Python
