import os
import subprocess
import sys
import venv

def detect_os():
    """Определяет операционную систему"""
    if sys.platform.startswith('linux'):
        return 'linux'
    else:
        return 'unknown'

def detect_linux_package_manager():
    """Определяет пакетный менеджер Linux"""
    try:
        # Проверяем какой пакетный менеджер доступен
        if subprocess.run(["which", "apt"], capture_output=True).returncode == 0:
            return "apt"
        elif subprocess.run(["which", "dnf"], capture_output=True).returncode == 0:
            return "dnf"
        elif subprocess.run(["which", "yum"], capture_output=True).returncode == 0:
            return "yum"
        elif subprocess.run(["which", "pacman"], capture_output=True).returncode == 0:
            return "pacman"
        elif subprocess.run(["which", "zypper"], capture_output=True).returncode == 0:
            return "zypper"
        else:
            return "unknown"
    except:
        return "unknown"

def check_linux_system():
    """Проверяет что скрипт запущен на Linux"""
    if not sys.platform.startswith('linux'):
        print("\n" + "!"*60)
        print("ОШИБКА: Этот скрипт предназначен только для Linux!")
        print("Обнаружена ОС:", sys.platform)
        print("!"*60)
        sys.exit(1)

def ask_package_manager():
    """Спрашивает пользователя о пакетном менеджере для Linux"""
    print("\nВыберите ваш пакетный менеджер:")
    print("1. apt (Debian/Ubuntu/Kali)")
    print("2. dnf (Fedora/RHEL)")
    print("3. pacman (Arch/Manjaro)")
    print("4. yum (CentOS/RHEL)")
    print("5. zypper (openSUSE)")
    
    while True:
        choice = input("Введите номер (1-5): ").strip()
        if choice == '1':
            return 'apt'
        elif choice == '2':
            return 'dnf'
        elif choice == '3':
            return 'pacman'
        elif choice == '4':
            return 'yum'
        elif choice == '5':
            return 'zypper'
        else:
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

def create_virtual_environment():
    """Создает виртуальное окружение Python"""
    print("\n" + "="*50)
    print("Создание виртуального окружения Python...")
    print("="*50)
    
    venv_dir = "venv"
    
    if os.path.exists(venv_dir):
        print(f"Виртуальное окружение '{venv_dir}' уже существует")
        return venv_dir
    
    try:
        # Создаем виртуальное окружение
        venv.create(venv_dir, with_pip=True)
        print(f"✓ Виртуальное окружение создано: {venv_dir}")
        return venv_dir
    except Exception as e:
        print(f"✗ Ошибка при создании виртуального окружения: {e}")
        return None

def get_venv_python(venv_dir):
    """Возвращает путь к Python в виртуальном окружении"""
    return os.path.join(venv_dir, "bin", "python")

def get_venv_pip(venv_dir):
    """Возвращает путь к pip в виртуальном окружении"""
    return os.path.join(venv_dir, "bin", "pip")

def install_dependencies(package_manager):
    """Устанавливает системные зависимости"""
    print("\n" + "="*50)
    print("Установка системных зависимостей...")
    print("="*50)
    
    if package_manager == 'apt':
        commands = [
            "sudo apt update",
            "sudo apt install -y git python3 python3-pip curl golang-go nmap ruby ruby-dev build-essential libpq-dev zlib1g-dev libsqlite3-dev",
        ]
    elif package_manager == 'dnf':
        commands = [
            "sudo dnf update -y",
            "sudo dnf install -y git python3 python3-pip curl golang nmap ruby ruby-devel postgresql-devel zlib-devel sqlite-devel",
        ]
    elif package_manager == 'pacman':
        commands = [
            "sudo pacman -Syu --noconfirm",
            "sudo pacman -S --noconfirm git python python-pip curl go nmap ruby",
        ]
    elif package_manager == 'yum':
        commands = [
            "sudo yum update -y",
            "sudo yum install -y git python3 python3-pip curl golang nmap ruby ruby-devel",
        ]
    elif package_manager == 'zypper':
        commands = [
            "sudo zypper refresh",
            "sudo zypper install -y git python3 python3-pip curl go nmap ruby ruby-devel",
        ]
    else:
        print("Неизвестный пакетный менеджер. Пропускаем установку системных зависимостей.")
        return
    
    for cmd in commands:
        print(f"Выполняю: {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Предупреждение: команда завершилась с ошибкой: {cmd}")
            continue

