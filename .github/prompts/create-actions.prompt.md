---
agent: agent
description: "Створи кросплатформний GitHub Actions workflow за skill github-actions."
---

# Передумови

- Робочий каталог — корінь проєкту.
- Прочитай skill `github-actions` із
  `.github/skills/github-actions/SKILL.md`.
- Переконайся, що `ci.sh` і `ci.bat` доступні; workflow має викликати ці
  скрипти, а не дублювати їхню логіку.

# Дії

1. Виконай інструкції skill `github-actions`.
2. Створи workflow із тригерами `push` і `pull_request`, кожен обмежений
   гілками `develop` і `main`.
3. Додай рівно одну job із matrix `ubuntu-latest`, `windows-latest` і
   `macos-latest`, кроки checkout та setup Python `3.11`.
4. Запускай `./ci.sh` на Linux/macOS за умови `if: runner.os != 'Windows'`
   і `ci.bat` на Windows за умови `if: runner.os == 'Windows'`.
5. Додай завантаження `dist/` через `actions/upload-artifact`, назва
   артефакту має враховувати ОС.
6. Не додавай branch-based умови чи кроки, що можуть пропустити CI за
   назвою гілки, подією або результатом іншого кроку. Для виконання скриптів
   дозволені лише platform-specific умови на `runner.os`.
7. Перевір YAML, структуру job, matrix, тригери та відсутність умов
   пропуску за гілкою.

# Очікувані файли

- `.github/workflows/ci.yml` — одна job із матрицею трьох ОС, Python 3.11,
  безумовними щодо гілок platform-specific CI-кроками та завантаженням
  `dist/`.

# Команди перевірки

Перевір валідність YAML і підтверди, що:

- обидва тригери обмежені гілками `develop` і `main`;
- workflow має рівно одну job із усіма трьома ОС;
- є кроки checkout, setup-python версії `3.11` та upload-artifact для
  `dist/`;
- команди `./ci.sh` і `ci.bat` запускаються лише відповідно до ОС runner;
- жодна job або step не має branch-based `if`-умови чи умови на вихід
  іншого кроку;
- YAML не дублює встановлення залежностей, pytest або PyInstaller.

# Повідомлення про помилку

Якщо `ci.sh` або `ci.bat` відсутній, YAML невалідний чи будь-яка вимога не
виконана, повідом конкретну причину й зупинись. Не перенось логіку збирання
до workflow і не заявляй про проходження перевірок без результату.

# Ідемпотентність

Перед зміною прочитай наявний workflow. Внось лише необхідні зміни;
повторний запуск не створює дубльованих job, тригерів чи кроків.
