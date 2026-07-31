#!/usr/bin/env python3
"""
BugBounty-script — автоматическая подготовка окружения для Bug Bounty / пентестинга.

ВАЖНО: используйте установленные инструменты только в рамках законных
и согласованных тестов (authorized testing / bug bounty программы).
Несанкционированное использование может нарушать закон.
"""

import argparse
import os
import shutil
import subprocess
import sys
import venv
from concurrent.futures import ThreadPoolExecutor, as_completed

IS_ROOT = hasattr(os, "geteuid") and os.geteuid() == 0
FAILURES = []  # список (этап, элемент, ошибка) для финального отчёта
MAX_WORKERS = 6  # параллелизм для I/O-bound операций (git clone, go install)


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

def print_header(text):
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50)


def sudo():
    """Возвращает 'sudo ' если скрипт запущен не от root, иначе ''."""
    return "" if IS_ROOT else "sudo "


def binary_exists(name):
    return shutil.which(name) is not None


def run(cmd, stage, item, shell=True, check_output=False, report=True):
    """
    Унифицированный запуск команды с обработкой ошибок, записью в FAILURES
    и (опционально) печатью результата в едином формате.

    При check_output=True возвращает CompletedProcess при успехе или None при ошибке.
    Иначе возвращает True/False.
    """
    try:
        if check_output:
            result = subprocess.run(cmd, shell=shell, check=True,
                                     capture_output=True, text=True)
            if report:
                print(f"✓ Успешно: {item}")
            return result
        subprocess.run(cmd, shell=shell, check=True)
        if report:
            print(f"✓ Успешно: {item}")
        return True
    except subprocess.CalledProcessError as e:
        FAILURES.append((stage, item, str(e)))
        if report:
            print(f"✗ Ошибка установки: {item}")
        return None if check_output else False
    except FileNotFoundError as e:
        FAILURES.append((stage, item, f"команда не найдена: {e}"))
        if report:
            print(f"✗ Ошибка установки: {item}")
        return None if check_output else False


def run_many(jobs, stage, max_workers=MAX_WORKERS):
    """
    Выполняет список задач параллельно (ThreadPoolExecutor) — подходит для
    I/O-bound операций вроде git clone / go install / pip install.

    jobs: список (item_label, cmd, shell)
    """
    print(f"Запускаю {len(jobs)} задач параллельно (до {max_workers} одновременно)...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run, cmd, stage, label, shell): label
            for label, cmd, shell in jobs
        }
        for future in as_completed(futures):
            future.result()  # ошибки уже записаны в FAILURES внутри run()


# ---------------------------------------------------------------------------
# Определение системы
# ---------------------------------------------------------------------------

def detect_os():
    """Определяет операционную систему"""
    if sys.platform.startswith("linux"):
        return "linux"
    return "unknown"


def check_linux_system():
    """Проверяет, что скрипт запущен на Linux"""
    if detect_os() != "linux":
        print("\n" + "!" * 60)
        print("ОШИБКА: Этот скрипт предназначен только для Linux!")
        print("Обнаружена ОС:", sys.platform)
        print("!" * 60)
        sys.exit(1)


def check_sudo_access():
    """Проверяет, что есть возможность выполнять команды с повышенными правами"""
    if IS_ROOT:
        return
    if not binary_exists("sudo"):
        print("\n" + "!" * 60)
        print("ОШИБКА: команда 'sudo' не найдена, а скрипт запущен не от root.")
        print("Установите sudo или запустите скрипт от имени root.")
        print("!" * 60)
        sys.exit(1)


def detect_linux_package_manager():
    """Определяет пакетный менеджер Linux"""
    for pm in ("apt", "dnf", "yum", "pacman", "zypper"):
        if binary_exists(pm):
            return pm
    return "unknown"


def ask_package_manager():
    """Спрашивает пользователя о пакетном менеджере для Linux"""
    print("\nВыберите ваш пакетный менеджер:")
    print("1. apt (Debian/Ubuntu/Kali)")
    print("2. dnf (Fedora/RHEL)")
    print("3. pacman (Arch/Manjaro)")
    print("4. yum (CentOS/RHEL)")
    print("5. zypper (openSUSE)")

    mapping = {"1": "apt", "2": "dnf", "3": "pacman", "4": "yum", "5": "zypper"}
    while True:
        choice = input("Введите номер (1-5): ").strip()
        if choice in mapping:
            return mapping[choice]
        print("Неверный выбор. Попробуйте снова.")


def show_banner():
    """Показывает баннер"""
    banner = r"""
        ____                 ____                    __       
      / __ )__  ______ _   / __ )____  __  ______  / /___  __
      / __  / / / / __ `/  / __  / __ \/ / / / __ \/ __/ / / /
    / /_/ / /_/ / /_/ /  / /_/ / /_/ / /_/ / / / / /_/ /_/ / 
    /_____/\__,_/\__, /  /_____/\____/\__,_/_/ /_/\__/\__, /  
                /____/                               /____/   
      __              __    
      / /_____  ____  / /____
    / __/ __ \/ __ \/ / ___/
    / /_/ /_/ / /_/ / (__  ) 
    \__/\____/\____/_/____/  
    """
    print(banner)


