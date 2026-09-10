"""Structured logging, with a run ID threaded through every log line
via structlog's contextvars binding. Notice what's logged at each
step: order_id, always. customer_email, never - that's PII, and
nothing here needs it to diagnose a delivery failure.
"""

import uuid
from typing import TypedDict

import structlog

from notifier.email_service import send_confirmation_email

logger = structlog.get_logger()


class Order(TypedDict):
    order_id: str
    customer_email: str
    total: float


def process_orders(orders: list[Order]) -> None:
    run_id = str(uuid.uuid4())
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(run_id=run_id)

    logger.info("batch_started", order_count=len(orders))

    for order in orders:
        order_id = order["order_id"]
        logger.info("email_send_started", order_id=order_id)
        try:
            send_confirmation_email(order_id, order["customer_email"], order["total"])
            logger.info("email_send_succeeded", order_id=order_id)
        except Exception as e:
            logger.error("email_send_failed", order_id=order_id, error=str(e))

    logger.info("batch_finished")
