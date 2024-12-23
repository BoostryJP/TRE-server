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

from fastapi import status


class AppError(Exception):
    status_code: int
    code: int | None = None
    code_list: list[int] | None = None


################################################
# 400_BAD_REQUEST
################################################
class BadRequestError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidParameterError(BadRequestError):
    code = 1


class Integer64bitLimitExceededError(BadRequestError):
    code = 2


################################################
# 401_UNAUTHORIZED
################################################
class AuthorizationError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = 1


################################################
# 503_SERVICE_UNAVAILABLE
################################################
class ServiceUnavailableError(AppError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = 1
