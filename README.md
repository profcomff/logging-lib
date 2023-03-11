#  logging-lib
Библиотека для логирования сервисов Твой ФФ!

## Как подключить
1. В requirements.txt добавьте logging-profcomff
2. Скопируйте из /gunicorn_logging_examples обе конфигурации
3. Вставьте их в корень проекта
4. Добаввьте в Dockerfile ARG CONF_FILE
5. В Dockerfile добавьте GUNICORN_CMD_ARGS в качестве env переменной
6. Пропишите туда "--log-config  $CONF_FILE"
7. В Actions в запуск добавьте(прод) --build-args: docker build --build-arg CONF_FILE=logging_prod.conf
8. В Actions в запуск добавьте(тест) --build-args: docker build --build-arg CONF_FILE=logging_test.conf