# ---------------------------------------------------------------------------
# Виртуальное окружение
# ---------------------------------------------------------------------------

def create_virtual_environment(venv_dir="venv"):
    """Создаёт виртуальное окружение Python (вызывать ПОСЛЕ установки системных пакетов,
    т.к. на Debian/Ubuntu для этого нужен системный пакет python3-venv)."""
    print_header("Создание виртуального окружения Python...")

    if os.path.exists(venv_dir):
        print(f"Виртуальное окружение '{venv_dir}' уже существует")
        return venv_dir

    try:
        venv.create(venv_dir, with_pip=True)
        print(f"✓ Виртуальное окружение создано: {venv_dir}")
        return venv_dir
    except Exception as e:
        FAILURES.append(("venv", venv_dir, str(e)))
        print(f"✗ Ошибка при создании виртуального окружения: {e}")
        return None


def get_venv_pip(venv_dir):
    """Возвращает АБСОЛЮТНЫЙ путь к pip в виртуальном окружении.
    Абсолютный путь обязателен: команды установки делают 'cd' в папку
    конкретного инструмента перед вызовом pip, и относительный путь
    в этот момент уже указывал бы не туда."""
    return os.path.abspath(os.path.join(venv_dir, "bin", "pip"))


# ---------------------------------------------------------------------------
# Системные пакеты
# ---------------------------------------------------------------------------

PACKAGE_COMMANDS = {
    "apt": [
        "{sudo}apt update",
        "{sudo}apt install -y git python3 python3-venv python3-pip curl wget "
        "golang-go nmap nikto ruby ruby-dev build-essential libpq-dev "
        "zlib1g-dev libsqlite3-dev feroxbuster cargo jq "
        "libzstd-dev make",
    ],
    "dnf": [
        "{sudo}dnf update -y",
        "{sudo}dnf install -y git python3 python3-pip curl wget golang nmap "
        "nikto ruby ruby-devel postgresql-devel zlib-devel sqlite-devel "
        "cargo jq libzstd-devel make",
        "{sudo}dnf copr enable atim/rustscan -y && {sudo}dnf install -y rustscan",
    ],
    "pacman": [
        "{sudo}pacman -Syu --noconfirm",
        "{sudo}pacman -S --noconfirm git python python-pip curl wget go nmap "
        "nikto ruby rust jq zstd make",
    ],
    "yum": [
        "{sudo}yum update -y",
        "{sudo}yum install -y git python3 python3-pip curl wget golang nmap "
        "nikto ruby ruby-devel cargo jq libzstd-devel make",
    ],
    "zypper": [
        "{sudo}zypper refresh",
        "{sudo}zypper install -y git python3 python3-pip curl wget go nmap "
        "nikto ruby ruby-devel cargo jq libzstd-devel make",
    ],
}


def install_system_packages(package_manager):
    """Устанавливает системные зависимости и инструменты одним проходом
    (раньше это были две отдельные функции с дублирующимся apt update и пакетами)."""
    print_header("Установка системных зависимостей и инструментов...")

    commands = PACKAGE_COMMANDS.get(package_manager)
    if not commands:
        print("Неизвестный пакетный менеджер. Пропускаем установку системных пакетов.")
        return

    for template in commands:
        cmd = template.format(sudo=sudo())
        print(f"Выполняю: {cmd}")
        if not run(cmd, "Системные пакеты", cmd, report=False):
            print(f"Предупреждение: команда завершилась с ошибкой: {cmd}")


def install_ruby_tools():
    """Устанавливает Ruby-инструменты (WPScan) поверх системного Ruby"""
    print_header("Установка Ruby-инструментов (WPScan)...")

    if not binary_exists("gem"):
        print("✗ gem не найден, пропускаем установку WPScan")
        FAILURES.append(("Ruby tools", "wpscan", "бинарь gem не найден"))
        return

    cmd = f"{sudo()}gem install wpscan"
    print(f"Выполняю: {cmd}")
    run(cmd, "Ruby tools", "wpscan")


def install_rust_tools():
    """Устанавливает Rust/Cargo-инструменты (x8 — параметр-дискавери на Rust)"""
    print_header("Установка Rust-инструментов (x8)...")

    if not binary_exists("cargo"):
        print("✗ cargo не найден, пропускаем установку Rust-инструментов")
        FAILURES.append(("Rust tools", "cargo", "бинарь cargo не найден"))
        return

    cmd = "cargo install x8"
    print(f"Выполняю: {cmd}")
    run(cmd, "Rust tools", "x8")


# ---------------------------------------------------------------------------
# Структура папок и инструменты
# ---------------------------------------------------------------------------

