# Copyright 2024 Moth Quantum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==========================================================================

"""
========
Overview
========

This subpackage contains the utility modules that support the core operations of schemes.
The contents of the following modules are directly accessible from the subpackage `quantumaudio.utils`.

- **circuit**: Helper functions for quantum audio circuit preparations with `Qiskit`.
- **convert**: Data pre-processing functions required for encoding values into the quantum circuit.
- **data**: Data preparation and calculation functions.
- **execute**: Helper Functions for executing circuits. Uses `AerSimulator` as Default backend.
- **preview**: Functions to draw and print information of a circuit.
- **results**: Common helper functions for obtaining circuit results.
"""

from .circuit import *
from .convert import *
from .data import *
from .execute import *
from .results import *
from .preview import *
