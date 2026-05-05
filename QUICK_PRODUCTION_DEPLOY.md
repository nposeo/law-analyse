# 🚀 ШВИДКИЙ СТАРТ - Production Deployment

## ⏱️ Час: 1-2 години | Вартість: $0/місяць

---

## 📋 ЩО ВАМ ПОТРІБНО

1. ✅ GitHub акаунт (вже є)
2. ⏳ OpenAI API key (https://platform.openai.com/api-keys)
3. ⏳ Neon акаунт (https://neon.tech)
4. ⏳ Railway акаунт (https://railway.app)
5. ⏳ Vercel акаунт (https://vercel.com)

**Всі сервіси мають безкоштовні тарифи!**

---

## 🎯 КРОК 1: GITHUB (5 хвилин)

### Додати Topics

**URL:** https://github.com/nposeo/law-analyse

1. Клікніть ⚙️ біля "About"
2. Додайте topics (Enter після кожного):
   - legal-tech
   - ai
   - nlp
   - ukrainian-law
   - fastapi
   - astro
   - react
   - typescript
   - python
   - openai
   - gpt-4
   - langchain
   - postgresql
   - docker

3. Description: `AI-powered Ukrainian law analysis platform with GPT-4o`
4. Save

### Додати Secret

**URL:** https://github.com/nposeo/law-analyse/settings/secrets/actions

1. New repository secret
2. Name: `OPENAI_API_KEY`
3. Value: ваш ключ з https://platform.openai.com/api-keys
4. Add secret

✅ **Крок 1 завершено!**

---

## 🎯 КРОК 2: RELEASE (5 хвилин)

**URL:** https://github.com/nposeo/law-analyse/releases/new

**Tag:** `v1.0.0`  
**Title:** `Law Analyse MVP v1.0.0`  
**Description:** Скопіюйте з `RELEASE_NOTES_v1.0.0.md`

✅ Set as latest release  
🚀 Publish release

✅ **Крок 2 завершено!**

---

## 🎯 КРОК 3: DATABASE (10 хвилин)

**URL:** https://console.neon.tech/signup

1. Створіть акаунт
2. Create project: `law-analyse-db`
3. Region: Europe
4. PostgreSQL: 16
5. **СКОПІЮЙТЕ connection string:**
   ```
   postgresql://user:pass@host/db
   ```

✅ **Крок 3 завершено!** Збережіть connection string!

---

## 🎯 КРОК 4: BACKEND (20 хвилин)

**URL:** https://railway.app/new

1. Створіть акаунт
2. Deploy from GitHub repo
3. Виберіть `nposeo/law-analyse`
4. Deploy
5. Settings → Root Directory: `backend`
6. Variables → Add:
   - `DATABASE_URL`: (з Neon)
   - `OPENAI_API_KEY`: (ваш ключ)
   - `PORT`: `8000`
   - `CORS_ORIGINS`: `https://law-analyse.vercel.app`
7. Deploy
8. Settings → Networking → Generate Domain
9. **СКОПІЮЙТЕ URL:**
   ```
   https://law-analyse-backend.up.railway.app
   ```

**Тест:** Відкрийте `https://your-backend.up.railway.app/docs`

✅ **Крок 4 завершено!** Збережіть backend URL!

---

## 🎯 КРОК 5: МІГРАЦІЇ (5 хвилин)

**На вашому комп'ютері:**

```bash
# Windows
set DATABASE_URL=postgresql://user:pass@host/db
cd backend
pip install alembic psycopg2-binary
alembic upgrade head
```

**Перевірка:**
```bash
psql "postgresql://user:pass@host/db" -c "\dt"
```

Має показати: laws, articles, norms, alembic_version

✅ **Крок 5 завершено!**

---

## 🎯 КРОК 6: FRONTEND (15 хвилин)

**URL:** https://vercel.com/signup

1. Створіть акаунт
2. Add New → Project
3. Import `nposeo/law-analyse`
4. Configure:
   - Framework: Astro
   - Root Directory: `frontend`
5. Environment Variables:
   - `PUBLIC_API_URL`: (ваш Railway URL)
6. Deploy
7. **СКОПІЮЙТЕ URL:**
   ```
   https://law-analyse.vercel.app
   ```

✅ **Крок 6 завершено!** Збережіть frontend URL!

---

## 🎯 КРОК 7: CORS (2 хвилини)

**Поверніться на Railway:**

1. Ваш проект → backend service
2. Variables → `CORS_ORIGINS`
3. Edit → Вставте ваш Vercel URL
4. Update

✅ **Крок 7 завершено!**

---

## 🎉 ГОТОВО!

### Перевірте:

**Frontend:**
```
https://law-analyse.vercel.app
```

**Backend:**
```
https://law-analyse-backend.up.railway.app/docs
```

### Має працювати:
- ✅ Frontend завантажується
- ✅ Немає помилок в консолі
- ✅ API docs відкриваються

---

## 📝 ЗБЕРЕЖІТЬ ЦІ URL:

```
Repository:  https://github.com/nposeo/law-analyse
Frontend:    https://law-analyse.vercel.app
Backend:     https://law-analyse-backend.up.railway.app
API Docs:    https://law-analyse-backend.up.railway.app/docs
Database:    [Neon Console]
```

---

## 🆘 ПОТРІБНА ДОПОМОГА?

**Детальні інструкції:**
- `PRODUCTION_DEPLOYMENT_READY.md` - Повний гайд
- `STEP_BY_STEP_DEPLOYMENT.md` - Покрокові інструкції
- `DEPLOYMENT_CHECKLIST.md` - Checklist

**Підтримка:**
- GitHub Issues: https://github.com/nposeo/law-analyse/issues
- Email: nposeo@gmail.com

---

**Час:** 1-2 години  
**Вартість:** $0/місяць  
**Складність:** Середня

🚀 **Почніть з Кроку 1!**

🇺🇦 **Making Ukrainian laws accessible to everyone through AI**
