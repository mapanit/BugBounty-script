BugBounty Environment Setup tools
<p align="center"> <img src="https://img.shields.io/badge/Python-3.6+-blue.svg" alt="Python"> <img src="https://img.shields.io/badge/Platform-Linux-lightgrey.svg" alt="Platform"> <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"> </p>
📋 Описание

BugBounty-tools — это автоматический скрипт для быстрого развертывания полноценного окружения для Bug Bounty и пентестинга. Он устанавливает и настраивает десятки популярных инструментов, создает структуру каталогов и готовит виртуальное окружение Python.

    ⚠️ ВАЖНО: Используйте установленные инструменты ТОЛЬКО в рамках законных и согласованных тестов (authorized testing / bug bounty программы). Несанкционированное использование может нарушать закон.

🚀 Быстрый старт
bash

# Клонирование репозитория
git clone https://github.com/yourusername/bugbounty-script.git
cd bugbounty-script

# Запуск скрипта
python3 main.py

📦 Что устанавливается
🔍 Разведка (Reconnaissance)

    theHarvester — сбор информации о доменах

    assetfinder, subfinder, amass, chaos-client — поиск поддоменов

    subzy — детект subdomain takeover

    waybackurls, gau — сбор исторических URL

    gowitness — массовые скриншоты хостов

    naabu — быстрый port scan

    dnsx — массовая DNS-резолюция

    hakrawler, katana — веб-краулинг

🛡️ Сканирование уязвимостей

    nuclei — темплейт-базированное сканирование

    nikto — веб-сканер

    Metasploit — фреймворк для эксплуатации (опционально)

    interactsh-client — OOB-сервер для слепых SSRF/XXE/RCE

    notify — пуш результатов в Slack/Discord/Telegram

🎯 CMS

    WPScan — сканер WordPress

    CMSeeK, droopescan — определение и анализ CMS

    wpprobe — быстрый WordPress-сканер

🔌 API / GraphQL

    graphql-cop — сканер уязвимостей GraphQL

    kiterunner — brute-force API-эндпоинтов по Swagger/OpenAPI

📊 Wordlists

    SecLists — коллекции словарей для брутфорса (опционально)

🔐 Анализ JavaScript & Secrets

    SecretFinder — поиск API-ключей в JS

    Pinkerton — анализ JS на уязвимости

    trufflehog, gitleaks — поиск credentials в коде

🚀 Fuzzing & Brute Force

    ffuf — быстрый HTTP fuzzer

    feroxbuster — перебор путей

    dirsearch — поиск скрытых папок

    Arjun, x8 — обнаружение скрытых HTTP-параметров

☁️ Cloud

    cloud_enum — enum S3/Azure/GCP по имени компании

    S3Scanner — поиск открытых S3-бакетов

    CloudBrute — enum облачных ресурсов

    Trivy — сканер уязвимостей контейнеров/IaC (опционально)

📱 Mobile (опционально)

    MobSF — статический + динамический анализ APK/IPA

    apktool, jadx — декомпиляция APK

📂 Структура каталогов
text

├── Web_catalog/          # Веб-каталоги и сканеры
├── Subdomains/           # Инструменты для поиска поддоменов
├── Scaner/               # Сканеры уязвимостей
├── CMS/                  # CMS-сканеры
├── SSRF/                 # SSRF-инструменты
├── Open_redirect/        # Open redirect сканеры
├── LFI/                  # LFI-инструменты
├── XSS/                  # XSS-сканеры
├── SSTI/                 # SSTI-инструменты
├── SQLj/                 # SQL-инъекции
├── JS/                   # JavaScript-анализ
├── Dorks/                # Dorks-инструменты
├── Reconnaissance/       # Разведка
├── Secrets/              # Поиск секретов
├── Nuclei_Templates/     # Шаблоны Nuclei
├── Wordlists/            # Словари
├── API_GraphQL/          # API/GraphQL инструменты
├── Cloud/                # Cloud-инструменты
└── Mobile/               # Mobile-инструменты (опционально)

🖥️ Поддерживаемые системы

    Debian/Ubuntu/Kali (apt)

    Fedora/RHEL (dnf/yum)

    Arch/Manjaro (pacman)

    openSUSE (zypper)

⚙️ Использование
Базовый запуск
bash

python3 main.py

Интерактивный режим

Скрипт автоматически определит пакетный менеджер и предложит установить опциональные компоненты.
Неинтерактивный режим
bash

# Установка всех опциональных компонентов
python3 main.py --non-interactive --install-seclists --install-metasploit --install-trivy --install-mobile-tools

Аргументы командной строки
Аргумент	Описание
--package-manager {apt,dnf,yum,pacman,zypper}	Явно указать пакетный менеджер
--venv-dir DIR	Имя каталога для виртуального окружения (по умолчанию: venv)
--skip-venv	Не создавать виртуальное окружение Python
--install-seclists	Установить SecLists без вопроса
--install-metasploit	Установить Metasploit без вопроса
--install-trivy	Установить Trivy без вопроса
--install-mobile-tools	Установить инструменты для мобильного пентеста
--non-interactive, -y	Не задавать вопросы; использовать флаги выше
🔧 Рекомендуемый workflow

    Разведка: theHarvester → subfinder → amass → chaos → assetfinder → httpx

    Проверка takeover: subzy

    Порты/DNS: naabu → dnsx

    Поиск секретов: SecretFinder → trufflehog → gitleaks

    Fuzzing/параметры: ffuf → feroxbuster → dirsearch → Arjun/x8 (с SecLists)

    Краулинг: katana / hakrawler → waybackurls / gau

    Сканирование: nuclei → nikto → graphql-cop (для API)

    Слепые уязвимости: interactsh-client (OOB для SSRF/XXE/RCE)

    Cloud: cloud_enum → S3Scanner

    Эксплуатация: Metasploit для известных уязвимостей

    Автоматизация уведомлений: notify (Slack/Discord/Telegram)

🐍 Виртуальное окружение

Скрипт автоматически создает виртуальное окружение Python для изоляции зависимостей:
bash

# Активация
source venv/bin/activate

# Деактивация
deactivate

📝 Примечания
Python 2 vs Python 3

Некоторые легаси-инструменты (например, tplmap, LFIscanner) написаны под Python 2 и несовместимы с Python 3. Для них рекомендуется использовать отдельное окружение с Python 2 или искать актуальные форки.
Сборка из исходников

    kiterunner собирается из исходников через Makefile (требует CGO + libzstd)

    CloudBrute требует ручной go build после клонирования

Docker для MobSF

MobSF рекомендуется запускать через Docker:
bash

docker pull opensecurity/mobile-security-framework-mobsf:latest

🛠️ Требования

    Linux (Debian/Ubuntu/Kali/Fedora/Arch/openSUSE)

    Python 3.6+

    sudo права или root-доступ

    Интернет-соединение

📄 Лицензия

MIT License
⚖️ Отказ от ответственности

Данный скрипт предназначен исключительно для образовательных целей и проведения авторизованных тестов на проникновение. Использование инструментов без явного разрешения владельца системы является незаконным. Автор не несет ответственности за неправомерное использование.
<p align="center"> <sub>Built with ❤️ for the security community</sub> </p>
