# MCP Agent

## О проекте

MCP Agent — это проект с открытым исходным кодом, направленный на разработку интеллектуального агента на основе фреймворка LangChain. Агент предназначен для автоматизации задач, взаимодействия с Google Calendar, Google Sheets, Google Gmail, а также для ответов на вопросы при использовании внутренней базы знаний.

### Основные функции:
- Взаимодействие с MCP серверами для работы с сервисами Google
- Ответы на вопросы пользователя

### Требования
- Python 3.12
- Docker

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/Aeksar/mcp_agent.git
   ```

3. Добавьте в корневую директорию файл .env на подобии .env.example.

4. Добавьте в корневую директорию файл redis.env и задайте в нем REDIS_PASSWORD.

5. Создайте в Google Cloud авторизованного клиента и скачайте его зависимости.

   1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/welcome).
   2. Создайте новый проект или выберите существующий.
   3. Включите API Google Calendar и Google Sheets API.
   4. Создайте учётные данные OAuth 2.0.
   5. Загрузите учётные данные и сохраните их как credentials.json в папке каждого сервера.

6. Добавьте в директорию calendar и sheet серверов файл credentials.json с зависимостями.

7. Создайте пароль приложения почты в [Google Account](https://myaccount.google.com/apppasswords)

8. Добавьте его в credentials.json для почты вместе с именем почтового ящика

7. Запустите Docker Compose:
   ```
   docker compose up --build
   ```