FOLDERS = [
    "Web_catalog",
    "Subdomains",
    "Scaner",
    "CMS",
    "SSRF",
    "Open_redirect",
    "LFI",
    "XSS",
    "SSTI",
    "SQLj",
    "JS",
    "Dorks",
    "Reconnaissance",
    "Secrets",
    "Nuclei_Templates",
    "Wordlists",
    "API_GraphQL",
    "Cloud",
    "Mobile",
]


def create_folders():
    """Создаёт структуру папок для инструментов"""
    print_header("Создание структуры папок...")

    for folder in FOLDERS:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"Создана папка: {folder}")
        except OSError as e:
            FAILURES.append(("Папки", folder, str(e)))
            print(f"Ошибка при создании папки {folder}: {e}")


# Репозитории для git-клонирования, сгруппированные по категориям/папкам.
GIT_TOOLS = {
    "Web_catalog": [
        "https://github.com/maurosoria/dirsearch.git",
        "https://github.com/0xKayala/ParamSpider.git",
        "https://github.com/s0md3v/Arjun.git",              # HTTP-параметр дискавери
    ],
    "Subdomains": [
        "https://github.com/m8sec/subscraper.git",
    ],
    "Open_redirect": [
        "https://github.com/devanshbatham/openredirex.git",
    ],
    "Scaner": [
        "https://github.com/coffinsp/lostools.git",
        "https://github.com/cc1a2b/PenHunter.git",
        "https://github.com/jasonxtn/argus.git",
        "https://github.com/atoz-chevara/xlsNinja.git",
        "https://github.com/projectdiscovery/nuclei.git",
    ],
    "LFI": [
        "https://github.com/R3LI4NT/LFIscanner.git",
        "https://github.com/capture0x/Lfi-Space.git",
    ],
    "SQLj": [
        "https://github.com/j1t3sh/SQL-Injection-Finder",
        "https://github.com/sqlmapproject/sqlmap",
    ],
    "XSS": [
        "https://github.com/s0md3v/XSStrike",
    ],
    "SSTI": [
        # legacy-проект (Python 2 в основе), может требовать доп. правок для py3
        "https://github.com/epinna/tplmap",
    ],
    "SSRF": [
        "https://github.com/swisskyrepo/SSRFmap",
    ],
    "JS": [
        "https://github.com/000pp/Pinkerton",
        "https://github.com/m4ll0k/SecretFinder",
    ],
    "CMS": [
        "https://github.com/Tuhinshubhra/CMSeeK.git",
        "https://github.com/droope/droopescan.git",
    ],
    "Dorks": [
        "https://github.com/techgaun/github-dorks",
    ],
    "Reconnaissance": [
        "https://github.com/laramies/theHarvester",
    ],
    "Secrets": [
        "https://github.com/trufflesecurity/trufflehog",
    ],
    "Nuclei_Templates": [
        "https://github.com/projectdiscovery/nuclei-templates",
    ],
    "API_GraphQL": [
        "https://github.com/dolevf/graphql-cop.git",         # сканер уязвимостей GraphQL
    ],
    "Cloud": [
        "https://github.com/initstring/cloud_enum.git",      # enum S3/Azure/GCP по имени компании
        "https://github.com/0xsha/CloudBrute.git",            # требует ручной 'go build' после клонирования
    ],
}

# Тяжёлые/опциональные инструменты для мобильного пентеста (--install-mobile-tools)
MOBILE_GIT_TOOLS = {
    "Mobile": [
        "https://github.com/MobSF/Mobile-Security-Framework-MobSF.git",  # статич+динам анализ APK/IPA
    ],
}


def _clone_job(category, repo):
    repo_name = repo.rstrip("/").split("/")[-1].replace(".git", "")
    target_dir = os.path.join(category, repo_name)
    if os.path.exists(target_dir):
        print(f"Пропускаем {repo_name} (уже существует)")
        return None
    cmd = ["git", "clone", "--depth", "1", repo, target_dir]
    return (repo_name, cmd, False)


def download_tools(tools_dict=None, stage_label="Скачивание инструментов"):
    """Скачивает инструменты из GitHub параллельно (git clone), список репозиториев
    по категориям задаётся в tools_dict (по умолчанию GIT_TOOLS)."""
    print_header(f"{stage_label}...")

    if not binary_exists("git"):
        print("✗ git не найден, пропускаем скачивание инструментов")
        FAILURES.append((stage_label, "git", "бинарь git не найден"))
        return

    tools_dict = tools_dict if tools_dict is not None else GIT_TOOLS

    jobs = []
    for category, repos in tools_dict.items():
        for repo in repos:
            job = _clone_job(category, repo)
            if job:
                jobs.append(job)

    if not jobs:
        print("Нечего скачивать (все репозитории уже присутствуют).")
        return

    run_many(jobs, stage_label)


