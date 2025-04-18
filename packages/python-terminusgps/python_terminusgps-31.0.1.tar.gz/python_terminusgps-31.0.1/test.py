import asyncio

from terminusgps.twilio.caller import TwilioCaller


async def main() -> None:
    with TwilioCaller() as caller:
        task = caller.create_notification(
            to_number="+17133049421", message="Hello from Terminus GPS!", method="sms"
        )
        await task


if __name__ == "__main__":
    asyncio.run(main())
