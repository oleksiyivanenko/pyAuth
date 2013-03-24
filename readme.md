# pyAuth

Простая GUI программка парольной авторизации.  
Все данные хранит в sqlite3. Для GUI инспользуется биндинг к Qt - PySide.

Запуск:

	python pyAuth.py

При первом старте автоматически создается база passApp.db и пользователь admin с пустым паролем.

Админимтратор может:

- Войти/выйти
- Поменять себе пароль
- Посмотреть список пользователей
- Добавить пользователя с пустым паролем
- Заблокировать пользователя
- Наложить ограничения на пароль пользователя(на сложность пароля)

Простой пользователь может:

- Войти/выйти
- Поменять себе пароль

Зависимости:

- sqlite3
- PySide