def install_seclists():
    """Устанавливает SecLists — коллекции wordlists для пентеста"""
    print_header("Установка SecLists...")

    seclists_dir = os.path.join("Wordlists", "SecLists")

    if os.path.exists(seclists_dir):
        print("SecLists уже установлены")
        return True

    if not binary_exists("git"):
        print("✗ git не найден, пропускаем установку SecLists")
        FAILURES.append(("SecLists", "git", "бинарь git не найден"))
        return False

    print("Скачиваю SecLists...")
    cmd = f"git clone --depth 1 https://github.com/danielmiessler/SecLists.git {seclists_dir}"
    if not run(cmd, "SecLists", "клонирование"):
        return False

    link_target = "/usr/share/seclists"
    if os.path.exists(link_target):
        print(f"{link_target} уже существует")
    else:
        current_dir = os.getcwd()
        cmd = f"{sudo()}ln -sf {current_dir}/{seclists_dir} {link_target}"
        if run(cmd, "SecLists", "symlink"):
            print(f"✓ Создана символическая ссылка {link_target}")
        else:
            print(f"⚠ Не удалось создать ссылку {link_target}. Создайте вручную при необходимости.")

    return True


def install_metasploit(package_manager):
    """Устанавливает Metasploit Framework через пакетный менеджер, без скачивания
    отдельного файла-установщика."""
    print_header("Установка Metasploit Framework...")

    if binary_exists("msfconsole"):
        print("Metasploit Framework уже установлен")
        db_check = subprocess.run(["msfdb", "status"], capture_output=True, text=True)
        if "not running" in db_check.stdout or "not initialized" in db_check.stdout:
            print("Инициализируем базу данных Metasploit...")
            run(f"{sudo()}msfdb init", "Metasploit", "msfdb init")
        return True

    install_commands = {
        "apt": f"{sudo()}apt install -y metasploit-framework",
        "dnf": f"{sudo()}dnf install -y metasploit-framework",
        "yum": f"{sudo()}yum install -y metasploit-framework",
        "pacman": f"{sudo()}pacman -S --noconfirm metasploit",
        "zypper": f"{sudo()}zypper install -y metasploit-framework",
    }

    cmd = install_commands.get(package_manager)
    if not cmd:
        print(f"✗ Нет команды установки Metasploit для пакетного менеджера '{package_manager}'")
        FAILURES.append(("Metasploit", "install", f"нет команды для {package_manager}"))
        return False

    if package_manager == "apt":
        print("Установка зависимостей для Metasploit...")
        run(f"{sudo()}apt install -y libpq-dev postgresql postgresql-contrib libpcap-dev",
            "Metasploit", "зависимости apt")

    print(f"Выполняю: {cmd}")
    if not run(cmd, "Metasploit", "установка пакета"):
        print("  Возможно, пакет недоступен в репозиториях вашего дистрибутива")
        print("  (типично для не-Kali Debian/Ubuntu) — установите вручную при необходимости")
        return False

    run(f"{sudo()}msfdb init", "Metasploit", "инициализация БД")
    return True


def install_trivy():
    """Устанавливает Trivy (сканер уязвимостей контейнеров/IaC) через официальный
    install-скрипт — работает одинаково на всех поддерживаемых дистрибутивах."""
    print_header("Установка Trivy...")

    if binary_exists("trivy"):
        print("Trivy уже установлен")
        return True

    if not binary_exists("curl"):
        print("✗ curl не найден, пропускаем установку Trivy")
        FAILURES.append(("Trivy", "curl", "бинарь curl не найден"))
        return False

    cmd = (
        "curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/"
        f"contrib/install.sh | {sudo()}sh -s -- -b /usr/local/bin"
    )
    return bool(run(cmd, "Trivy", "install.sh"))


def install_mobile_tools():
    """Опционально устанавливает инструменты для мобильного пентеста
    (тяжёлые/специфичные зависимости — Docker для MobSF, JDK для apktool/jadx)."""
    print_header("Установка инструментов для мобильного пентеста...")

    download_tools(MOBILE_GIT_TOOLS, stage_label="Mobile tools")

    print("\nПримечания:")
    print("  - MobSF рекомендуется запускать через Docker:")
    print("    docker pull opensecurity/mobile-security-framework-mobsf:latest")
    print("  - apktool и jadx можно поставить пакетным менеджером (если есть в репозиториях)")
    print("    или скачать релизы вручную: https://github.com/iBotPeaches/Apktool "
          "и https://github.com/skylot/jadx")


