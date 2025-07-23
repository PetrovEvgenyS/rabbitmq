import pika     # Импортир библиотеки для работы с RabbitMQ
import time     # Импортируем модуль для работы с задержками

# Настройки подключения.
rabbitmq_host = '10.100.10.1'   # Хост RabbitMQ (по умолчанию localhost).
rabbitmq_port = 5672            # Порт RabbitMQ (по умолчанию 5672).
rabbitmq_user = 'consumer_user' # Имя пользователя RabbitMQ.
rabbitmq_password = 'conpass'   # Пароль пользователя RabbitMQ.
rabbitmq_queue = 't_queue'      # Имя очереди, из которой нужно получать сообщения.

def callback(ch, method, properties, body):
    """
    Обработчик входящих сообщений.
    :param ch: канал, по которому пришло сообщение
    :param method: данные о доставке (delivery info)
    :param properties: свойства сообщения
    :param body: тело сообщения
    """
    message = body.decode()                 # Декодирование сообщения.
    print(f"Получено сообщение: {message}") # Вывод сообщения.
    
    # Записываем сообщение в файл databases.db.
    with open('/root/rabbitmq_compose/databases.db', 'a') as file:
        file.write(message + '\n')

    # Подтверждаем, что сообщение обработано.
    ch.basic_ack(delivery_tag=method.delivery_tag)

    # Добавляем задержку в 500 миллисекунд (0.5 секунды).
    time.sleep(0.5)

def main():
    # Устанавливаем подключение к RabbitMQ.
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Убеждаемся, что очередь существует.
    channel.queue_declare(queue=rabbitmq_queue, durable=True)

    # Начинаем потреблять сообщения из очереди.
    print(f"Ожидание сообщений из очереди '{rabbitmq_queue}'. Нажмите CTRL+C для выхода.")
    channel.basic_consume(
        queue=rabbitmq_queue,           # Имя очереди для чтения.
        on_message_callback=callback    # Функция-обработчик.
    )

    try:
        # Запускаем бесконечный цикл ожидания сообщений.
        channel.start_consuming()   # Запуск ожидания сообщений.
    except KeyboardInterrupt:
        print("Остановлено пользователем")
        channel.stop_consuming()

    # Закрываем соединение.
    connection.close()

if __name__ == '__main__':
    main()
