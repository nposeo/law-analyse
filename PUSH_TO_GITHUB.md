# 🚀 Push код на GitHub (nposeo)

## Швидкий старт

```bash
cd D:\server\OpenServer\domains\LawAnalyse\www

# Перевірити поточний стан
git status
git log --oneline -5

# Push на GitHub
git push -u origin main
```

## Якщо виникають помилки

### Помилка: "remote origin already exists"

```bash
# Видалити старий remote
git remote remove origin

# Додати новий
git remote add origin https://github.com/nposeo/law-analyse.git

# Push
git push -u origin main
```

### Помилка: "Authentication failed"

**Варіант 1: Personal Access Token (Рекомендовано)**

1. Перейдіть на https://github.com/settings/tokens
2. Generate new token (classic)
3. Виберіть scopes: `repo`, `workflow`
4. Скопіюйте token

```bash
# При push використайте token замість пароля
git push -u origin main
# Username: nposeo
# Password: [ваш token]
```

**Варіант 2: SSH Key**

```bash
# Згенерувати SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Додати до ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Скопіювати публічний ключ
cat ~/.ssh/id_ed25519.pub

# Додати на GitHub: Settings → SSH and GPG keys → New SSH key
```

Змінити remote на SSH:
```bash
git remote set-url origin git@github.com:nposeo/law-analyse.git
git push -u origin main
```

### Помилка: "Repository not found"

Спочатку створіть репозиторій на GitHub:

1. Відкрийте https://github.com/new
2. Repository name: `law-analyse`
3. Public
4. НЕ додавайте README, .gitignore, license
5. Create repository

Потім push:
```bash
git push -u origin main
```

## Перевірка після push

1. Відкрийте https://github.com/nposeo/law-analyse
2. Перевірте, що всі файли завантажені
3. Перевірте, що GitHub Actions запустилися (Actions tab)
4. Перевірте README відображається правильно

## Наступні кроки

Після успішного push:

1. ✅ Налаштувати Secrets для GitHub Actions
2. ✅ Створити Release v1.0.0
3. ✅ Deploy на Railway + Vercel
4. ✅ Додати badges до README

Детальні інструкції: `GITHUB_SETUP.md`

---

**Repository URL:** https://github.com/nposeo/law-analyse
