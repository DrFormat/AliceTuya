# Алиса+Tuya

Интеграция устройств Tuya с Алисой

Навык [Smart Life](https://dialogs.yandex.ru/store/skills/8b143108-smart-life)
поддерживает только устройства
>Осветительные приборы Powered By Tuya  
>Розетка Powered By Tuya

Данная реализация имеет поддержку реле и контакртных сенсоров  
А так же уведомление Алисы о событиях  

Написано на 
> FastAPI  
> tuya-iot-py-sdk  
> aiosqlite + sqlalchemy

Так же включает простую реализацию OAuth2 (необходим для работы навыка)
 

Для запуска необходимо  
Tuya IOT https://www.home-assistant.io/integrations/tuya/  
Yandex Алиса https://yandex.ru/dev/dialogs/smart-home/doc/  

При необходимости Nginx https://hub.docker.com/r/jwilder/nginx-proxy

## Config

#### [Tuya IOT](https://www.home-assistant.io/integrations/tuya/  )
    ACCESS_ID = access_id
    ACCESS_SECRET = access_secret
    USERNAME = linked username
    PASSWORD = linked password
    ENDPOINT_URL=openapi.tuyaeu.com
    MQ_ENDPOINT=wss://mqe.tuyaeu.com:8285/

#### [Yandex Алиса](https://yandex.ru/dev/dialogs/smart-home/doc/)

    SKILL_ID =
    SKILL_TOKEN =

## Alembic
### Generate
`alembic revision --autogenerate`
### Migrate
`alembic upgrade head`

## [Nginx](https://hub.docker.com/r/jwilder/nginx-proxy "hub.docker.com")

[Для связи](mailto:formacevt@bk.ru)