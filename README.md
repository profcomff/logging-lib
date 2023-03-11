#  logging-lib
Библиотека для логирования сервисов Твой ФФ!

## Как подключить
1. В requirements.txt добавьте logging-profcomff
2. Скопируйте из /gunicorn_logging_examples обе конфигурации
3. Вставьте их в корень проекта
4. Добаввьте в Dockerfile ARG conf_file
4. В Dockerfile добавьте GUNICORN_CMD_ARGS в качестве env переменной
5. Пропишите туда "--log-config $conf_file"
6. В Actions в запуск добавьте(прод) --build-args: docker build --build-arg conf_file=logging_prod.conf
7. В Actions в запуск добавьте(тест) --build-args: docker build --build-arg conf_file=logging_test.conf