def create_folders():
    """Создает структуру папок для инструментов"""
    print("\n" + "="*50)
    print("Создание структуры папок...")
    print("="*50)
    
    folders = [
        "Web_catalog",
        "Subdomains", 
        "Scaner",
        "CMS",
        "SSRF",
        "Open_redirect",
        "LFI",
        "XSS",
        "SQLj",
        "JS",
        "Dorks",
        "Reconnaissance",
        "Secrets",
        "Nuclei_Templates",
        "Wordlists",
    ]
    
    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"Создана папка: {folder}")
        except Exception as e:
            print(f"Ошибка при создании папки {folder}: {e}")

def download_tools(venv_dir=None):
    """Скачивает инструменты из GitHub"""
    print("\n" + "="*50)
    print("Скачивание инструментов...")
    print("="*50)
    
    tools = {
        "Web_catalog": [
            "https://github.com/maurosoria/dirsearch.git",
            "https://github.com/0xKayala/ParamSpider.git",
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
        "SSRF": [
            "https://github.com/swisskyrepo/SSRFmap",
        ],
        "JS": [
            "https://github.com/000pp/Pinkerton",
            "https://github.com/m4ll0k/SecretFinder",
        ],
        "CMS": [
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
        ]
    }
    
    for category, repos in tools.items():
        print(f"\n--- {category} ---")
        for repo in repos:
            repo_name = repo.split("/")[-1].replace(".git", "")
            target_dir = os.path.join(category, repo_name)
            
            if os.path.exists(target_dir):
                print(f"Пропускаем {repo_name} (уже существует)")
                continue
                
            print(f"Скачиваю: {repo_name}")
            try:
                cmd = f"git clone --depth 1 {repo} {target_dir}"
                subprocess.run(cmd, shell=True, check=True)
                print(f"✓ Успешно: {repo_name}")
            except subprocess.CalledProcessError:
                print(f"✗ Ошибка при скачивании: {repo_name}")

def install_seclists():
    """Устанавливает SecLists - коллекции wordlists для пентеста"""
    print("\n" + "="*50)
    print("Установка SecLists...")
    print("="*50)
    
    seclists_dir = "Wordlists/SecLists"
    
    if os.path.exists(seclists_dir):
        print("SecLists уже установлены")
        return True
    
    print("Скачиваю SecLists...")
    try:
        cmd = "git clone --depth 1 https://github.com/danielmiessler/SecLists.git Wordlists/SecLists"
        subprocess.run(cmd, shell=True, check=True)
        print("✓ SecLists успешно установлены")
        
        # Создаем символическую ссылку в /usr/share/seclists для совместимости
        if os.path.exists("/usr/share/seclists"):
            print("Ссылка на /usr/share/seclists уже существует")
        else:
            try:
                # Пытаемся создать символическую ссылку с sudo
                current_dir = os.getcwd()
                cmd = f"sudo ln -sf {current_dir}/Wordlists/SecLists /usr/share/seclists"
                subprocess.run(cmd, shell=True, check=True)
                print("✓ Создана символическая ссылка /usr/share/seclists")
            except:
                print("⚠ Не удалось создать ссылку в /usr/share/seclists. Создайте вручную при необходимости.")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка при установке SecLists: {e}")
        return False

def install_metasploit(package_manager):
    """Устанавливает Metasploit Framework"""
    print("\n" + "="*50)
    print("Установка Metasploit Framework...")
    print("="*50)
    
    # Проверяем, не установлен ли уже Metasploit
    msf_check = subprocess.run(["which", "msfconsole"], capture_output=True)
    if msf_check.returncode == 0:
        print("Metasploit Framework уже установлен")
        
        # Проверяем инициализацию базы данных
        db_check = subprocess.run(["msfdb", "status"], capture_output=True, text=True)
        if "not running" in db_check.stdout or "not initialized" in db_check.stdout:
            print("Инициализируем базу данных Metasploit...")
            subprocess.run(["sudo", "msfdb", "init"], check=False)
        
        return True
    
    print("Установка Metasploit Framework...")
    
    # Устанавливаем зависимости для Metasploit в зависимости от пакетного менеджера
    if package_manager == 'apt':
        print("Установка зависимостей для Metasploit...")
        deps_cmd = "sudo apt install -y libpq-dev postgresql postgresql-contrib libpcap-dev"
        subprocess.run(deps_cmd, shell=True, check=False)
    
    try:
        # Скачиваем и запускаем установщик Metasploit
        print("Скачиваю установщик Metasploit...")
        subprocess.run("curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall", 
                      shell=True, check=True)
        
        print("Устанавливаю Metasploit...")
        subprocess.run("chmod 755 msfinstall", shell=True, check=True)
        subprocess.run("sudo ./msfinstall", shell=True, check=True)
        
        print("Инициализирую базу данных Metasploit...")
        subprocess.run("sudo msfdb init", shell=True, check=True)
        
        print("Очищаю временные файлы...")
        subprocess.run("rm -f msfinstall", shell=True, check=True)
        
        print("✓ Metasploit Framework успешно установлен")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка при установке Metasploit: {e}")
        
        # Альтернативный способ установки через пакетный менеджер
        print("Пробую альтернативный способ установки...")
        
        if package_manager == 'apt':
            alt_cmd = "sudo apt install -y metasploit-framework"
        elif package_manager == 'dnf':
            alt_cmd = "sudo dnf install -y metasploit-framework"
        elif package_manager == 'yum':
            alt_cmd = "sudo yum install -y metasploit-framework"
        elif package_manager == 'pacman':
            alt_cmd = "sudo pacman -S --noconfirm metasploit"
        else:
            print("Не удалось установить Metasploit автоматически")
            return False
        
        try:
            subprocess.run(alt_cmd, shell=True, check=True)
            subprocess.run("sudo msfdb init", shell=True, check=True)
            print("✓ Metasploit Framework установлен через пакетный менеджер")
            return True
        except:
            print("✗ Не удалось установить Metasploit")
            return False

def install_python_requirements(venv_dir):
    """Устанавливает Python зависимости для инструментов в виртуальном окружении"""
    print("\n" + "="*50)
    print("Установка Python зависимостей в виртуальном окружении...")
    print("="*50)
    
    venv_pip = get_venv_pip(venv_dir)
    
    # Сначала устанавливаем общие зависимости
    common_packages = [
        "requests",
        "beautifulsoup4",
        "urllib3",
        "colorama",
        "lxml",
        "pyyaml",
        "tqdm",
        "bs4",
        "dnspython",
        "certifi",
        "charset-normalizer",
        "idna",
        "soupsieve",
    ]
    
    print("Установка общих Python пакетов...")
    for package in common_packages:
        try:
            cmd = f'"{venv_pip}" install {package}'
            subprocess.run(cmd, shell=True, check=True)
            print(f"✓ Установлен: {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Ошибка установки: {package}")
    
    # Затем устанавливаем зависимости из requirements.txt файлов
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "requirements.txt":
                req_path = os.path.join(root, file)
                print(f"Найден requirements.txt: {req_path}")
                try:
                    cmd = f'"{venv_pip}" install -r "{req_path}"'
                    subprocess.run(cmd, shell=True, check=True)
                    print(f"✓ Зависимости установлены для {root}")
                except subprocess.CalledProcessError:
                    print(f"✗ Ошибка установки зависимостей для {root}")
            
            # Устанавливаем зависимости для xlsNinja
            if file == "setup.py" and "xlsNinja" in root:
                print(f"Устанавливаю xlsNinja: {root}")
                try:
                    cmd = f'cd "{root}" && "{venv_pip}" install .'
                    subprocess.run(cmd, shell=True, check=True)
                    print(f"✓ xlsNinja установлен")
                except subprocess.CalledProcessError:
                    print(f"✗ Ошибка установки xlsNinja")

def setup_go_tools():
    """Устанавливает Go инструменты"""
    print("\n" + "="*50)
    print("Установка Go инструментов...")
    print("="*50)
    
    go_tools = [
        "github.com/tomnomnom/assetfinder@latest",
        "github.com/hahwul/dalfox/v2@latest",
        "github.com/projectdiscovery/katana/cmd/katana@latest",
        "github.com/cc1a2b/jshunter@latest",
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        "github.com/projectdiscovery/httpx/cmd/httpx@latest",
        "github.com/Chocapikk/wpprobe@latest",
    ]
    
    for tool in go_tools:
        print(f"Устанавливаю: {tool}")
        try:
            cmd = f"go install {tool}"
            subprocess.run(cmd, shell=True, check=True)
            print(f"✓ Успешно: {tool}")
        except subprocess.CalledProcessError:
            print(f"✗ Ошибка установки: {tool}")

def install_system_tools(package_manager):
    """Устанавливает системные инструменты"""
    print("\n" + "="*50)
    print("Установка системных инструментов...")
    print("="*50)
    
    tools_commands = {
        'apt': [
            "sudo apt update",
            "sudo apt install -y nmap subfinder feroxbuster ffuf golang-go nikto",
            "sudo apt install -y python3-pip curl git wget",
        ],
        'dnf': [
            "sudo dnf update -y",
            "sudo dnf install -y nmap subfinder ffuf golang nikto",
            "sudo dnf install -y python3-pip curl git wget",
            "dnf copr enable atim/rustscan -y && dnf install rustscan -y",
        ],
        'pacman': [
            "sudo pacman -Syu --noconfirm",
            "sudo pacman -S --noconfirm nmap subfinder ffuf go python pip curl git nikto wget",
        ],
        'yum': [
            "sudo yum update -y",
            "sudo yum install -y nmap ffuf golang python3-pip curl git nikto wget",
        ],
        'zypper': [
            "sudo zypper refresh",
            "sudo zypper install -y nmap ffuf go python3-pip curl git nikto wget",
        ]
    }
    
    if package_manager in tools_commands:
        for cmd in tools_commands[package_manager]:
            print(f"Выполняю: {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True)
            except subprocess.CalledProcessError:
                print(f"Ошибка в команде: {cmd}")
                continue

def setup_go_path():
    """Настраивает PATH для Go инструментов"""
    print("\n" + "="*50)
    print("Настройка PATH для Go инструментов...")
    print("="*50)
    
    try:
        result = subprocess.run(["go", "env", "GOPATH"], capture_output=True, text=True, check=True)
        go_path = result.stdout.strip()
        go_bin = os.path.join(go_path, "bin")
        
        if os.path.exists(go_bin):
            print(f"Go bin directory: {go_bin}")
            
            # Проверяем, есть ли уже путь в переменной PATH
            result = subprocess.run(["echo", "$PATH"], shell=True, capture_output=True, text=True)
            current_path = result.stdout.strip()
            
            if go_bin not in current_path:
                print(f"Добавьте этот путь в переменную окружения PATH:")
                print(f'export PATH="$PATH:{go_bin}"')
                print("\nДобавьте эту строку в файл ~/.bashrc или ~/.zshrc для постоянного эффекта")
                
                # Создаем простой скрипт для добавления в PATH
                with open("setup_gopath.sh", "w") as f:
                    f.write(f'#!/bin/bash\n')
                    f.write(f'echo "Adding Go bin to PATH..."\n')
                    f.write(f'export PATH="$PATH:{go_bin}"\n')
                    f.write(f'echo "Go tools should now be available in your PATH"\n')
                
                os.chmod("setup_gopath.sh", 0o755)
                print("✓ Создан setup_gopath.sh для настройки PATH")
            else:
                print("✓ Go bin уже добавлен в PATH")
        else:
            print("Не удалось найти Go bin directory")
            
    except subprocess.CalledProcessError:
        print("Ошибка при определении Go PATH")

def create_venv_activation_info(venv):
    """Создает инструкцию по активации виртуального окружения"""
    print("\n" + "="*50)
    print("Инструкция по активации виртуального окружения:")
    print("="*50)
    
    print(f"\nДля активации виртуального окружения выполните:")
    print(f"source {venv}/bin/activate")
    print(f"\nДля деактивации выполните:")
    print(f"deactivate")
    
    # Создаем простой текстовый файл с инструкциями
    with open("VENV_INSTRUCTIONS.txt", "w") as f:
        f.write("="*60 + "\n")
        f.write("ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ ВИРТУАЛЬНОГО ОКРУЖЕНИЯ\n")
        f.write("="*60 + "\n\n")
        f.write("АКТИВАЦИЯ ВИРТУАЛЬНОГО ОКРУЖЕНИЯ:\n")
        f.write(f"source {venv}/bin/activate\n\n")
        f.write("ДЕАКТИВАЦИЯ:\n")
        f.write("deactivate\n\n")
        f.write("ДОСТУПНЫЕ ПАПКИ С ИНСТРУМЕНТАМИ:\n")
        f.write("- Web_catalog - инструменты сканирования каталогов\n")
        f.write("- Subdomains - инструменты поиска поддоменов\n")
        f.write("- Scaner - сканеры уязвимостей\n")
        f.write("- CMS - инструменты для CMS\n")
        f.write("- SSRF - инструменты для обнаружения SSRF\n")
        f.write("- Open_redirect - инструменты для открытых редиректов\n")
        f.write("- LFI - инструменты для Local File Inclusion\n")
        f.write("- XSS - инструменты для XSS\n")
        f.write("- SQLj - инструменты для SQL инъекций\n")
        f.write("- JS - инструменты для анализа JavaScript\n")
        f.write("- Dorks - инструменты для поиска уязвимостей\n")
        f.write("- Wordlists - словари для брутфорса\n")
    
    print(f"\n✓ Создан файл VENV_INSTRUCTIONS.txt с инструкциями")

def main():
    """Основная функция"""
    show_banner()
    
    # Проверяем что это Linux
    check_linux_system()
    
    # Создаем виртуальное окружение
    venv_dir = create_virtual_environment()
    if not venv_dir:
        print("Не удалось создать виртуальное окружение. Продолжаем без него...")
        venv_dir = None
    
    # Определение пакетного менеджера
    auto_pm = detect_linux_package_manager()
    
    if auto_pm != 'unknown':
        print(f"\n✓ Автоматически определен пакетный менеджер: {auto_pm}")
        use_auto_pm = input("Использовать его? (y/n): ").strip().lower()
        if use_auto_pm == 'y':
            package_manager = auto_pm
        else:
            package_manager = ask_package_manager()
    else:
        print("\nНе удалось определить пакетный менеджер автоматически.")
        package_manager = ask_package_manager()
    
    print(f"\n✓ Выбран пакетный менеджер: {package_manager}")
    
    # Спрашиваем про установку SecLists
    print("\n" + "-"*50)
    seclists_choice = input("Установить SecLists (коллекция wordlists)? (y/n): ").strip().lower()
    
    # Спрашиваем про установку Metasploit
    print("\n" + "-"*50)
    metasploit_choice = input("Установить Metasploit Framework? (y/n): ").strip().lower()
    
    # Выполняем установку
    install_dependencies(package_manager)
    install_system_tools(package_manager)
    create_folders()
    download_tools(venv_dir)
    setup_go_tools()
    
    if seclists_choice == 'y':
        install_seclists()
    
    if metasploit_choice == 'y':
        install_metasploit(package_manager)
    
    if venv_dir:
        install_python_requirements(venv_dir)
        create_venv_activation_info(venv_dir)
    
    setup_go_path()
    
    print("\n" + "="*70)
    print("✓ УСТАНОВКА ЗАВЕРШЕНА!")
    print("="*70)
    
    if venv_dir:
        print(f"\n✓ Виртуальное окружение создано в папке: {venv_dir}")
        print("✓ Для активации окружения выполните: source venv/bin/activate")
        print("✓ Для деактивации: deactivate")
    
    print("\n✓ Все инструменты успешно скачаны в соответствующие папки.")
    
    print(f"\n✓ Использованный пакетный менеджер: {package_manager}")
    
    # Инструкция по добавлению Go инструментов в PATH
    print("\n" + "-"*50)
    print("ИНСТРУКЦИЯ ПО ДОБАВЛЕНИЮ GO ИНСТРУМЕНТОВ В PATH:")
    print("-"*50)
    
    try:
        result = subprocess.run(["go", "env", "GOPATH"], capture_output=True, text=True, check=True)
        go_path = result.stdout.strip()
        go_bin = os.path.join(go_path, "bin")
        
        if os.path.exists(go_bin):
            print(f"\nДобавьте путь к Go инструментам в переменную PATH:")
            print(f'export PATH="$PATH:{go_bin}"')
            print("\nДобавьте эту строку в файл ~/.bashrc или ~/.zshrc для постоянного эффекта")
            print("Или выполните: source setup_gopath.sh")
    
    except:
        pass
    
    if seclists_choice == 'y':
        print("\n✓ SecLists установлены в папке Wordlists/SecLists")
        print("  Для использования в других инструментах: /usr/share/seclists")
    
    if metasploit_choice == 'y':
        print("\n✓ Metasploit Framework установлен")
        print("  Для запуска: msfconsole")
        print("  Для инициализации БД: sudo msfdb init")
        print("  Для проверки статуса БД: msfdb status")
    
    print("\n✓ Установленные инструменты:")
    print("  РАЗВЕДКА (Reconnaissance):")
    print("    - theHarvester - сбор информации о доменах")
    print("    - gitrob - поиск секретов в GitHub")
    print("    - assetfinder - поиск связанных доменов (Go)")
    print("    - subfinder - поиск поддоменов (Go)")
    print("  ")
    print("  СКАНИРОВАНИЕ УЯЗВИМОСТЕЙ:")
    print("    - nuclei - темплейт-базированное сканирование (Go)")
    print("    - nikto - веб-сканер")
    print("    - Metasploit - фреймворк для эксплуатации уязвимостей")
    print("  ")
    print("  WORDLISTS:")
    print("    - SecLists - коллекции словарей для брутфорса")
    print("  ")
    print("  АНАЛИЗ JAVASCRIPT & SECRETS:")
    print("    - SecretFinder - поиск API ключей в JS")
    print("    - JSSteal - извлечение чувствительных данных")
    print("    - Pinkerton - анализ JS на уязвимости")
    print("    - trufflehog - поиск credentials в коде")
    print("  ")
    print("  FUZZING & BRUTE FORCE:")
    print("    - ffuf - быстрый HTTP fuzzer (Go)")
    print("    - feroxbuster - перебор путей")
    print("    - dirsearch - поиск скрытых папок")
    print("  ")
    print("  СПЕЦИАЛИЗИРОВАННЫЕ СКАНЕРЫ:")
    print("    - sqlmap - SQL инъекции")
    print("    - XSStrike - XSS уязвимости")
    print("    - SSRFmap - SSRF уязвимости")
    print("    - LFI Scanner - Local File Inclusion")
    print("  ")
    print("  ДОПОЛНИТЕЛЬНО:")
    print("    - nuclei-templates - готовые шаблоны сканирования")
    
    print("\n РЕКОМЕНДУЕМЫЙ WORKFLOW для Bug Bounty:")
    print("  1. Разведка: theHarvester → subfinder → assetfinder → httpx")
    print("  2. Поиск секретов: gitrob → SecretFinder → JSSteal → trufflehog")
    print("  3. Fuzzing: ffuf → feroxbuster → dirsearch (с использованием SecLists)")
    print("  4. Сканирование: nuclei → nikto")
    print("  5. Эксплуатация: Metasploit для известных уязвимостей")
    
    print("\n" + "="*70)
    print("Спасибо за использование BugBounty-script!")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nУстановка прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Ошибка: {e}")
        sys.exit(1)