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


@pytest.mark.asyncio
class TestGetPublicKey:
    api_url = "/key/public_key"

    async def test_normal_1(self, client):
        resp = client.get(self.api_url)

        assert resp.status_code == 200
        assert resp.json() == {
            "p": [
                "2914531705650652319358640088552519387536747023535073939204517923508042515930849106617082205318500856219255907557559",
                "3873347379530622534418133828971788254348152099338757624804067384414595956184006563536355109484617090434664752062793",
                "2008202023908700881367320793004029009610761805536488785208045086923720446169338314547174315296345430152667577665095",
            ]
        }