def install_python_requirements(venv_dir):
    """Устанавливает Python-зависимости для инструментов в виртуальном окружении"""
    print_header("Установка Python-зависимостей в виртуальном окружении...")

    venv_pip = get_venv_pip(venv_dir)

    common_packages = [
        "requests", "beautifulsoup4", "urllib3", "colorama", "lxml",
        "pyyaml", "tqdm", "bs4", "dnspython", "certifi",
        "charset-normalizer", "idna", "soupsieve",
        "autorecon",  # оркестратор recon-сканов (nmap + веб-сканы по найденным портам)
    ]

    print("Установка общих Python-пакетов одной командой...")
    cmd = f'"{venv_pip}" install ' + " ".join(common_packages)
    run(cmd, "Python deps", "common packages")

    # Инструменты, чьи requirements.txt тянут пакеты, несовместимые с Python 3
    # (написаны под Python 2 и не имеют актуальной версии зависимостей) —
    # автоматическая установка гарантированно упадёт, пропускаем и ставим вручную.
    SKIP_REQUIREMENTS = {"tplmap", "LFIscanner"}

    # Ищем requirements.txt / setup.py только в известных папках с инструментами,
    # а не во всём дереве проекта — быстрее и предсказуемее.
    search_roots = FOLDERS
    req_jobs = []
    skipped = []
    for root_folder in search_roots:
        if not os.path.isdir(root_folder):
            continue
        for root, _dirs, files in os.walk(root_folder):
            tool_name = os.path.basename(root)
            if tool_name in SKIP_REQUIREMENTS:
                if "requirements.txt" in files:
                    skipped.append(tool_name)
                continue
            if "requirements.txt" in files:
                # cd в папку самого инструмента: requirements.txt может содержать
                # '-e .' (editable install), который иначе резолвится относительно
                # текущей рабочей директории скрипта, а не относительно самого файла.
                cmd = f'cd "{root}" && "{venv_pip}" install -r requirements.txt'
                req_jobs.append((f"{tool_name}/requirements.txt", cmd, True))
            if "setup.py" in files and "xlsNinja" in root:
                cmd = f'cd "{root}" && "{venv_pip}" install .'
                req_jobs.append(("xlsNinja", cmd, True))

    if skipped:
        print(f"Пропускаю (легаси Python 2, несовместимо с venv): {', '.join(skipped)}")
        print("  Для этих инструментов используйте отдельное окружение с Python 2/pip2,")
        print("  либо их актуальные форки, если такие есть.")

    if req_jobs:
        print(f"Найдено {len(req_jobs)} requirements.txt/setup.py — устанавливаю параллельно...")
        run_many(req_jobs, "Python deps")


def install_kiterunner():
    """Устанавливает kiterunner (brute-force API-эндпоинтов по Swagger/OpenAPI).
    Не ставится через `go install`, т.к. использует CGO + libzstd и собирается
    через Makefile, а не как обычный versioned Go-модуль."""
    print_header("Установка kiterunner...")

    if binary_exists("kr"):
        print("kiterunner (команда 'kr') уже установлен")
        return True

    if not binary_exists("git") or not binary_exists("make") or not binary_exists("go"):
        print("✗ Нужны git, make и go для сборки kiterunner — пропускаем")
        FAILURES.append(("kiterunner", "deps", "git/make/go не найдены"))
        return False

    target_dir = os.path.join("API_GraphQL", "kiterunner")
    if not os.path.exists(target_dir):
        clone_cmd = ["git", "clone", "--depth", "1",
                     "https://github.com/assetnote/kiterunner.git", target_dir]
        if not run(clone_cmd, "kiterunner", "клонирование", shell=False):
            return False

    build_cmd = f'cd "{target_dir}" && make build'
    if not run(build_cmd, "kiterunner", "make build"):
        print("  Сборка не удалась — проверьте наличие libzstd-dev/libzstd-devel")
        return False

    # Собранный бинарь называется 'kr' (см. Makefile проекта), а не 'kiterunner'
    binary_path = os.path.join(target_dir, "dist", "kr")
    if os.path.exists(binary_path):
        install_cmd = f"{sudo()}cp {binary_path} /usr/local/bin/kr"
        if run(install_cmd, "kiterunner", "установка в /usr/local/bin"):
            print("✓ kiterunner доступен в PATH как команда 'kr'")
            return True
        print(f"  Бинарь собран, но не скопирован — используйте напрямую: {binary_path}")

    return True


