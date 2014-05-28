# Copyright 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
gcd error classes
"""

class Fail(Exception):
    """
    Assertion failure. Something went very wrong.
    """
    pass

class InvalidCondition(Exception):
    """
    Invalid Condition: some mismatch of parameters or specifications gave
    us a condition we can't interpret
    """
    pass

class NoAuthKeys(Exception):
    """
    Invalid Condition: some mismatch of parameters or specifications gave
    us a condition we can't interpret
    """
    pass
