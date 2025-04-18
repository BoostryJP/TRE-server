#!/bin/bash

# Copyright BOOSTRY Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

source ~/.bash_profile

cd /app/TRE-server

TEST_TARGET=${TEST_TARGET:-tests/}

sleep 10

# Test
uv run pytest -v --cov=. --junitxml=pytest.xml --cov-report=xml --cov-report=term-missing:skip-covered --cov-branch $TEST_TARGET

status_code=$?

# Move coverage files
mv coverage.xml cov/
mv pytest.xml cov/
mv .coverage cov/

if [ $status_code -ne 0 ]; then
  exit 1
fi