def setup_go_tools():
    """Устанавливает Go-инструменты параллельно"""
    print_header("Установка Go-инструментов...")

    if not binary_exists("go"):
        print("✗ Go не найден в системе, пропускаем установку Go-инструментов")
        FAILURES.append(("Go tools", "go", "бинарь go не найден"))
        return

    go_tools = [
        "github.com/tomnomnom/assetfinder@latest",
        "github.com/hahwul/dalfox/v2@latest",
        "github.com/projectdiscovery/katana/cmd/katana@latest",
        "github.com/cc1a2b/jshunter/cmd/jshunter@latest",
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        "github.com/ffuf/ffuf/v2@latest",
        "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        "github.com/projectdiscovery/httpx/cmd/httpx@latest",
        "github.com/Chocapikk/wpprobe@latest",
        "github.com/tomnomnom/waybackurls@latest",          # сбор исторических URL
        "github.com/lc/gau/v2/cmd/gau@latest",               # сбор исторических URL (доп. источники)
        "github.com/sensepost/gowitness@latest",             # массовые скриншоты хостов
        "github.com/PentestPad/subzy@latest",                 # детект subdomain takeover
        "github.com/zricethezav/gitleaks/v8@latest",           # поиск секретов в коде (module path в go.mod)
        # добавлено по итогам обсуждения:
        "github.com/owasp-amass/amass/v4/...@master",         # мощный active/passive subdomain enum
        "github.com/projectdiscovery/chaos-client/cmd/chaos@latest",  # база поддоменов Chaos
        "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",      # быстрый port scan
        "github.com/projectdiscovery/dnsx/cmd/dnsx@latest",           # массовая DNS-резолюция
        "github.com/projectdiscovery/notify/cmd/notify@latest",       # пуш результатов в Slack/Discord/TG
        "github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest",  # свой OOB-сервер
        "github.com/hakluke/hakrawler@latest",                # веб-краулер
        "github.com/sa7mon/s3scanner@latest",                 # поиск открытых S3-бакетов (module lowercase)
        # kiterunner НЕ ставится через go install (CGO + libzstd, сборка через Makefile) —
        # см. install_kiterunner()
    ]

    jobs = [(tool, f"go install {tool}", True) for tool in go_tools]
    run_many(jobs, "Go tools")


def setup_go_path():
    """Определяет каталог GOPATH/bin и печатает подсказку по добавлению в PATH.
    Возвращает путь к go_bin или None, если Go недоступен."""
    print_header("Настройка PATH для Go-инструментов...")

    if not binary_exists("go"):
        print("✗ Go не найден, пропускаем настройку PATH")
        return None

    result = run(["go", "env", "GOPATH"], "Go PATH", "go env GOPATH",
                 shell=False, check_output=True, report=False)
    if not result:
        print("Ошибка при определении Go PATH")
        return None

    go_path = result.stdout.strip()
    go_bin = os.path.join(go_path, "bin")

    if not os.path.exists(go_bin):
        print(f"Каталог {go_bin} пока не создан (возможно, go install ещё не запускался)")
        return go_bin

    print(f"Go bin directory: {go_bin}")

    current_path = os.environ.get("PATH", "")
    if go_bin in current_path:
        print("✓ Go bin уже добавлен в PATH")
        return go_bin

    print("Добавьте этот путь в переменную окружения PATH:")
    print(f'  export PATH="$PATH:{go_bin}"')
    print("Добавьте эту строку в файл ~/.bashrc или ~/.zshrc для постоянного эффекта")

    return go_bin


def print_venv_activation_info(venv_dir):
    """Печатает инструкцию по активации виртуального окружения (без записи в файл)"""
    print_header("Инструкция по активации виртуального окружения:")
    print("\nДля активации виртуального окружения выполните:")
    print(f"source {venv_dir}/bin/activate")
    print("\nДля деактивации выполните:")
    print("deactivate")


# ---------------------------------------------------------------------------
# Итоговые отчёты
# ---------------------------------------------------------------------------

def print_installed_tools_summary():
    print("\n✓ Установленные инструменты:")
    print("  РАЗВЕДКА (Reconnaissance):")
    print("    - theHarvester — сбор информации о доменах")
    print("    - assetfinder, subfinder, amass, chaos-client — поиск поддоменов")
    print("    - subzy — детект subdomain takeover (Go)")
    print("    - waybackurls, gau — сбор исторических URL (Go)")
    print("    - gowitness — массовые скриншоты хостов (Go)")
    print("    - naabu — быстрый port scan (Go)")
    print("    - dnsx — массовая DNS-резолюция и фильтрация (Go)")
    print("    - hakrawler, katana — веб-краулинг (Go)")
    print("  ")
    print("  СКАНИРОВАНИЕ УЯЗВИМОСТЕЙ:")
    print("    - nuclei — темплейт-базированное сканирование (Go)")
    print("    - nikto — веб-сканер")
    print("    - Metasploit — фреймворк для эксплуатации уязвимостей (опционально)")
    print("    - interactsh-client — собственный OOB-сервер для слепых SSRF/XXE/RCE")
    print("    - notify — пуш результатов сканов в Slack/Discord/Telegram")
    print("  ")
    print("  CMS:")
    print("    - WPScan — сканер WordPress (gem)")
    print("    - CMSeeK, droopescan — определение и анализ CMS")
    print("    - wpprobe — быстрый WordPress-сканер (Go)")
    print("  ")
    print("  API / GraphQL:")
    print("    - graphql-cop — сканер уязвимостей GraphQL")
    print("    - kiterunner (команда 'kr') — brute-force API-эндпоинтов по Swagger/OpenAPI (сборка из исходников)")
    print("  ")
    print("  WORDLISTS:")
    print("    - SecLists — коллекции словарей для брутфорса (опционально)")
    print("  ")
    print("  АНАЛИЗ JAVASCRIPT & SECRETS:")
    print("    - SecretFinder — поиск API-ключей в JS")
    print("    - Pinkerton — анализ JS на уязвимости")
    print("    - trufflehog, gitleaks — поиск credentials в коде")
    print("  ")
    print("  FUZZING & BRUTE FORCE:")
    print("    - ffuf — быстрый HTTP fuzzer (Go)")
    print("    - feroxbuster — перебор путей")
    print("    - dirsearch — поиск скрытых папок")
    print("    - Arjun, x8 — обнаружение скрытых HTTP-параметров")
    print("  ")
    print("  СПЕЦИАЛИЗИРОВАННЫЕ СКАНЕРЫ:")
    print("    - sqlmap — SQL-инъекции")
    print("    - XSStrike, dalfox — XSS-уязвимости")
    print("    - SSRFmap — SSRF-уязвимости")
    print("    - tplmap — Server-Side Template Injection (легаси, py2)")
    print("    - LFI Scanner, Lfi-Space — Local File Inclusion")
    print("  ")
    print("  CLOUD:")
    print("    - cloud_enum — enum S3/Azure/GCP по имени компании")
    print("    - S3Scanner — поиск открытых S3-бакетов (Go)")
    print("    - CloudBrute — enum облачных ресурсов (требует ручной go build)")
    print("    - Trivy — сканер уязвимостей контейнеров/IaC (опционально)")
    print("  ")
    print("  MOBILE (опционально, --install-mobile-tools):")
    print("    - MobSF — статический + динамический анализ APK/IPA (через Docker)")
    print("    - apktool, jadx — декомпиляция APK (ставятся вручную)")
    print("  ")
    print("  ДОПОЛНИТЕЛЬНО:")
    print("    - nuclei-templates — готовые шаблоны сканирования")
    print("    - AutoRecon (pip) — оркестратор recon: сам запускает nmap + веб-сканы")


