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

import commandant as _commandant
import plano as _plano
import sys as _sys

_description = "Ghost!"

_epilog = """
example usage:
  $ ghost clone someproject

Ghost looks for its configuration at $HOME/.config/ghost/config.py.
"""

class GhostCommand(_commandant.Command):
    def __init__(self, home_dir):
        super(GhostCommand, self).__init__(home_dir, "ghost")

        self.description = _description
        self.epilog = _epilog

        config = self.load_config()
        user = config.get("user")

        self.add_argument("--user", metavar="USER", default=user,
                          help="GitHub user name (default {})".format(user))

        subparsers = self.add_subparsers()

        parser_clone = subparsers.add_parser("clone")
        parser_clone.add_argument("repo_name", metavar="REPO-NAME",
                                  help="The repository name")
        parser_clone.set_defaults(func=self.clone_command)

        parser_init = subparsers.add_parser("init")
        parser_init.add_argument("repo_dir", metavar="REPO-DIR",
                                 help="The repository directory")
        parser_init.set_defaults(func=self.init_command)

        parser_status = subparsers.add_parser("status")
        parser_status.add_argument("repo_dir", nargs="+", metavar="REPO-DIR",
                                   help="A repository directory")
        parser_status.set_defaults(func=self.status_command)

    def init(self):
        super(GhostCommand, self).init()

        if self.args.user is None:
            _plano.exit("No user name")

        if "func" not in self.args:
            _plano.exit("Missing subcommand")

    def run(self):
        self.args.func()

    def clone_command(self):
        _plano.set_message_threshold("warn")

        if _plano.exists(self.args.repo_name):
            exit("Path already exists")

        _plano.call("git clone git@github.com:{}/{}.git", self.args.user, self.args.repo_name)

    def init_command(self):
        _plano.set_message_threshold("warn")

        if _plano.exists(_plano.join(self.args.repo_dir, ".git")):
            self.fail("The directory is already initialized")

        repo_name = _plano.file_name(self.args.repo_dir)

        with _plano.working_dir(self.args.repo_dir):
            _plano.call("git init")
            _plano.call("git add .")
            _plano.call("git commit -m \"Initial commit\"")
            _plano.call("git remote add origin git@github.com:{}/{}.git", self.args.user, repo_name)

            print("Make sure this repo exists on GitHub and then push:")
            print("git push -u origin/{}".format(repo_name))

    def status_command(self):
        _plano.set_message_threshold("warn")

        for repo_dir in self.args.repo_dir:
            if not _plano.exists(_plano.join(repo_dir, ".git")):
                continue

            _sys.stdout.write("## {:<40} ".format(repo_dir))

            with _plano.working_dir(repo_dir):
                output = _plano.call_for_output("git status -sb")

            _sys.stdout.write(output.decode("utf-8"))
            _sys.stdout.flush()
