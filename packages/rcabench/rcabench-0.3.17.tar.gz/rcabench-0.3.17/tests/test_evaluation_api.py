# Run this file:
# uv run pytest -s tests/test_dataset_api.py
from typing import List, Optional
from pprint import pprint
import pytest


@pytest.mark.parametrize(
    "execution_ids, algorithms, levels, metrics, rank",
    [(311, None, None, None, None)],
)
def test_execute(
    sdk,
    execution_ids: List[int],
    algorithms: Optional[List[str]],
    levels: Optional[List[str]],
    metrics: Optional[List[str]],
    rank: Optional[int],
):
    """测试算法评估"""
    file_path = sdk.evaluation.execute(execution_ids, algorithms, levels, metrics, rank)
    pprint(file_path)
