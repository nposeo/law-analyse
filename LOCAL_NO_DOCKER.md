# 🚀 Law Analyse - Локальний запуск БЕЗ Docker

## Ситуація
Docker не запускається, але у вас є:
- ✅ Python 3.12.2
- ✅ Node.js 22.22.2
- ✅ OpenServer (з MySQL/MariaDB)

## Рішення: Запуск без Docker

### Варіант 1: Тільки Frontend (Demo Mode)

Запустити тільки інтерфейс для перегляду дизайну:

```bash
cd frontend
npm install
npm run dev
```

Відкрийте: http://localhost:4321

**Що працюватиме:**
- ✅ Інтерфейс
- ✅ Навігація
- ❌ API запити (backend не запущено)
- ❌ Обробка законів

---

### Варіант 2: Frontend + Backend (без AI)

#### Крок 1: Встановіть PostgreSQL

**Швидкий спосіб (portable):**
1. Завантажте: https://www.enterprisedb.com/download-postgresql-binaries
2. Розпакуйте в `D:\PostgreSQL`
3. Ініціалізуйте:
   ```bash
   D:\PostgreSQL\bin\initdb.exe -D D:\PostgreSQL\data
   ```
4. Запустіть:
   ```bash
   D:\PostgreSQL\bin\pg_ctl.exe -D D:\PostgreSQL\data start
   ```
5. Створіть базу:
   ```bash
   D:\PostgreSQL\bin\createdb.exe -U postgres law_analyse
   ```

**Або використайте OpenServer PostgreSQL addon** (якщо є)

#### Крок 2: Налаштуйте Backend

```bash
cd backend

# Створіть віртуальне середовище
python -m venv .venv

# Активуйте
.venv\Scripts\activate

# Встановіть залежності
pip install -r requirements.txt

# Налаштуйте .env
echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/law_analyse > .env
echo OPENAI_API_KEY=sk-test-dummy-key >> .env
echo PORT=8000 >> .env
echo ENVIRONMENT=development >> .env

# Запустіть міграції
alembic upgrade head

# Запустіть сервер
uvicorn app.main:app --reload
```

Backend буде на: http://localhost:8000

#### Крок 3: Запустіть Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend буде на: http://localhost:4321

---

### Варіант 3: Використати SQLite замість PostgreSQL

Найпростіший варіант - без встановлення PostgreSQL:

#### Змініть backend/.env:
```bash
DATABASE_URL=sqlite:///./law_analyse.db
OPENAI_API_KEY=sk-test-dummy-key
PORT=8000
ENVIRONMENT=development
```

#### Встановіть SQLite драйвер:
```bash
cd backend
.venv\Scripts\activate
pip install aiosqlite
```

#### Запустіть:
```bash
# Backend
cd backend
.venv\Scripts\activate
alembic upgrade head
uvicorn app.main:app --reload

# Frontend (в іншому терміналі)
cd frontend
npm run dev
```

---

## Швидкий старт (Рекомендовано)

**Найпростіший спосіб - тільки Frontend:**

```bash
cd D:\server\OpenServer\domains\LawAnalyse\www\frontend
npm install
npm run dev
```

Відкрийте: http://localhost:4321

Ви побачите інтерфейс застосунку (без функціональності обробки законів).

---

## Що робити з Docker?

Docker Desktop може не запускатися через:
1. Не встановлено WSL2
2. Віртуалізація вимкнена в BIOS
3. Конфлікт з іншим ПЗ
4. Недостатньо прав

**Рішення:**
- Використайте локальний запуск (варіанти вище)
- Або виправте Docker пізніше

---

## Наступні кроки

Оберіть варіант:
1. **Demo Mode** - тільки frontend (5 хв)
2. **Full Local** - frontend + backend + PostgreSQL (30 хв)
3. **SQLite Mode** - frontend + backend + SQLite (15 хв)

Який варіант спробуємо?
