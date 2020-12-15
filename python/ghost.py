#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import runpy as _runpy

from plano import *

def load_config():
    config_file = _os.path.join(get_home_dir(), ".config", "ghost", "config.py")
    config = dict()

    if exists(config_file):
        entries = _runpy.run_path(config_file, config)
        config.update(entries)

    return config

config = load_config()

@command
def clone(repo, output_dir=None):
    check_program("git")

    user = config["user"]
    command = ["git", "clone", f"git@github.com:{user}/{repo}.git"]

    if output_dir is not None:
        command.append(output_dir)

    run(command)
