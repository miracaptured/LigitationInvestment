# Судебная инвестиция
Код к курсовому проекту 2023.

Сервис «Судебная инвестиция» предназначен в первую очередь для расширения возможностей компании ООО «СУДИНВЕСТ.РУ». Внедрение разработки должно ускорить процесс перехода от судебного инвестиционного фонда (страница фонда с лид-формой, обработка информации локально) к специализированной площадке для инвестиций на основе механик краудфандинговых платформ (веб-сервис, автоматизация процесса подачи заявок). Система будет использоваться для работы с делами (добавление, просмотр, отслеживание статуса) авторизованных пользователей. 

## Описание и ссылочки
- штука

## Как запустить?
Необходимо иметь docker с docker-compose.
Предварительная настройка:
1. перейти в папку с проектом
2. создать файл .env со следующим наполнением:
```
  DBNAME=*название базы*
  DBPASSWORD=*пароль для подключения к БД*
  DBUSER=*имя пользователя для подключения к БД*
  PORT=*порт для размещения базы*
  HOST=*имя хоста базы*
  SSL_KEY=*ключ для аутентификации*
```
3. как сгенерировать ключ? Открыть терминал и выполнить команду: ```openssl rand -hex 32```

Процесс запуска:
1. открыть терминал;
2. перейти в папку с проектом;
3. выполнить команду: ```docker-compose up```
4. после этого можно в браузере открыть страницу ```localhost:4200``` и протестировать сервис.

Тестовые аккаунты для проверки (пароль везде 123):
- фигуранты: figurant*@email.com, вместо звездочки цифры от 1 до 6
- инвесторы: investor*@email.com, вместо звездочки цифры от 1 до 2
- или можно зарегистрироваться самостоятельно

