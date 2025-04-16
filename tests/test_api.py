# tests/test_api.py

import pytest
from httpx import AsyncClient
from backend.main import app  # Make sure this points to your FastAPI instance

@pytest.mark.asyncio
async def test_list_functions():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/functions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
