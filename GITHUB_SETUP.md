# 🚀 Інструкції для створення GitHub репозиторію

## Крок 1: Створення репозиторію на GitHub

### Варіант A: Через веб-інтерфейс (Рекомендовано)

1. Відкрийте https://github.com/new
2. Заповніть форму:
   - **Repository name:** `law-analyse`
   - **Description:** `AI-powered Ukrainian law analysis platform with GPT-4o`
   - **Visibility:** Public
   - **НЕ додавайте:** README, .gitignore, license (вони вже є)
3. Натисніть **"Create repository"**

### Варіант B: Через GitHub CLI (якщо встановлено)

```bash
cd D:\server\OpenServer\domains\LawAnalyse\www
gh repo create law-analyse --public --source=. --push
```

## Крок 2: Підключення локального репозиторію

```bash
cd D:\server\OpenServer\domains\LawAnalyse\www

# Додати remote
git remote add origin https://github.com/YOUR-USERNAME/law-analyse.git

# Перейменувати branch на main (якщо потрібно)
git branch -M main

# Push код
git push -u origin main
```

## Крок 3: Налаштування GitHub репозиторію

### 3.1 Додати Topics (теги)

На сторінці репозиторію натисніть ⚙️ біля "About" та додайте:
- `legal-tech`
- `ai`
- `nlp`
- `ukrainian-law`
- `fastapi`
- `astro`
- `react`
- `gpt-4`
- `langchain`

### 3.2 Налаштувати Secrets (для GitHub Actions)

Settings → Secrets and variables → Actions → New repository secret:

- **Name:** `OPENAI_API_KEY`
- **Value:** `sk-your-openai-key-here`

### 3.3 Увімкнути GitHub Actions

Actions → "I understand my workflows, go ahead and enable them"

### 3.4 Налаштувати Branch Protection (опціонально)

Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging
  - Select: `test`, `build-backend`, `build-frontend`

### 3.5 Додати Description та Website

Settings → General:
- **Description:** `🤖 AI-powered platform for analyzing Ukrainian laws using GPT-4o with adversarial review`
- **Website:** `https://law-analyse.vercel.app` (після deployment)

## Крок 4: Створити перший Release

1. Перейдіть на Releases → "Create a new release"
2. Заповніть:
   - **Tag:** `v1.0.0`
   - **Release title:** `v1.0.0 - MVP Release`
   - **Description:**
     ```markdown
     ## 🎉 Law Analyse MVP - First Release
     
     ### Features
     - ✅ PDF parsing for Ukrainian laws
     - ✅ AI extraction with 2-agent adversarial review
     - ✅ Confidence scoring and human review flags
     - ✅ Plain language explanations
     - ✅ Interactive article tree UI
     - ✅ Docker support
     
     ### Tech Stack
     - Backend: FastAPI + Python 3.11
     - Frontend: Astro + React + TypeScript
     - AI: OpenAI GPT-4o
     - Database: PostgreSQL
     
     ### Deployment
     See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions.
     
     ### Quick Start
     ```bash
     ./setup.sh
     ./dev.sh
     ```
     
     See [QUICKSTART.md](QUICKSTART.md) for details.
     ```
3. Натисніть **"Publish release"**

## Крок 5: Додати README badges

Відредагуйте `README.md` та додайте на початок:

```markdown
# Law Analyse

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![Backend Tests](https://github.com/YOUR-USERNAME/law-analyse/actions/workflows/backend-tests.yml/badge.svg)](https://github.com/YOUR-USERNAME/law-analyse/actions/workflows/backend-tests.yml)
[![Docker Build](https://github.com/YOUR-USERNAME/law-analyse/actions/workflows/docker-build.yml/badge.svg)](https://github.com/YOUR-USERNAME/law-analyse/actions/workflows/docker-build.yml)
```

Commit та push:
```bash
git add README.md
git commit -m "docs: add badges to README"
git push
```

## Крок 6: Створити Project Board (опціонально)

Projects → New project → Board:
- **Name:** `Law Analyse Roadmap`
- **Columns:** 
  - 📋 Backlog
  - 🚧 In Progress
  - ✅ Done

Додайте issues для майбутніх features з `CHANGELOG.md`.

## Крок 7: Налаштувати Discussions

Settings → General → Features:
- ✅ Discussions

Categories:
- 💡 Ideas
- 🙏 Q&A
- 📣 Announcements
- 🐛 Bug Reports

## Крок 8: Додати Social Preview

Settings → General → Social preview:
- Upload image (1280x640px) з логотипом та назвою проєкту

## Крок 9: Перевірити все працює

1. **GitHub Actions:** Actions → Перевірте, що workflows запустилися
2. **Issues:** Issues → Перевірте templates
3. **README:** Перевірте, що все відображається правильно
4. **License:** Перевірте, що MIT license відображається

## Крок 10: Поділитися проєктом

Створіть пост на:
- Twitter/X: `#LegalTech #AI #Ukraine`
- LinkedIn: Поділіться з професійною мережею
- Reddit: r/legaltech, r/ukraine
- Dev.to: Напишіть статтю про розробку

---

## ✅ Checklist

- [ ] Репозиторій створено на GitHub
- [ ] Код запушено (`git push -u origin main`)
- [ ] Topics додано
- [ ] Secrets налаштовано (OPENAI_API_KEY)
- [ ] GitHub Actions увімкнено
- [ ] Description та Website додано
- [ ] Release v1.0.0 створено
- [ ] README badges додано
- [ ] Discussions увімкнено (опціонально)
- [ ] Project board створено (опціонально)

---

## 🎯 Наступний крок: Deployment

Після створення GitHub репозиторію, переходьте до:
- **DEPLOYMENT.md** - для production deployment на Railway + Vercel
- **DOCKER.md** - для Docker deployment

---

**Час виконання:** ~10-15 хвилин

**Результат:** Повністю налаштований GitHub репозиторій з CI/CD
