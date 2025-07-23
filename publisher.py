import pika     # Импортир библиотеки для работы с RabbitMQ
import time     # Импортируем модуль для работы с задержками

# Переменные для подключения.
rabbitmq_host = '10.100.10.1'             # Хост RabbitMQ (по умолчанию localhost).
rabbitmq_port = 5672                      # Порт RabbitMQ (по умолчанию 5672).
rabbitmq_user = 'publisher_user'          # Учетные данные для доступа.
rabbitmq_password = 'pubpass'             # Учетные данные для доступа.
rabbitmq_queue = 't_queue'                # Очередь.
rabbitmq_exchange = 't_exchange'          # Обменник.
rabbitmq_routing_key = 't_routing_key'    # Ключ маршрутизации.
rabbitmq_virtual_host = '/'               # Виртуальный хост (по умолчанию '/').

# Устанавливаем параметры подключения.
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection_params = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    credentials=credentials,
    virtual_host=rabbitmq_virtual_host
)

# Установка соединения.
connection = pika.BlockingConnection(connection_params)
# Создание канала
channel = connection.channel()

# Объявляем обменник. Создает обменник, если он еще не существует.
channel.exchange_declare(
    exchange=rabbitmq_exchange,  # Имя обменника.
    exchange_type='direct',      # Тип обменника.
    durable=True                 # Сохранение данных после перезапуска RabbitMQ.
)

# Объявляем очередь. Создает очередь, если она еще не существует.
channel.queue_declare(
    queue=rabbitmq_queue,        # Имя очереди.
    durable=True                 # Сохранение данных после перезапуска RabbitMQ.
)

# Связываем очередь с обменником, указывая, как маршрутизировать сообщения.
channel.queue_bind(
    exchange=rabbitmq_exchange,          # Имя обменника.
    queue=rabbitmq_queue,                # Имя очереди.
    routing_key=rabbitmq_routing_key     # Ключ маршрутизации.
)

# Отправляем 10 сообщений с уникальным номером.
for i in range(1, 11):
    message = f"Hello, RabbitMQ! Message number {i}"  # Объявляем переменную, хранящую текст сообщения.
    channel.basic_publish(
        exchange=rabbitmq_exchange,          # Имя обменника.
        routing_key=rabbitmq_routing_key,    # Ключ маршрутизации.
        body=message,                        # Текст сообщения.
        properties=pika.BasicProperties(
            delivery_mode=2     # Указывает, что сообщение нужно сохранить на диск (2 — устойчивое сообщение).
        )
    )
    print(f"Сообщение '{message}' отправлено через обменник '{rabbitmq_exchange}' в очередь '{rabbitmq_queue}'.")
    time.sleep(0.5)  # Задержка 500 миллисекунд (0.5 секунды)

# Закрываем соединение.
connection.close()
