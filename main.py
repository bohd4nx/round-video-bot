import asyncio
import logging

from bot.app import run

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception:
        logging.getLogger(__name__).exception("Bot crashed")
