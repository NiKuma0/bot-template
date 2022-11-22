import asyncio

from app.bot import init_bot


def main():
    try:
        asyncio.run(init_bot())
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
