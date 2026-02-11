# Что делает `main.py`

`main.py` — это основной установочный и подготовительный скрипт проекта. Его задача — автоматически подготовить рабочее окружение для Bug Bounty / пентестинга и собрать полезные инструменты в упорядоченные папки.

Основные действия, выполняемые скриптом:

- Проверка ОС: скрипт проверяет, запущен ли он на Linux, и прерывает выполнение при отсутствии поддержки.
- Создание виртуального окружения Python (`venv`) и генерация инструкции по активации (`VENV_INSTRUCTIONS.txt`).
- Авто-определение пакетного менеджера Linux (`apt`, `dnf`, `yum`, `pacman`, `zypper`) с возможностью ручного выбора.
- Установка системных зависимостей (git, python3, curl, golang, nmap, ruby и др.) через выбранный менеджер пакетов.
- Создание структуры папок для инструментов (Web_catalog, Subdomains, Scaner, CMS, LFI, XSS, SQLj, JS, Dorks, Wordlists и т.д.).
- Клонирование популярных инструментов с GitHub в соответствующие директории (dirsearch, ParamSpider, sqlmap, nuclei, XSStrike, SSRFmap и др.).
- Установка SecLists (опционально) и попытка создать символическую ссылку в `/usr/share/seclists`.
- Установка Metasploit Framework (опционально): скачивание инсталлятора, установка и инициализация БД (`msfdb`).
- Установка общих Python-пакетов внутри виртуального окружения и установка зависимостей из всех найденных `requirements.txt`.
- Установка Go-инструментов через `go install` (assetfinder, subfinder, nuclei, httpx и др.) и создание `setup_gopath.sh` с подсказками по добавлению `GOPATH/bin` в `PATH`.

Пререквизиты:

- Python 3.x
- Интернет-соединение
- Права `sudo` для установки системных пакетов (на Linux)

````markdown
# Что делает `main.py`

`main.py` — это основной установочный и подготовительный скрипт проекта. Его задача — автоматически подготовить рабочее окружение для Bug Bounty / пентестинга и собрать полезные инструменты в упорядоченные папки.

Основные действия, выполняемые скриптом:

- Проверка ОС: скрипт проверяет, запущен ли он на Linux, и прерывает выполнение при отсутствии поддержки.
- Создание виртуального окружения Python (`venv`) и генерация инструкции по активации (`VENV_INSTRUCTIONS.txt`).
- Авто-определение пакетного менеджера Linux (`apt`, `dnf`, `yum`, `pacman`, `zypper`) с возможностью ручного выбора.
- Установка системных зависимостей (git, python3, curl, golang, nmap, ruby и др.) через выбранный менеджер пакетов.
- Создание структуры папок для инструментов (Web_catalog, Subdomains, Scaner, CMS, LFI, XSS, SQLj, JS, Dorks, Wordlists и т.д.).
- Клонирование популярных инструментов с GitHub в соответствующие директории (dirsearch, ParamSpider, sqlmap, nuclei, XSStrike, SSRFmap и др.).
- Установка SecLists (опционально) и попытка создать символическую ссылку в `/usr/share/seclists`.
- Установка Metasploit Framework (опционально): скачивание инсталлятора, установка и инициализация БД (`msfdb`).
- Установка общих Python-пакетов внутри виртуального окружения и установка зависимостей из всех найденных `requirements.txt`.
- Установка Go-инструментов через `go install` (assetfinder, subfinder, nuclei, httpx и др.) и создание `setup_gopath.sh` с подсказками по добавлению `GOPATH/bin` в `PATH`.

Пререквизиты:

- Python 3.x
- Права `sudo` для установки системных пакетов (на Linux)

Как запустить:

```bash
python3 main.py
```

После выполнения вы получите:

- Виртуальное окружение `venv` и `VENV_INSTRUCTIONS.txt` с инструкциями по активации.
- Набор папок с клонированными инструментами.
- Установленные (или частично установленные при ошибках) системные и Go-инструменты.

Важно:

Используйте установленный набор инструментов только в рамках законных и согласованных тестов. Скрипт автоматизирует установку мощных инструментов, неправильное или несанкционированное использование которых может привести к нарушению закона.

Если хотите, могу дополнительно расширить README разделами: примеры запуска каждого инструмента, рекомендации по workflow и инструкции для Windows/WSL.
````

## Инструменты, которые скачивает/устанавливает `main.py`

Ниже — перечень инструментов, которые скрипт клонирует или устанавливает, с кратким описанием и ссылками на репозитории.

