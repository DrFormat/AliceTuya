# Алиса+Tuya

## Config

#### [Tuya IOT](http://iot.tuya.com/)
    ACCESS_ID = access_id
    ACCESS_SECRET = access_secret
    USERNAME = linked username
    PASSWORD = linked password
    ENDPOINT_URL=openapi.tuyaeu.com
    MQ_ENDPOINT=wss://mqe.tuyaeu.com:8285/

#### [Yandex Алиса](https://yandex.ru/dev/dialogs/smart-home/doc/reference-alerts/post-skill_id-callback-state.html)

    SKILL_ID =
    SKILL_TOKEN =

## Alembic
### Generate
`alembic revision --autogenerate`
### Migrate
`alembic upgrade head`

## [Nginx](https://hub.docker.com/r/jwilder/nginx-proxy "hub.docker.com")