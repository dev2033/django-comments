<h1>Comments_project</h1>

<p>Как запустить проект:</p>

- Удаляем папку venv;
- Создаем новое виртуальное окружение;
- Устанавливаем зависимости:
    
    `pip install -r requrements.txt`
- Ставим миграции:

    `python manage.py makemigrations`
    
    `python manage.py migrate`
- Запускаем сервер: 

    `python manage.py runserver`    
-Переходим на страницу **post-comments/** :

    **``http://127.0.0.1:8000/post-comments/``**