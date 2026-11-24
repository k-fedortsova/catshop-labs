import sys
from pathlib import Path
import pytest

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_DIR))

import os
os.environ.pop("DATABASE_URL", None)

import app as shop_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create a test client with an isolated counter file."""
    counter_file = tmp_path / "visits.txt"

    monkeypatch.setattr(shop_app, "COUNTER_FILE", counter_file)

    with shop_app.app.test_client() as test_client:
        yield test_client