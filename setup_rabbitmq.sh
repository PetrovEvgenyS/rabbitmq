#!/bin/bash

### ЦВЕТА ##
ESC=$(printf '\033') RESET="${ESC}[0m" MAGENTA="${ESC}[35m" RED="${ESC}[31m" GREEN="${ESC}[32m"

### Функции цветного вывода ##
magentaprint() { echo; printf "${MAGENTA}%s${RESET}\n" "$1"; }
errorprint() { echo; printf "${RED}%s${RESET}\n" "$1"; }
greenprint() { echo; printf "${GREEN}%s${RESET}\n" "$1"; }


# --------------------------------------------------------


# Проверка запуска через sudo
if [ -z "$SUDO_USER" ]; then
    errorprint "Пожалуйста, запустите скрипт через sudo."
    exit 1
fi

# Функция для установки RabbitMQ на Ubuntu
install_rabbitmq_ubuntu() {  

    magentaprint "Установка зависимостей"
    apt install -y curl gnupg apt-transport-https
    
    magentaprint "Добавление ключа репозитория RabbitMQ"
    curl -fsSL https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey | apt-key add -
    
    magentaprint "Добавление репозитория RabbitMQ"  
    tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
deb https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ $(lsb_release -cs) main
EOF
    
    magentaprint "Обновление списка пакетов"
    apt update
    
    magentaprint "Установка RabbitMQ"
    apt install -y rabbitmq-server

    magentaprint "Запуск и включение в автозагрузку RabbitMQ"
    systemctl enable --now rabbitmq-server

    magentaprint "Проверка статуса RabbitMQ"
    systemctl status rabbitmq-server --no-pager
}

# Функция для установки RabbitMQ на AlmaLinux
install_rabbitmq_almalinux() {

    magentaprint "Установка зависимостей"
    dnf install -y epel-release

    magentaprint "Установка Erlang"    
    dnf install -y erlang
    
    magentaprint "Добавление репозитория RabbitMQ"  
    tee /etc/yum.repos.d/rabbitmq.repo <<EOF
[rabbitmq]
name=RabbitMQ Repository
baseurl=https://packagecloud.io/rabbitmq/rabbitmq-server/el/7/\$basearch
gpgcheck=1
gpgkey=https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey
enabled=1
EOF
    
    magentaprint "Установка RabbitMQ"
    dnf install -y rabbitmq-server
    
    magentaprint "Запуск и включение в автозагрузку RabbitMQ"
    systemctl enable --now rabbitmq-server

    magentaprint "Проверка статуса RabbitMQ"
    systemctl status rabbitmq-server --no-pager
}

# Определение дистрибутива и вызов соответствующей функции
if [ -f /etc/lsb-release ]; then
    install_rabbitmq_ubuntu
elif [ -f /etc/redhat-release ]; then
    install_rabbitmq_almalinux
else
    errorprint "Неподдерживаемая операционная система для установки."
    exit 1
fi
