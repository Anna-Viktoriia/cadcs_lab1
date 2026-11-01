---
name: github-actions
description: "Створюй і перевіряй GitHub Actions CI workflow для Python-проєкту на Linux, Windows і macOS. Застосовуй під час налаштування .github/workflows/ci.yml."
---

# Призначення

Створити або перевірити GitHub Actions workflow, що запускає наявні скрипти
збирання та перевірки проєкту на Linux, Windows і macOS. Workflow лише
викликає `ci.sh` або `ci.bat`; логіку встановлення залежностей, тестування та
пакування зберігай у цих скриптах.

# Вхід

- Python-проєкт із `ci.sh` для Linux/macOS і `ci.bat` для Windows.
- Гілки для CI: `develop` і `master`.
- Python: версія `3.11`.
- Матриця операційних систем: `ubuntu-latest`, `windows-latest`,
  `macos-latest`.

# Вихід

Підготуй `.github/workflows/ci.yml` з:

- тригерами `push` і `pull_request` лише для гілок `develop` та `master`;
- рівно однією job із матрицею `os: [ubuntu-latest, windows-latest,
  macos-latest]`;
- кроками `actions/checkout`, `actions/setup-python` з `python-version: '3.11'`,
  запуском платформного CI-скрипту та завантаженням артефакту `dist/` через
  `actions/upload-artifact`;
- запуском `./ci.sh` на Linux/macOS за умови `if: runner.os != 'Windows'`;
- запуском `ci.bat` на Windows за умови `if: runner.os == 'Windows'`.

Workflow не повинен містити команд встановлення залежностей, запуску pytest
чи PyInstaller: ці дії належать `ci.sh` і `ci.bat`. Не використовуй секрети,
токени чи credentials.

# Кроки

1. Перевір наявний `.github/workflows/ci.yml` і CI-скрипти. Не перезаписуй
   наявний workflow без перевірки; внеси лише мінімальні зміни, необхідні для
   відповідності цим вимогам.
2. Якщо workflow відсутній, створи його з двома тригерами та фільтром гілок
   `develop` і `master`.
3. Додай одну job, яка використовує matrix із трьома вказаними ОС.
4. Додай кроки checkout репозиторію та налаштування Python версії `3.11`.
5. Додай умовні кроки виконання `./ci.sh` на Linux/macOS і `ci.bat` на
   Windows. Не дублюй у YAML дії, які вже виконує CI-скрипт.
6. Після завершення CI-скрипту додай крок
   `actions/upload-artifact` для каталогу `dist/`. Задай зрозумілу назву
   артефакту, що враховує ОС із матриці.
7. Перевір синтаксис YAML і підтверди, що матриця містить усі три ОС та
   workflow містить рівно одну job.
8. Повідом про змінені файли та результат перевірок.

# Перевірки

- `.github/workflows/ci.yml` є валідним YAML.
- Тригери включають `push` і `pull_request`, кожен обмежений гілками
  `develop` і `master`.
- Workflow має одну job і matrix рівно з `ubuntu-latest`, `windows-latest` та
  `macos-latest`.
- Крок запуску `./ci.sh` має умову `if: runner.os != 'Windows'`, а крок
  `ci.bat` — `if: runner.os == 'Windows'`.
- Workflow налаштовує Python `3.11` та завантажує `dist/` через
  `actions/upload-artifact`.
- Workflow не містить логіки збирання і не використовує секрети.

# Типова помилка

Якщо `ci.sh` або `ci.bat` відсутній, не підмінюй його логіку командами
збирання в workflow. Повідом про відсутній файл і зупинись або попроси
завершити відповідний етап налаштування CI-скриптів.

# Приклад

**Вхід**

```text
Створи CI workflow для Python 3.11 на Ubuntu, Windows і macOS.
Запускай на push та pull request у develop і master.
```

**Очікуваний результат**

Файл `.github/workflows/ci.yml` має дві події-тригери з фільтром гілок,
одну job з матрицею трьох ОС, кроки checkout і setup-python, умовний виклик
платформного CI-скрипту та завантаження `dist/`. Усі команди збирання та
тестування залишаються в `ci.sh` і `ci.bat`.
