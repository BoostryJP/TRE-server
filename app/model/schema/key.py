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

from pydantic import BaseModel, Field, RootModel


############################
# RESPONSE
############################
class GetPublicKeyResponse(BaseModel):
    """Public key schema (RESPONSE)"""

    p: list[str] = Field(description="Public key", min_length=3, max_length=3)


class TimeKeyFQ2Item(RootModel):
    root: list[str] = Field(min_length=2, max_length=2)


class GetTimeKeyResponse(BaseModel):
    """Time key schema (RESPONSE)"""

    q: list[TimeKeyFQ2Item] = Field(description="Time key", min_length=3, max_length=3)
