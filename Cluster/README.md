# Кластер RabbitMQ: запуск через Docker Compose

## Описание

Этот проект предназначен для быстрого развертывания кластера RabbitMQ из трёх узлов с помощью Docker Compose. Параметры конфигурации вынесены в файл `.env` для удобства настройки и безопасности.

---

## Структура файлов

### `.env`

Файл `.env` содержит переменные окружения, используемые в `docker-compose.yml`.  
**Не рекомендуется** добавлять этот файл в репозиторий, чтобы не раскрывать чувствительные данные. Данный файл - пример. 

**Пример содержимого:**
```
RABBITMQ_IMAGE=rabbitmq:4-management
RABBITMQ_DEFAULT_USER=rmuser
RABBITMQ_DEFAULT_PASS=rmpass
RABBITMQ_ERLANG_COOKIE=sgeRr3EC4sheFs2Ee2s
RABBITMQ_DISK_LIMIT=2147483648
```

**Пояснения к переменным:**
- `RABBITMQ_IMAGE` — образ RabbitMQ с web-интерфейсом.
- `RABBITMQ_DEFAULT_USER` и `RABBITMQ_DEFAULT_PASS` — логин и пароль по умолчанию для доступа к RabbitMQ.
- `RABBITMQ_ERLANG_COOKIE` — секретный ключ для объединения узлов в кластер.
- `RABBITMQ_DISK_LIMIT` — лимит свободного места на диске (в байтах), при достижении которого RabbitMQ перестанет принимать сообщения.

---

### `docker-compose.yml`

Файл описывает три сервиса (узла RabbitMQ), каждый из которых:
- Использует параметры из `.env`
- Имеет уникальное имя контейнера и hostname
- Пробрасывает уникальный порт для web-интерфейса (15672, 15673, 15674)
- Хранит данные в отдельной папке (`./rabbitmq-1`, `./rabbitmq-2`, `./rabbitmq-3`)
- Объединён в одну сеть `rabbitmq_cluster` для взаимодействия между узлами

**Основные параметры:**
- `environment` — переменные окружения для каждого контейнера (см. выше)
- `ports` — проброс портов для доступа к web-интерфейсу каждого узла
- `volumes` — монтирование локальных папок для хранения данных RabbitMQ
- `networks` — объединение контейнеров в одну сеть для кластера

---

## Запуск кластера

1. **Создайте и настройте файл `.env`** (можно скопировать из примера выше).
2. **Запустите кластер:**
   ```
   docker-compose --env-file .env up -d
   ```
3. **Доступ к web-интерфейсу:**
   - Первый узел: [http://localhost:15672](http://localhost:15672)
   - Второй узел: [http://localhost:15673](http://localhost:15673)
   - Третий узел: [http://localhost:15674](http://localhost:15674)
   - Логин и пароль — из `.env` (`RABBITMQ_DEFAULT_USER` / `RABBITMQ_DEFAULT_PASS`)

4. **Добавление ноды в кластер**
   - В Web-интерфейсе обращаем внимание только на поле `Cluster: rabbit@rabbitmq1` - именно по этому имени мы будем дальше подключать ноды.
   Далее надо зайти в контейнеры (`rabbitmq2` и `rabbitmq3`) и выполнить следующие команды:
   ```bash
   docker-compose exec rabbitmq2 bash
   rabbitmqctl stop_app
   rabbitmqctl reset
   rabbitmqctl join_cluster rabbit@rabbitmq-01
   rabbitmqctl start_app
   ```
   На первой ноде никаких действий не требуется! Также мы увидим пачку `warning - про depricated` метод передачи COOKIE, игнорируем.

   Одной командой можно выполнить указанные действия так:
   ```bash
   HOST=rabbitmq2; docker-compose exec $HOST rabbitmqctl stop_app && docker-compose exec $HOST rabbitmqctl reset && docker-compose exec $HOST rabbitmqctl join_cluster rabbit@rabbitmq-01 && docker-compose exec $HOST rabbitmqctl start_app
   ```

   ```bash
   HOST=rabbitmq3; docker-compose exec $HOST rabbitmqctl stop_app && docker-compose exec $HOST rabbitmqctl reset && docker-compose exec $HOST rabbitmqctl join_cluster rabbit@rabbitmq-01 && docker-compose exec $HOST rabbitmqctl start_app
   ```
   Заходим в интерфейс 1 ноды, проверяем добавление нод в кластер. На этом сборка кластера завершена.

### Удаление ноды из кластера

   Чтобы убрать ноду из кластера, выполняем команды:
   ```bash
   docker-compose exec rabbitmq3 bash
   rabbitmqctl stop_app
   rabbitmqctl reset
   rabbitmqctl start_app
   ```
   Нода `rabbitmq3` удалена из кластера.

### **Quorum queue**

   Можно создать очередь с типом `Quorum` на любой ноде и она сразу станет отказоустойчивой, данная очередь будет на каждой ноде в кластере.