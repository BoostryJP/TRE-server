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

from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Path
from py_ecc.bls.ciphersuites import G2Basic
from py_ecc.bls.hash_to_curve import hash_to_G2
from py_ecc.fields import optimized_bls12_381_FQ, optimized_bls12_381_FQ2
from py_ecc.optimized_bls12_381 import G1
from py_ecc.optimized_bls12_381.optimized_curve import multiply

from app.exceptions import InvalidParameterError
from app.model.schema import GetPublicKeyResponse, GetTimeKeyResponse
from app.utils.docs_utils import get_routers_responses
from app.utils.fastapi_utils import json_response
from config import MASTER_KEY

router = APIRouter(prefix="/key", tags=["key"])


# GET: /key/public_key
@router.get(
    "/public_key", operation_id="GetPublicKey", response_model=GetPublicKeyResponse
)
async def get_public_key():
    """Get public key"""

    p_x: tuple[
        optimized_bls12_381_FQ, optimized_bls12_381_FQ, optimized_bls12_381_FQ
    ] = multiply(G1, MASTER_KEY)

    return json_response(
        {
            "p": [
                str(p_x[0]),
                str(p_x[1]),
                str(p_x[2]),
            ]
        }
    )


# GET: /key/time_key/{timestamp}
@router.get(
    "/time_key/{timestamp}",
    operation_id="GetTimeKey",
    response_model=GetTimeKeyResponse,
    responses=get_routers_responses(InvalidParameterError),
)
async def get_time_key(
    timestamp: Annotated[int, Path(description="Unix timestamp")],
):
    """Get time key"""

    if datetime.now(UTC).timestamp() < timestamp:
        print(datetime.now(UTC).timestamp())
        raise InvalidParameterError("The release time has not been reached yet.")

    q_x: tuple[
        optimized_bls12_381_FQ2, optimized_bls12_381_FQ2, optimized_bls12_381_FQ2
    ] = multiply(
        hash_to_G2(str(timestamp).encode(), G2Basic.DST, G2Basic.xmd_hash_function),
        MASTER_KEY,
    )
    return json_response(
        {
            "q": [
                [str(q_x[0].coeffs[0]), str(q_x[0].coeffs[1])],
                [str(q_x[1].coeffs[0]), str(q_x[1].coeffs[1])],
                [str(q_x[2].coeffs[0]), str(q_x[2].coeffs[1])],
            ]
        }
    )
