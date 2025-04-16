import asyncio
import logging
from signal_generator import run_signal_loop

logging.basicConfig(level=logging.WARNING)

if __name__ == "__main__":
    try:
        asyncio.run(run_signal_loop())
    except Exception as e:
        logging.error(f"HATA: {e}")
