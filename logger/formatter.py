import datetime
import json
import logging
import traceback


class JSONLogFormatter(logging.Formatter):
    """
    Кастомизированный класс-форматер для логов в формате json
    """

    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        """
        Преобразование объект журнала в json

        :param record: объект журнала
        :return: строка журнала в JSON формате
        """
        log_object: dict = self._format_log_object(record)
        return json.dumps(
            log_object,
            ensure_ascii=False,
            skipkeys=True,
            default=lambda o: f"<{type(o)=} not serializable>",
        )

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict:
        """
        Перевод записи объекта журнала
        в json формат с необходимым перечнем полей

        :param record: объект журнала
        :return: Словарь с объектами журнала
        """
        now = (
            datetime.datetime.fromtimestamp(record.created)
            .astimezone()
            .replace(microsecond=0)
            .isoformat()
        )
        message = record.getMessage()
        duration_ms = record.duration if hasattr(record, "duration") else record.msecs
        # Инициализация тела журнала
        json_log_fields = dict()
        json_log_fields["thread"] = record.process
        json_log_fields["timestamp"] = now
        json_log_fields["level"] = record.levelno
        json_log_fields["level_name"] = record.levelname
        json_log_fields["message"] = message
        json_log_fields["source"] = record.name
        json_log_fields["duration_ms"] = duration_ms
        json_log_fields["func"] = record.funcName
        json_log_fields["file"] = record.filename
        empty_record = logging.LogRecord(
            str(), int(), str(), int(), object(), exc_info=None, args=(object,)
        )
        keys = set(dir(record)) - set(dir(empty_record))
        json_log_fields.update({key: getattr(record, key) for key in keys})

        if hasattr(record, "props"):
            json_log_fields.props = record.props

        if record.exc_info:
            json_log_fields["exceptions"] = traceback.format_exception(*record.exc_info)
        elif record.exc_text:
            json_log_fields["exceptions"] = record.exc_text

        if hasattr(record, "request_json_fields"):
            json_log_fields.update(record.request_json_fields)

        return json_log_fields
