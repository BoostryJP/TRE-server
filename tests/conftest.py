"""
Copyright BOOSTRY Co., Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncClient:
    async_client = AsyncClient(app=app, base_url="http://localhost")
    async with async_client as s:
        yield s


@pytest.fixture(scope="session")
def client() -> TestClient:
    client = TestClient(app)
    return client
