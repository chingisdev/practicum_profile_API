"""Настройки логгера для uvicorn."""
from pathlib import Path

base_dir: Path = Path(__file__).resolve().parent.parent.parent.parent
access_log_file_path = base_dir / 'logs' / 'access.log'
error_log_file_path = base_dir / 'logs' / 'errors.log'

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = [
    'console',
]

# из теории практикума

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT,
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'error_file': {
            'formatter': 'default',
            'class': 'logging.FileHandler',
            'filename': error_log_file_path,
        },
        'access_file': {
            'formatter': 'default',
            'class': 'logging.FileHandler',
            'filename': access_log_file_path,
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'DEBUG',
        },
        'uvicorn.error': {
            'handlers': ['error_file', 'default'],
            'level': 'INFO',
        },
        'uvicorn.access': {
            'handlers': ['access_file', 'access'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