def print_recommended_workflow():
    print("\nРЕКОМЕНДУЕМЫЙ WORKFLOW для Bug Bounty:")
    print("  1. Разведка: theHarvester → subfinder → amass → chaos → assetfinder → httpx")
    print("  2. Проверка takeover: subzy")
    print("  3. Порты/DNS: naabu → dnsx")
    print("  4. Поиск секретов: SecretFinder → trufflehog → gitleaks")
    print("  5. Fuzzing/параметры: ffuf → feroxbuster → dirsearch → Arjun/x8 (с SecLists)")
    print("  6. Краулинг: katana / hakrawler → waybackurls / gau")
    print("  7. Сканирование: nuclei → nikto → graphql-cop (для API)")
    print("  8. Слепые уязвимости: interactsh-client (OOB для SSRF/XXE/RCE)")
    print("  9. Cloud: cloud_enum → S3Scanner")
    print("  10. Эксплуатация: Metasploit для известных уязвимостей")
    print("  11. Автоматизация уведомлений: notify (Slack/Discord/Telegram)")


def print_failures_report():
    print("\n" + "=" * 70)
    if not FAILURES:
        print("✓ Все шаги установки завершились без ошибок.")
        return
    print(f"⚠ Обнаружено {len(FAILURES)} ошибок/предупреждений в процессе установки:")
    print("=" * 70)
    for stage, item, error in FAILURES:
        short_error = error if len(error) < 200 else error[:200] + "..."
        print(f"  [{stage}] {item}: {short_error}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

# Опциональные компоненты, задаются данными, а не повторяющимся кодом в main().
# Формат: (флаг_атрибута_argparse, текст_вопроса, install_func(package_manager) -> None)
OPTIONAL_COMPONENTS = [
    ("install_seclists", "Установить SecLists (коллекция wordlists)? (y/n): ",
     lambda pm: install_seclists()),
    ("install_metasploit", "Установить Metasploit Framework? (y/n): ",
     lambda pm: install_metasploit(pm)),
    ("install_trivy", "Установить Trivy (сканер контейнеров/IaC)? (y/n): ",
     lambda pm: install_trivy()),
    ("install_mobile_tools", "Установить инструменты для мобильного пентеста (MobSF и др.)? (y/n): ",
     lambda pm: install_mobile_tools()),
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Подготовка окружения для Bug Bounty / пентестинга."
    )
    parser.add_argument(
        "--package-manager", choices=["apt", "dnf", "yum", "pacman", "zypper"],
        help="Явно указать пакетный менеджер (пропускает автоопределение и вопрос)",
    )
    parser.add_argument(
        "--venv-dir", default="venv",
        help="Имя каталога для виртуального окружения (по умолчанию: venv)",
    )
    parser.add_argument(
        "--skip-venv", action="store_true",
        help="Не создавать виртуальное окружение Python",
    )
    parser.add_argument(
        "--install-seclists", action="store_true",
        help="Установить SecLists без вопроса",
    )
    parser.add_argument(
        "--install-metasploit", action="store_true",
        help="Установить Metasploit Framework без вопроса",
    )
    parser.add_argument(
        "--install-trivy", action="store_true",
        help="Установить Trivy без вопроса",
    )
    parser.add_argument(
        "--install-mobile-tools", action="store_true",
        help="Установить инструменты для мобильного пентеста (MobSF и др.) без вопроса",
    )
    parser.add_argument(
        "--non-interactive", "-y", action="store_true",
        help="Не задавать вопросы; использовать автоопределение и флаги выше",
    )
    return parser.parse_args()


def resolve_package_manager(args):
    """Определяет пакетный менеджер: явный флаг → автоопределение (+ подтверждение) → ручной выбор."""
    if args.package_manager:
        print(f"\n✓ Пакетный менеджер задан вручную: {args.package_manager}")
        return args.package_manager

    auto_pm = detect_linux_package_manager()
    if auto_pm == "unknown":
        print("\nНе удалось определить пакетный менеджер автоматически.")
        if args.non_interactive:
            print("Неинтерактивный режим без --package-manager — выходим.")
            sys.exit(1)
        return ask_package_manager()

    print(f"\n✓ Автоматически определён пакетный менеджер: {auto_pm}")
    if args.non_interactive:
        return auto_pm

    use_auto_pm = input("Использовать его? (y/n): ").strip().lower()
    return auto_pm if use_auto_pm == "y" else ask_package_manager()


def resolve_optional_flags(args):
    """Определяет, какие опциональные компоненты ставить: явные флаги CLI
    имеют приоритет, иначе (в интерактивном режиме) спрашиваем пользователя."""
    flags = {name: getattr(args, name) for name, _prompt, _fn in OPTIONAL_COMPONENTS}

    if args.non_interactive:
        return flags

    print("\n" + "-" * 50)
    for name, prompt, _fn in OPTIONAL_COMPONENTS:
        if not flags[name]:
            flags[name] = input(prompt).strip().lower() == "y"

    return flags


def main():
    """Основная функция"""
    args = parse_args()
    show_banner()

    check_linux_system()
    check_sudo_access()

    package_manager = resolve_package_manager(args)
    print(f"\n✓ Выбран пакетный менеджер: {package_manager}")

    optional_flags = resolve_optional_flags(args)

    # --- Установка системных пакетов СНАЧАЛА (включая python3-venv) ---
    install_system_packages(package_manager)
    install_ruby_tools()
    install_rust_tools()

    # --- venv создаём ПОСЛЕ системных зависимостей ---
    venv_dir = None
    if not args.skip_venv:
        venv_dir = create_virtual_environment(args.venv_dir)
        if not venv_dir:
            print("Не удалось создать виртуальное окружение. Продолжаем без него...")

    create_folders()
    download_tools()
    setup_go_tools()
    install_kiterunner()
    go_bin = setup_go_path()

    for name, _prompt, install_fn in OPTIONAL_COMPONENTS:
        if optional_flags[name]:
            install_fn(package_manager)

    if venv_dir:
        install_python_requirements(venv_dir)
        print_venv_activation_info(venv_dir)

    # --- Итоги ---
    print_header("✓ УСТАНОВКА ЗАВЕРШЕНА!")

    if venv_dir:
        print(f"\n✓ Виртуальное окружение создано в папке: {venv_dir}")
        print(f"✓ Для активации окружения выполните: source {venv_dir}/bin/activate")
        print("✓ Для деактивации: deactivate")

    print("\n✓ Инструменты скачаны в соответствующие папки (см. отчёт об ошибках ниже).")
    print(f"\n✓ Использованный пакетный менеджер: {package_manager}")

    if go_bin:
        print("\n" + "-" * 50)
        print("GO-ИНСТРУМЕНТЫ:")
        print("-" * 50)
        print(f'export PATH="$PATH:{go_bin}"')
        print("Добавьте строку выше в ~/.bashrc или ~/.zshrc для постоянного эффекта.")

    if optional_flags["install_seclists"]:
        print("\n✓ SecLists установлены в папке Wordlists/SecLists")
        print("  Для использования в других инструментах: /usr/share/seclists")

    if optional_flags["install_metasploit"]:
        print("\n✓ Metasploit Framework установлен")
        print("  Для запуска: msfconsole")
        print("  Для инициализации БД: sudo msfdb init")
        print("  Для проверки статуса БД: msfdb status")

    if optional_flags["install_trivy"]:
        print("\n✓ Trivy установлен")
        print("  Пример запуска: trivy image <образ> | trivy fs <путь>")

    if optional_flags["install_mobile_tools"]:
        print("\n✓ Инструменты для мобильного пентеста подготовлены (см. заметки выше)")

    print_installed_tools_summary()
    print_recommended_workflow()
    print_failures_report()

    print("\n" + "=" * 70)
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nУстановка прервана пользователем.")
        print_failures_report()
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Непредвиденная ошибка: {e}")
        print_failures_report()
        sys.exit(1)
