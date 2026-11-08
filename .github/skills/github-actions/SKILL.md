---
name: github-actions
description: "Створюй і перевіряй GitHub Actions workflow для Python-проєкту на Linux, Windows і macOS."
---

# Призначення

Створити або перевірити GitHub Actions workflow, що запускає наявні скрипти
збирання та перевірки проєкту на Linux, Windows і macOS. Workflow лише
викликає `ci.sh` або `ci.bat`; логіку встановлення залежностей, тестування та
пакування зберігай у цих скриптах.

# Вхід

- Python-проєкт із `ci.sh` для Linux/macOS і `ci.bat` для Windows.
- Python: версія `3.11`.
- Цільові гілки CI: `develop` і `main`.
- Матриця операційних систем: `ubuntu-latest`, `windows-latest`,
  `macos-latest`.

# Вихід

Підготуй `.github/workflows/ci.yml` з:

- тригерами `push` і `pull_request`, обмеженими гілками `develop` та `main`;
- рівно однією job із матрицею `os: [ubuntu-latest, windows-latest,
  macos-latest]`;
- кроками `actions/checkout`, `actions/setup-python` з `python-version: '3.11'`,
  запуском платформного CI-скрипту та завантаженням артефакту `dist/` через
  `actions/upload-artifact`;
- запуском `./ci.sh` на Linux/macOS за умови `if: runner.os != 'Windows'`;
- запуском `ci.bat` на Windows за умови `if: runner.os == 'Windows'`.

Не додавай branch-based `if`-умови для job, CI-скриптів або завантаження
артефакту. Кожне відповідне push або pull request у `develop` чи `main` має
запускати CI на всіх трьох ОС. Не додавай кроків, які перевіряють назву
гілки або вирішують, чи пропускати збірку. Не використовуй секрети, токени
чи credentials.

# Кроки

1. Перевір наявний workflow і CI-скрипти. Не перезаписуй наявний workflow без
   перевірки; внеси лише мінімальні зміни, необхідні для вимог.
2. Якщо workflow відсутній, створи його з тригерами `push` і
   `pull_request`, кожен лише для `develop` та `main`.
3. Додай одну job із матрицею трьох вказаних ОС, checkout і налаштуванням
   Python `3.11`.
4. Додай умовні кроки запуску `./ci.sh` на Linux/macOS та `ci.bat` на
   Windows. Умови мають залежати лише від `runner.os`, не від гілки, події
   або результату іншого кроку.
5. Після CI-скрипту додай крок `actions/upload-artifact` для `dist/` з
   назвою, що враховує ОС із матриці. Не додавай для нього умову, що може
   пропустити крок через назву гілки.
6. Перевір синтаксис YAML, тригери, матрицю та умови всіх job і steps.

# Перевірки

- `.github/workflows/ci.yml` є валідним YAML.
- Тригери включають `push` і `pull_request`, кожен обмежений гілками
  `develop` та `main`.
- Workflow має одну job і матрицю рівно з `ubuntu-latest`,
  `windows-latest` та `macos-latest`.
- Workflow налаштовує Python `3.11` та завантажує `dist/` через
  `actions/upload-artifact`.
- `./ci.sh` виконується на Linux/macOS, а `ci.bat` — на Windows. Їхні
  єдині `if`-умови перевіряють `runner.os`.
- Жоден job чи step не має branch-based умови або залежності від результату
  іншого кроку; жодна цільова гілка не може пропустити CI через step condition.
- Workflow не містить логіки встановлення залежностей, тестування чи
  пакування і не використовує секрети.

# Типова помилка

Якщо `ci.sh` або `ci.bat` відсутній, не підмінюй його логіку командами
збирання у workflow. Повідом про відсутній файл і зупинись.

# Ідемпотентність

Перед зміною прочитай наявний workflow і перевір наявність CI-скриптів.
Внось лише необхідні зміни; повторний запуск не створює дубльованих job,
тригерів чи кроків.
