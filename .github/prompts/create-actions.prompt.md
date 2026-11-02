---
agent: agent
description: "Створи кросплатформний GitHub Actions workflow за skill github-actions."
---

# Передумови

- Робочий каталог — корінь проєкту.
- Прочитай skill `github-actions` із
  `.github/skills/github-actions/SKILL.md`.
- Переконайся, що CI-скрипти `ci.sh` і `ci.bat` та сканер
  `.github/scripts/detect_base_branch.py` доступні; workflow має викликати
  їх, а не дублювати їхню логіку.

# Дії

1. Виконай інструкції skill `github-actions`.
2. Увімкни `push` для всіх гілок і `pull_request` для всіх цільових гілок;
   не задавай фіксований список на кшталт `master` або `main`.
3. Переконайся, що scanner читає payload GitHub event, визначає
   `repository.default_branch` і відрізняє push у базову гілку від PR,
   націленого на неї. Сканер має записати `run_ci` у `GITHUB_OUTPUT`.
4. Додай одну job із matrix трьох ОС, checkout і Python `3.11`, виконай
   scanner та запускай платформний CI-скрипт і upload-artifact лише якщо
   scanner дозволив CI.
5. Не додавай логіку збирання до YAML і не використовуй API, секрети або
   токени.

# Очікувані файли

- `.github/workflows/ci.yml` — одна job із `ubuntu-latest`,
  `windows-latest` та `macos-latest`, налаштування Python 3.11, сканер
  базової гілки, умовні виклики CI-скриптів і завантаження `dist/`.
- `.github/scripts/detect_base_branch.py` — scanner базової гілки.
- `tests/test_detect_base_branch.py` — тести рішень scanner для push, PR і
  некоректного payload.

# Команди перевірки

Запусти targeted pytest для scanner і перевір валідність YAML парсером,
доступним у середовищі. Переконайся, що:

- є тригери `push` та `pull_request`, а зміни в логіці не залежать від
  назви `master` чи `main`;
- scanner дозволяє збірку лише для push у `repository.default_branch` або PR,
  націленого на цю гілку, і повертає помилку для некоректних даних;
- є рівно одна job і всі три ОС у matrix;
- виклики shell і batch-скриптів перевіряють scanner output і мають правильні
  умови runner OS;
- workflow використовує actions checkout, setup-python версії `3.11` та
  upload-artifact для `dist/`;
- workflow не містить команд встановлення залежностей, pytest або PyInstaller.

# Повідомлення про помилку

Якщо skill, scanner або потрібні CI-скрипти відсутні, YAML невалідний чи
будь-яка вимога не виконана, повідом конкретну причину й зупинись. Не
перенось логіку збирання до workflow і не заявляй про проходження перевірок
без результату.

# Ідемпотентність

Перед зміною прочитай наявні workflow і scanner. Внось лише необхідні зміни;
повторний запуск не створює дубльованих job, тригерів чи кроків. Не
вбудовуй назву базової гілки в конфігурацію: визначай її з payload кожної
події.
