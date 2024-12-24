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

from datetime import UTC, datetime, timedelta

import pytest


@pytest.mark.asyncio
class TestGetPublicKey:
    api_url = "/key/time_key/{timestamp}"

    async def test_normal_1(self, client):
        key_time = int((datetime(2024, 1, 1).timestamp()))

        resp = client.get(self.api_url.format(timestamp=key_time))

        assert resp.status_code == 200
        assert resp.json() == {
            "q": [
                [
                    "2090889728011502656130730369179742288672236911116815902059395526378986859893825316956918545310693199813992699404766",
                    "540571566244664933393475393042139469607238224813796968468360485869774214401086727811682018858900997192958389446567",
                ],
                [
                    "2192023608798789472939614911254989854697433196377744152187787942968790382247214384591631184619192624058086801538521",
                    "1211740427996443494093908200325245382421422212433765469093707814061131790268298377977369767392040709304474702728762",
                ],
                [
                    "1200657101930443771107822154582816146255129246568182047310305319386060381276641124461876479804785463330555322953775",
                    "854004588131360785443399911945887146415898652111039370706929507613104930482011409843965216475150342152804273895550",
                ],
            ]
        }

    # RequestValidationError
    async def test_error_1(self, client):
        resp = client.get(self.api_url.format(timestamp="invalid_timestamp"))

        assert resp.status_code == 422
        assert resp.json() == {
            "meta": {"code": 1, "title": "RequestValidationError"},
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "timestamp"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "invalid_timestamp",
                }
            ],
        }

    # InvalidParameterError
    # - The release time has not been reached yet.
    async def test_error_2(self, client):
        key_time = int(((datetime.now(UTC) + timedelta(minutes=1)).timestamp()))

        resp = client.get(self.api_url.format(timestamp=key_time))

        assert resp.status_code == 400
        assert resp.json() == {
            "meta": {"code": 1, "title": "InvalidParameterError"},
            "detail": "The release time has not been reached yet.",
        }
