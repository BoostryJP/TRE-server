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

import configparser
import os

SERVER_NAME = "TRE-server"

####################################################
# Basic settings
####################################################
# System timezone for REST API
TZ = os.environ.get("TZ") or "Asia/Tokyo"

# Environment-specific settings
APP_ENV = os.environ.get("APP_ENV") or "local"
INI_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), f"conf/{APP_ENV}.ini"
)
CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)

# Response validation mode
RESPONSE_VALIDATION_MODE = (
    True if os.environ.get("RESPONSE_VALIDATION_MODE") == "1" else False
)

####################################################
# Server settings
####################################################
# Logging
LOG_LEVEL = CONFIG["logging"]["level"]
ACCESS_LOGFILE = os.environ.get("ACCESS_LOGFILE") or "/dev/stdout"

####################################################
# Key settings
####################################################
# Master key
MASTER_KEY = (
    int(os.environ.get("MASTER_KEY"))
    if os.environ.get("MASTER_KEY")
    else 10789811928921474688961551662172418488946510310186884612397521295881445660903
)
