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

import logging
import sys
import urllib
from datetime import UTC, datetime

from fastapi import Request, Response

from config import ACCESS_LOGFILE, APP_ENV, LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL)
LOG = logging.getLogger("tre_server")
LOG.propagate = False
ACCESS_LOG = logging.getLogger("tre_server_access")
ACCESS_LOG.propagate = False

INFO_FORMAT = "[%(asctime)s] {}[%(process)d] [%(levelname)s] %(message)s"
DEBUG_FORMAT = "[%(asctime)s] {}[%(process)d] [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S %z"

MESSAGE_FORMAT = '"%s %s HTTP/%s" %d (%.6fsec)'
ACCESS_FORMAT = "[%s] %s"

if APP_ENV == "live":
    # App Log
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(INFO_FORMAT.format("[APP-LOG] "), TIMESTAMP_FORMAT)
    stream_handler.setFormatter(formatter)
    LOG.addHandler(stream_handler)

    # Access Log
    stream_handler_access = logging.StreamHandler(open(ACCESS_LOGFILE, "a"))
    formatter_access = logging.Formatter(
        INFO_FORMAT.format("[ACCESS-LOG] "), TIMESTAMP_FORMAT
    )
    stream_handler_access.setFormatter(formatter_access)
    ACCESS_LOG.addHandler(stream_handler_access)

if APP_ENV == "dev" or APP_ENV == "local":
    # App Log
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(DEBUG_FORMAT.format("[APP-LOG] "), TIMESTAMP_FORMAT)
    stream_handler.setFormatter(formatter)
    LOG.addHandler(stream_handler)

    # Access Log
    stream_handler_access = logging.StreamHandler(open(ACCESS_LOGFILE, "a"))
    formatter_access = logging.Formatter(
        INFO_FORMAT.format("[ACCESS-LOG] "), TIMESTAMP_FORMAT
    )
    stream_handler_access.setFormatter(formatter_access)
    ACCESS_LOG.addHandler(stream_handler_access)


def get_logger():
    return LOG


def output_access_log(req: Request, res: Response, request_start_time: datetime):
    url = __get_url(req)
    if url != "/":
        method = req.scope.get("method", "")
        http_version = req.scope.get("http_version", "")
        status_code = res.status_code
        response_time = (
            datetime.now(UTC).replace(tzinfo=None) - request_start_time
        ).total_seconds()
        access_msg = MESSAGE_FORMAT % (
            method,
            url,
            http_version,
            status_code,
            response_time,
        )

        msg = __format_log(req, access_msg)
        ACCESS_LOG.info(msg)


def __format_log(req: Request, msg: str):
    if req.client is None:
        _host = ""
    else:
        _host = req.client.host
    return ACCESS_FORMAT % (_host, msg)


def __get_url(req: Request):
    scope = req.scope
    url = urllib.parse.quote(scope.get("root_path", "") + scope.get("path", ""))
    if scope.get("query_string", None):
        url = "{}?{}".format(url, scope["query_string"].decode("ascii"))
    return url
