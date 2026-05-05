# Contributing to Law Analyse

Дякуємо за інтерес до проєкту! Ми раді будь-якому внеску.

## Як допомогти

### 🐛 Повідомити про баг

1. Перевірте, чи баг вже не reported в [Issues](https://github.com/YOUR-USERNAME/law-analyse/issues)
2. Створіть новий issue з детальним описом:
   - Кроки для відтворення
   - Очікувана поведінка
   - Фактична поведінка
   - Скріншоти (якщо можливо)
   - Версія Python, Node.js, OS

### 💡 Запропонувати функцію

1. Створіть issue з тегом `enhancement`
2. Опишіть:
   - Проблему, яку вирішує функція
   - Запропоноване рішення
   - Альтернативи, які ви розглядали

### 🔧 Внести код

1. **Fork** репозиторій
2. **Clone** ваш fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/law-analyse.git
   cd law-analyse
   ```

3. **Створіть branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Внесіть зміни**:
   - Дотримуйтесь стилю коду (див. нижче)
   - Додайте тести для нової функціональності
   - Оновіть документацію

5. **Запустіть тести**:
   ```bash
   cd backend
   pytest
   ```

6. **Commit** змін:
   ```bash
   git commit -m "feat: add new feature"
   ```
   
   Формат commit messages:
   - `feat:` - нова функція
   - `fix:` - виправлення бага
   - `docs:` - зміни в документації
   - `test:` - додавання тестів
   - `refactor:` - рефакторинг коду
   - `style:` - форматування коду

7. **Push** до вашого fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Створіть Pull Request**:
   - Опишіть зміни
   - Посилання на related issues
   - Скріншоти (для UI змін)

## Стиль коду

### Python (Backend)

- **PEP 8** style guide
- **Type hints** для всіх функцій
- **Docstrings** для класів та публічних методів
- **Async/await** для I/O операцій

Приклад:
```python
async def get_law(law_id: UUID) -> Optional[Law]:
    """Get law by ID.
    
    Args:
        law_id: UUID of the law
        
    Returns:
        Law object or None if not found
    """
    return await db.query(Law).filter(Law.id == law_id).first()
```

### TypeScript (Frontend)

- **Strict mode** enabled
- **No `any` types**
- **Functional components** для React
- **Props interfaces** для всіх компонентів

Приклад:
```typescript
interface ArticleViewProps {
  article: Article | null;
}

export default function ArticleView({ article }: ArticleViewProps) {
  // ...
}
```

### Commit Messages

Використовуйте [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

Приклади:
- `feat(api): add article search endpoint`
- `fix(parser): handle articles without titles`
- `docs(readme): update installation instructions`

## Тестування

### Backend Tests

```bash
cd backend

# Запустити всі тести
pytest

# З coverage
pytest --cov=app --cov-report=html

# Конкретний файл
pytest app/tests/test_api.py -v
```

### Мінімальний coverage

- **API endpoints:** 80%+
- **Services:** 70%+
- **Models:** 60%+

## Документація

При додаванні нової функції:

1. Оновіть `README.md` (якщо змінюється API)
2. Додайте docstrings до коду
3. Оновіть `DEPLOYMENT.md` (якщо змінюється deployment)
4. Додайте приклади використання

## Code Review Process

1. Maintainer перевірить ваш PR протягом 2-3 днів
2. Можуть бути запитані зміни
3. Після approval PR буде merged
4. Ваш внесок буде додано до CHANGELOG

## Питання?

- Створіть [Discussion](https://github.com/YOUR-USERNAME/law-analyse/discussions)
- Напишіть в Issues з тегом `question`

## Кодекс поведінки

- Будьте ввічливі та поважайте інших
- Конструктивна критика вітається
- Дискримінація не толерується

Дякуємо за ваш внесок! 🎉
