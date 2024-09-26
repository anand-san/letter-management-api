import sentry_sdk
from utils.get_env import get_env_var


def init_sentry():

    try:
        SENTRY_DSN = get_env_var("SENTRY_DSN")
        ENVIRONMENT = get_env_var("ENVIRONMENT")

        if (ENVIRONMENT == "production"):
            sentry_sdk.init(
                dsn=''.join(SENTRY_DSN),
                traces_sample_rate=1.0,
            )

    except Exception as e:
        print(f"Error initializing Sentry: {e}")
