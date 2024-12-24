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
class TestGetTimeKey:
    api_url = "/key/time_key/{timestamp}"

    async def test_normal_1(self, client):
        key_time = int((datetime(2024, 1, 1, tzinfo=UTC).timestamp()))

        resp = client.get(self.api_url.format(timestamp=key_time))

        assert resp.status_code == 200
        assert resp.json() == {
            "q": [
                [
                    "1101798974526282471986224887686905968285497234745651116444903295936345549744574721859877651642500185355883597476090",
                    "3168356523279500265240544093584847833617843690357098076890922492978156466314860970122215302525629642473692715407509",
                ],
                [
                    "829108022039633017482471871806720108542704191761928320073257872114547914939005944178364647740348226860497843847077",
                    "3643708063449983355295092050677025810190592163522588265116541298665163669297725356872330227307362499431389980677531",
                ],
                [
                    "2275676799157674963541212316722260745913582057575238745960189132415184285104672180644581802748948287510637887447936",
                    "3804741950753690840394268440461483661728970256404173656533961438049684079346739178783107704126226783539055946770142",
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
