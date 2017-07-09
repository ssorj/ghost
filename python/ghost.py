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

import commandante as _commandante
import plano as _plano
import runpy as _runpy

_user_dir = _plano.home_dir()
_default_config_file = _plano.join(_user_dir, ".config", "ghost", "config.py")
_description = "Ghost!"

_epilog = """
example usage:
  $ ghost clone someproject

Ghost looks for its configuration at $HOME/.config/ghost/config.py.
"""

class GhostCommand(_commandante.Command):
    def __init__(self, home_dir):
        super(GhostCommand, self).__init__("ghost", home_dir)

        self.description = _description
        self.epilog = _epilog

        # XXX default=config.get("user"),
        self.add_argument("--user", metavar="USER", default=None,
                          help="GitHub user name")

        subparsers = self.parser.add_subparsers()

        parser_clone = subparsers.add_parser("clone")
        parser_clone.add_argument("repo", metavar="REPO",
                                  help="The repository name")
        parser_clone.set_defaults(func=self.clone_command)

        parser_init = subparsers.add_parser("init")
        parser_init.add_argument("repo", metavar="REPO",
                                 help="The repository name")
        parser_init.set_defaults(func=self.init_command)

        parser_status = subparsers.add_parser("status")
        parser_status.add_argument("repo", nargs="+",
                                   help="A repository directory")
        parser_status.set_defaults(func=self.status_command)

        self.quiet = False
        self.verbose = False

    def init(self):
        super(GhostCommand, self).init()

        if self.args.user is None:
            _plano.exit("No user name")

        if "func" not in self.args:
            _plano.exit("Missing subcommand")

    def run(self):
        pass

    def clone_command(self):
        pass

    def init_command(self):
        pass

    def status_command(self):
        pass

def main():
    config = load_config()

    args.func(args)

def load_config():
    user_dir = os.path.expanduser("~")
    config_file = os.path.join(user_dir, ".config", "ghost", "config.py")
    config = dict()

    if os.path.exists(config_file):
        entries = runpy.run_path(config_file, config)
        config.update(entries)

    return config

def clone(args):
    if exists(args.repo):
        exit("Path already exists")

    call("git clone git@github.com:{}/{}.git", args.user, args.repo)

def init(args):
    if exists(join(args.repo, ".git")):
        sys.exit("The directory is already initialized")

    with working_dir(args.repo):
        call("git init")
        call("git add .")
        call("git commit -m \"Initial commit\"")
        call("git remote add origin git@github.com:{}/{}.git", args.user, args.repo)
        call("git push --set-upstream origin master")

def status(args):
    set_message_threshold("warn")

    for repo in args.repo:
        if not exists(join(repo, ".git")):
            continue

        sys.stdout.write("## {:<40} ".format(repo))

        with working_dir(repo):
            output = call_for_output("git status -sb")

        sys.stdout.write(output)
        sys.stdout.flush()
