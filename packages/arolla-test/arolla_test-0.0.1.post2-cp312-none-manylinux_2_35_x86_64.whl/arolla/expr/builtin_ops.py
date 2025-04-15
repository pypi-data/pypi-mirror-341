# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Initializes builtin operators."""


def get_namespaces():
  return [
      # go/keep-sorted start
      'annotation',
      'array',
      'bitwise',
      'bool',
      'core',
      'derived_qtype',
      'dict',
      'edge',
      'experimental',
      'math',
      'math.trig',
      'namedtuple',
      'py',
      'qtype',
      'random',
      'seq',
      'strings',
      # go/keep-sorted end
  ]
