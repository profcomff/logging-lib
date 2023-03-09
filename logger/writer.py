from typing import Any


def create_log_config(*, log_level: str) -> dict[str, Any]:
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
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout'
            },
        },
        "loggers": {
            "": {
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


