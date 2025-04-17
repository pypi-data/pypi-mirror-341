from typing import Any, Dict, List, Optional
from rcabench.logger import logger
from rcabench.rcabench import RCABenchSDK
import asyncio

BASE_URL = "http://127.0.0.1:8082"
sdk = RCABenchSDK(BASE_URL)


async def test_injection_and_building_dataset_batch(
    benchmark: str,
    interval: int,
    pre_duration: int,
    specs: List[Dict[str, Any]],
    num_consumers: int,
    max_items_per_consumer: int,
    per_consumer_timeout: float,
):
    assert num_consumers <= len(specs)
    sdk = RCABenchSDK(BASE_URL)

    resp = sdk.injection.submit(benchmark, interval, pre_duration, specs)
    logger.info(resp)

    traces = resp.traces

    task_ids = [trace.head_task_id for trace in traces]
    trace_ids = [trace.trace_id for trace in traces]
    queue = await sdk.task.get_stream_batch(task_ids, trace_ids, interval * 60)

    results = await run_consumers(
        queue,
        num_consumers,
        max_items_per_consumer,
        per_consumer_timeout,
    )

    await sdk.task.stream.cleanup()
    return results


async def run_consumers(
    queue: asyncio.Queue,
    num_consumers: int,
    max_items_per_consumer: int,
    per_consumer_timeout: Optional[float] = None,
):
    all_results = {}
    tasks = [
        asyncio.create_task(
            consumer_task(
                i, queue, max_items_per_consumer, per_consumer_timeout * (i + 1)
            )
        )
        for i in range(num_consumers)
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Consumer {i} failed: {str(result)}")
            all_results[f"Batch-{i}"] = None
        else:
            all_results[f"Batch-{i}"] = result

    return all_results


async def consumer_task(
    consumer_id: int,
    queue: asyncio.Queue,
    max_num: int,
    timeout: Optional[float] = None,
):
    try:
        results = await consumer(queue, max_num, timeout)
        logger.info(f"Consumer-{consumer_id} completed")
        return results
    except asyncio.TimeoutError:
        logger.error(f"Consumer-{consumer_id} timed out")
        raise
    except Exception as e:
        logger.error(f"Consumer-{consumer_id} error: {str(e)}")
        raise


async def consumer(queue: asyncio.Queue, max_num: int, timeout: Optional[float] = None):
    results = []
    count = 0
    while count < max_num:
        try:
            item = await asyncio.wait_for(queue.get(), timeout)
            results.append(item)
            count += 1
        except asyncio.TimeoutError:
            logger.warning("Timeout while waiting for queue item")
            raise

    return results


async def main(total_timeout: Optional[float] = None):
    payload = [
        "clickhouse",
        3,
        1,
        [
            {
                "children": {
                    "1": {
                        "children": {
                            "0": {"value": 1},
                            "1": {"value": 0},
                            "2": {"value": 42},
                        }
                    },
                },
                "value": 1,
            },
        ],
        1,
        1,
        3 * 60,
    ]

    results = {}
    try:
        results = await asyncio.wait_for(
            test_injection_and_building_dataset_batch(*payload), timeout=total_timeout
        )
        logger.info(f"Final results: {results}")
    except asyncio.TimeoutError:
        logger.error("Total time out")
    finally:
        logger.info(f"Final results: {results}")


if __name__ == "__main__":
    asyncio.run(main())
