"""
Transaction Stream Endpoints
cf. https://developer.oanda.com/rest-live-v20/transaction-ep/
"""

import asyncio
import json
import logging
from collections.abc import AsyncGenerator
from typing import Optional

import aiohttp
from strats.exchange import StreamClient

from strats_oanda.config import get_config
from strats_oanda.model.transaction import (
    Transaction,
    parse_limit_order_transaction,
    parse_order_cancel_transaction,
    parse_order_fill_transaction,
)

logger = logging.getLogger(__name__)


class TransactionClient(StreamClient):
    def __init__(self):
        self.config = get_config()

    async def stream(self) -> AsyncGenerator[Transaction]:
        try:
            logger.info("TransactionClient start")

            url = f"{self.config.account_streaming_url}/transactions/stream"
            headers = {
                "Authorization": f"Bearer {self.config.token}",
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status != 200:
                        raise RuntimeError(f"Failed to connect: status={resp.status}")

                    async for line_bytes in resp.content:
                        line = line_bytes.decode("utf-8").strip()

                        if not line or "HEARTBEAT" in line:
                            continue

                        try:
                            data = json.loads(line)
                            tx_type = data.get("type")

                            tx: Optional[Transaction] = None
                            if tx_type == "LIMIT_ORDER":
                                tx = parse_limit_order_transaction(data)
                            elif tx_type == "ORDER_CANCEL":
                                tx = parse_order_cancel_transaction(data)
                            elif tx_type == "ORDER_FILL":
                                tx = parse_order_fill_transaction(data)
                            elif tx_type == "HEARTBEAT":
                                continue
                            else:
                                logger.warn(f"unknown transaction arrived. {data}")
                                continue

                            if tx is not None:
                                yield tx
                        except Exception as e:
                            logger.error(f"failed to parse message. {e}, {line=}")
                            continue

        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.error(f"Unhandled exception in TransactionClient: {e}")
        finally:
            logger.info("TransactionClient stopped")
