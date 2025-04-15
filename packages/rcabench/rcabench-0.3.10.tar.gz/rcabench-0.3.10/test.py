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
    queue = await sdk.task.get_stream_batch(task_ids, trace_ids)

    try:
        results = await run_consumers(
            queue,
            num_consumers,
            max_items_per_consumer,
            per_consumer_timeout,
            per_consumer_timeout * (num_consumers + 1),
        )
        logger.info(f"Final results: {results}")
        return results
    finally:
        await sdk.task.stream.cleanup()


async def run_consumers(
    queue: asyncio.Queue,
    num_consumers: int,
    max_items_per_consumer: int,
    per_consumer_timeout: Optional[float] = None,
    total_timeout: Optional[float] = None,
):
    all_results = {}

    start_time = asyncio.get_event_loop().time()
    for i in range(num_consumers):
        if total_timeout:
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed >= total_timeout:
                logger.warning(
                    f"Total execution time exceeded {total_timeout} seconds, stopping subsequent tasks"
                )
                break

            # Calculate remaining timeout for current task
            remaining = total_timeout - elapsed
            current_timeout = min(per_consumer_timeout, remaining)
        else:
            current_timeout = per_consumer_timeout

        logger.info(f"Starting consumer {i}, timeout: {current_timeout} seconds")

        try:
            results = await consumer(queue, max_items_per_consumer, current_timeout)
            all_results[f"Batch-{i}"] = results
            logger.info(f"Consumer-{i} completed")
        except asyncio.TimeoutError:
            logger.error(f"Consumer-{i} execution timeout")
        except Exception as e:
            logger.error(f"Consumer-{i} execution error: {e}")

    return all_results


async def consumer(queue: asyncio.Queue, max_num: int, timeout: Optional[float] = None):
    results = []
    count = 0
    while count < max_num:
        got_item = False
        try:
            item = await asyncio.wait_for(queue.get(), timeout)
            got_item = True

            results.append(item)

            count += 1
        finally:
            if got_item:
                queue.task_done()

    return results


async def main():
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

    return await test_injection_and_building_dataset_batch(*payload)


if __name__ == "__main__":
    asyncio.run(main())