- **dirsearch** — инструмент для перебора директорий и файлов на веб-сервере. https://github.com/maurosoria/dirsearch
- **ParamSpider** — сбор параметров URL из репозиториев/источников для поиска уязвимостей. https://github.com/0xKayala/ParamSpider
- **subscraper** — поиск и анализ поддоменов. https://github.com/m8sec/subscraper
- **openredirex** — проверка открытых перенаправлений (open redirect). https://github.com/devanshbatham/openredirex
- **lostools** — набор вспомогательных инструментов для поиска и анализа (различные утилиты). https://github.com/coffinsp/lostools
- **PenHunter** — инструмент для автоматизации поиска уязвимостей (репозиторий проекта). https://github.com/cc1a2b/PenHunter
- **argus** — инструмент для сбора и анализа данных (репозиторий). https://github.com/jasonxtn/argus
- **xlsNinja** — утилита для анализа/эксплуатации Excel-файлов. https://github.com/atoz-chevara/xlsNinja
- **nuclei** — шаблонный сканер уязвимостей от ProjectDiscovery. https://github.com/projectdiscovery/nuclei
- **LFIscanner** — сканер для поиска Local File Inclusion уязвимостей. https://github.com/R3LI4NT/LFIscanner
- **Lfi-Space** — дополнительные инструменты для LFI-анализа. https://github.com/capture0x/Lfi-Space
- **SQL-Injection-Finder** — утилита для поиска SQL-инъекций. https://github.com/j1t3sh/SQL-Injection-Finder
- **sqlmap** — автоматизированный инструмент для тестирования на SQL-инъекции. https://github.com/sqlmapproject/sqlmap
- **XSStrike** — сканер и fuzz-утилита для XSS. https://github.com/s0md3v/XSStrike
- **SSRFmap** — инструмент для поиска SSRF уязвимостей. https://github.com/swisskyrepo/SSRFmap
- **Pinkerton** — анализ JavaScript/веб-ресурсов на уязвимости. https://github.com/000pp/Pinkerton
- **SecretFinder** — поиск потенциальных секретов/ключей в JavaScript. https://github.com/m4ll0k/SecretFinder
- **github-dorks** — коллекция dork-запросов для поиска уязвимостей/информации. https://github.com/techgaun/github-dorks
- **theHarvester** — инструмент разведки для сбора e-mail, subdomains и прочего. https://github.com/laramies/theHarvester
- **trufflehog** — поиск секретов и чувствительных данных в репозиториях. https://github.com/trufflesecurity/trufflehog
- **nuclei-templates** — коллекция шаблонов для `nuclei`. https://github.com/projectdiscovery/nuclei-templates
- **SecLists** — большая коллекция словарей/wordlists для пентестинга. https://github.com/danielmiessler/SecLists

Go-инструменты (устанавливаются через `go install`):

- **assetfinder** — поиск связанных доменов/ресурсов. https://github.com/tomnomnom/assetfinder
- **dalfox** — инструмент для обнаружения XSS (быстрый анализ). https://github.com/hahwul/dalfox
- **katana** — высокопроизводительный краулер/сканер от ProjectDiscovery. https://github.com/projectdiscovery/katana
- **jshunter** — инструмент поиска JS-уязвимостей/анализатор. https://github.com/cc1a2b/jshunter
- **subfinder** — пассивный поиск поддоменов от ProjectDiscovery. https://github.com/projectdiscovery/subfinder
- **nuclei (Go)** — CLI-версия `nuclei` для шаблонного сканирования. https://github.com/projectdiscovery/nuclei
- **httpx** — быстрый HTTP-инструмент для проверки доступности/заголовков. https://github.com/projectdiscovery/httpx
- **wpprobe** — обнаружение WordPress-сайтов и их характеристик. https://github.com/Chocapikk/wpprobe

Системные пакеты (устанавливаются через пакетный менеджер):

- **nmap** — сетевой сканер портов и сервисов. https://nmap.org/
- **ffuf** — быстрый HTTP fuzzer (часто устанавливается как Go-инструмент). https://github.com/ffuf/ffuf
- **feroxbuster** — инструмент для перебора директорий (fast web fuzzer). https://github.com/epi052/feroxbuster
- **nikto** — веб-сканер уязвимостей сервера. https://github.com/sullo/nikto
- **Metasploit Framework** — платформа для разработки и эксплуатации эксплоитов (устанавливается опционально через инсталлятор Rapid7). https://www.metasploit.com/ и https://github.com/rapid7/metasploit-framework
- **rustscan** — быстрый сканер портов на Rust (опционно через COPR в dnf). https://github.com/RustScan/RustScan

Если хотите, могу: добавить команду примера для каждого инструмента, указать заметки по использованию или отсортировать инструменты по приоритету/workflow.

