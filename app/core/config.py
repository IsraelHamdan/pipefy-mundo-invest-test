from dotenv import load_dotenv

import os

load_dotenv()


class Settings:

    PIPEFY_PIPE_ID: int = int(
        os.getenv("PIPEFY_PIPE_ID", "0")
    )

    DB_URL: str = os.getenv(
        "DATABASE_URL",
        ""
    )


settings = Settings()