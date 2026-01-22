1-Загрузить файлы на компьютер
2-установить зависимости из файла requirements.txt
3-Создайте .env файл с настройками
    Пример:
    DATABASE_URL=postgresql://postgres:password@localhost:5432/advertisements
    SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
    ACCESS_TOKEN_EXPIRE_HOURS=48
    API_V1_PREFIX=
    PROJECT_NAME=Advertisement Service
    VERSION=1.0.0
    POSTGRES_DB=advertisements
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password
4-Запустите БД (или используйте свою PostgreSQL)
3-Запустить файл run.py
4-Дождаться заверешения работы файла
5-Открыть браузер, перейти по адресу http://localhost:8000/docs
6-Проверить работоспособность
    Для тестирования используйте:
   - Создание пользователя: POST /user
   - Авторизация: POST /login
   - Тестовые пользователи (пароль: password123):
     admin / admin
     user1 / user1
     user2 / user2
7-при необходимости можно развернуть Докер