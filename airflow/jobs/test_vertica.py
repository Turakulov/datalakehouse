import vertica_python

# Конфигурация подключения
conn_info = {
    "host": "host.docker.internal",  # Адрес сервера Vertica
    "port": 5433,  # Порт (по умолчанию 5433)
    "user": "newdbadmin",  # Имя пользователя
    "password": "vertica",  # Пароль
    "database": "VMart",  # Имя базы данных
    "autocommit": True,  # Автофиксирование изменений
}


# Устанавливаем соединение
try:
    connection = vertica_python.connect(**conn_info)
    cursor = connection.cursor()

    # Выполняем SQL-запрос
    cursor.execute("SELECT version();")

    # Получаем результат
    for row in cursor.fetchall():
        print("Vertica Version:", row[0])

except Exception as e:
    print("Ошибка при подключении к Vertica:", str(e))

finally:
    # Закрываем соединение
    if "connection" in locals():
        cursor.close()
        connection.close()
        print("Соединение закрыто.")
