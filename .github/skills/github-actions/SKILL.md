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
- Скрипт `.github/scripts/detect_base_branch.py`, який читає payload події
  GitHub та визначає гілку за замовчуванням репозиторію.
- Python: версія `3.11`.
- Матриця операційних систем: `ubuntu-latest`, `windows-latest`,
  `macos-latest`.

# Вихід

Підготуй `.github/workflows/ci.yml` з:

- тригерами `push` для гілок і `pull_request` для всіх цільових гілок;
- кроком-сканером, який визначає гілку за замовчуванням із payload події
  GitHub і дозволяє збірку лише для push у цю гілку або PR, націленого на неї;
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

1. Перевір наявний workflow, scanner і CI-скрипти. Не перезаписуй наявні
   файли без перевірки; внеси лише мінімальні необхідні зміни.
2. Увімкни `push` для всіх гілок і `pull_request` для всіх цільових гілок.
   Статичні фільтри не можуть використовувати результат сканера під час
   виконання, тому базову гілку фільтруй кроками job.
3. Переконайся, що сканер порівнює `repository.default_branch` із гілкою
   push або базовою гілкою PR, записує булевий результат у `GITHUB_OUTPUT`
   і повертає помилку для некоректного payload.
4. Додай одну job із matrix трьох вказаних ОС, checkout і налаштування Python
   версії `3.11`, після чого виклич сканер.
5. Запускай `./ci.sh`, `ci.bat` і upload-artifact лише коли вихід сканера
   вказує, що подія стосується базової гілки. Не дублюй у YAML логіку CI-
   скриптів.
6. Перевір синтаксис YAML, умови кроків і тести сканера. Повідом про змінені
   файли та результати перевірок.

# Перевірки

- `.github/workflows/ci.yml` є валідним YAML.
- Workflow запускається для push-гілок і цільових гілок PR; сканер пропускає
  CI для подій поза гілкою за замовчуванням репозиторію.
- Сканер визначає default branch із payload події, не використовує API,
  токени чи секрети та явно завершується помилкою на невалідних даних.
- Workflow має одну job і matrix рівно з `ubuntu-latest`, `windows-latest` та
  `macos-latest`.
- Крок запуску `./ci.sh` перевіряє результат сканера та має умову
  `runner.os != 'Windows'`; крок `ci.bat` аналогічно має умову
  `runner.os == 'Windows'`.
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
Створи CI workflow для Python 3.11 на Ubuntu, Windows і macOS. Запускай на
push та pull request; перед CI визначай default branch за payload GitHub event.
```

**Очікуваний результат**

Файл `.github/workflows/ci.yml` має дві події-тригери, одну job з матрицею
трьох ОС, кроки checkout, setup-python і сканер базової гілки. Платформний
CI-скрипт та завантаження `dist/` виконуються лише для базової гілки. Усі
команди збирання та тестування залишаються в `ci.sh` і `ci.bat`.
