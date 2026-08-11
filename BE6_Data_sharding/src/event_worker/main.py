import asyncio
import logging

from event_worker.config import worker_settings
from event_worker.db import WorkerSessionLocal, worker_engine
from event_worker.generator import generate_product_update
from event_worker.producer import ProductEventProducer
from event_worker.repository import ProductReadRepository


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    ),
)

logger = logging.getLogger("event_worker")


async def run_worker() -> None:
    producer = ProductEventProducer()

    logger.info("RabbitMQ bilan ulanish boshlandi")
    await producer.connect()
    logger.info("RabbitMQ bilan ulanish o‘rnatildi")

    try:
        while True:
            try:
                with WorkerSessionLocal() as db:
                    product = ProductReadRepository(
                        db
                    ).get_random()

                    if product is None:
                        logger.warning(
                            "Bazadan mahsulot topilmadi"
                        )
                    else:
                        event = generate_product_update(
                            product
                        )

                        await producer.publish(event)

                        logger.info(
                            "Event yuborildi: "
                            "event_id=%s product_id=%s "
                            "price=%s available_stock=%s",
                            event.event_id,
                            event.product_id,
                            event.price,
                            event.available_stock,
                        )

            except asyncio.CancelledError:
                raise

            except Exception:
                logger.exception(
                    "Event yaratish yoki yuborishda xatolik"
                )

            await asyncio.sleep(
                worker_settings
                .event_generator_interval_seconds
            )

    finally:
        logger.info("Event worker to‘xtatilmoqda")
        await producer.close()
        worker_engine.dispose()


def main() -> None:
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        logger.info("Event worker foydalanuvchi tomonidan to‘xtatildi")


if __name__ == "__main__":
    main()
