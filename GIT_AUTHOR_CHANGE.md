# Зміна автора комітів на nposeo

## Поточна ситуація

Всі 12 комітів зроблені під акаунтом `evolldevteam <evollapp@gmail.com>`.

Тепер Git налаштований для майбутніх комітів:
- **Username:** nposeo
- **Email:** nposeo@gmail.com

## Опції

### Варіант 1: Залишити як є (Рекомендовано)

Залишити історію комітів з evolldevteam, але всі нові коміти будуть від nposeo.

**Плюси:**
- Не потрібно переписувати історію
- Безпечно
- Швидко

**Мінуси:**
- В історії буде два автори

### Варіант 2: Переписати історію комітів

Змінити автора всіх 12 комітів на nposeo.

**Команда:**
```bash
cd D:/server/OpenServer/domains/LawAnalyse/www

git filter-branch --env-filter '
OLD_EMAIL="evollapp@gmail.com"
CORRECT_NAME="nposeo"
CORRECT_EMAIL="nposeo@gmail.com"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```

**Плюси:**
- Вся історія від одного автора

**Мінуси:**
- Переписує всю історію Git
- Потрібен force push
- Може бути проблематично, якщо хтось вже клонував репозиторій

## Рекомендація

Для нового проєкту (ще не запушеного на GitHub) **рекомендую Варіант 1** - залишити як є.

Причини:
1. Історія показує реальний процес розробки
2. Безпечно - не потрібно force push
3. Не важливо для нового проєкту
4. Всі майбутні коміти будуть від nposeo

## Наступний крок

Після вибору варіанту:

```bash
# Push на GitHub
git push -u origin main
```

Repository: https://github.com/nposeo/law-analyse
