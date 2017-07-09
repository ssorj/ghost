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

import argparse as _argparse

class Command(object):
    def __init__(self, name, home_dir):
        self.name = name
        self.home_dir = home_dir

        self._parser = _argparse.ArgumentParser()
        self._parser.formatter_class = _argparse.RawDescriptionHelpFormatter

        self._args = None

        self.add_argument("--init-only", action="store_true",
                          help="Initialize then exit")

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    @property
    def parser(self):
        return self._parser

    @property
    def args(self):
        return self._args

    @property
    def description(self):
        return self.parser.description

    @description.setter
    def description(self, text):
        text = text.strip()
        self.parser.description = text

    @property
    def epilog(self):
        return self.parser.epilog

    @epilog.setter
    def epilog(self, text):
        text = text.strip()
        self.parser.epilog = text

    def init(self):
        assert self._args is None

        self._args = self.parser.parse_args()

        self.init_only = self.args.init_only

    def run(self):
        raise NotImplementedError()

    def main(self):
        try:
            self.init()

            assert self._args is not None

            if self.init_only:
                return

            self.run()
        except KeyboardInterrupt:
            pass
