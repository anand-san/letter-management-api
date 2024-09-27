import sentry_sdk
from fastapi import HTTPException

from src.utils.get_env import get_env_var
from src.api.resolvers import RagException


def init_sentry():
    try:
        SENTRY_DSN = get_env_var("SENTRY_DSN")
        ENVIRONMENT = get_env_var("ENVIRONMENT")

        if (ENVIRONMENT != "local"):
            sentry_sdk.init(
                dsn=''.join(SENTRY_DSN),
                traces_sample_rate=1.0,
                before_send=before_send,
                debug=False,
                environment=ENVIRONMENT,
            )

            sentry_sdk.set_level("error")

    except Exception as e:
        print(f"Error initializing Sentry: {e}")


def before_send(event, hint):
    if should_send_event(event, hint):
        return event
    return None


def should_send_event(event, hint):
    exception = hint.get('exc_info')
    if exception:
        exc_type, exc_value, tb = exception
        # Always Catch RagException
        if isinstance(exc_value, RagException):
            return True

        # Ignored Exceptions
        if isinstance(exc_value, ValueError) or isinstance(exc_value, HTTPException):
            return False

    return True
