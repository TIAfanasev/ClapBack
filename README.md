# ClapBack

В директории `app` создать файл `.env` и заполнить его следующими данными:

```.env
DB_URL="psycopg2+asyncpg://<username>:<password>@db/clapdb"

SECRET_KEY=<your-secret-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

где:

- `<username>` - имя пользователя в СУБД (например, `postgres`),
- `<password>` - пароль для этого пользователя,
- `<your-secret-key>` - сгенерированный секретный ключ длиной в 20 символов (просто вбить в поисковик secret key generator).

Далее, в этой же директории выполнить команду:

```bash
docker-compose up --build
```
