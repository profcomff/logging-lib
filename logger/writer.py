from typing import Any


def create_log_config(project_name: str, *, log_level: str) -> dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": "logging.logger.formatter.JSONLogFormatter",
            },
        },
        "handlers": {
            "json": {
                "formatter": "json",
                "class": "asynclog.AsyncLogDispatcher",
                "func": "logging.logger.writer.write_log",
            },
        },
        "loggers": {
            project_name: {
                "handlers": ["json"],
                "level": log_level.upper(),
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["json"],
                "level": log_level.upper(),
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["json"],
                "level": log_level.upper(),
                "propagate": False,
            },
        },
    }


def write_log(message):
    print(message)
