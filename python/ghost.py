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
import sys as _sys

from plano import *

def load_config():
    config_file = join(get_home_dir(), ".config/ghost/config.py")
    config = dict()

    if exists(config_file):
        entries = _runpy.run_path(config_file, config)
        config.update(entries)

    return Namespace(**config)

def repo_url(owner, repo_name):
    return f"git@github.com:{owner}/{repo_name}.git"

_config = load_config()
_config_owner = getattr(_config, "owner", None)

_repo_name_arg = CommandArgument("repo_name", positional=True, help="The name of the desired repo")
_repo_dir_arg = CommandArgument("repo_dir", positional=True, help="The directory containing the repo")
_output_dir_arg = CommandArgument("output_dir", positional=True, help="The output directory")
_owner_arg = CommandArgument("owner", help="The GitHub user or organization containing the repo")

@command(args=(_repo_name_arg, _output_dir_arg, _owner_arg))
def clone(repo_name, output_dir=None, owner=_config_owner):
    """
    Clone a repo from GitHub
    """

    check_program("git")

    output_dir = nvl(output_dir, repo_name)

    run(f"git clone {repo_url(owner, repo_name)} {output_dir}")

@command(args=(_repo_dir_arg, _owner_arg))
def init(repo_dir=".", repo_name=None, owner=_config_owner):
    """
    Initialize a repo
    """

    check_program("git")

    if exists(join(repo_dir, ".git")):
        exit("The directory is already initialized")

    if repo_dir in (".", ".."):
        repo_dir = get_absolute_path(repo_dir)

    repo_name = nvl(repo_name, get_base_name(repo_dir))

    with working_dir(repo_dir):
        run("git init")
        run("git add .")
        run("git commit -m Initial")
        run("git branch -M main")
        run(f"git remote add origin {repo_url(owner, repo_name)}")

        print("Make sure this repo exists on GitHub and then push:")
        print(f"git push -u origin main")

@command(args=(_repo_dir_arg,))
def uninit(repo_dir="."):
    """
    Uninitialize a repo
    """

    git_dir = join(repo_dir, ".git")

    check_dir(git_dir)
    remove(git_dir)

@command
def status(*repo_dirs):
    """
    Report the status of multiple repos
    """

    if not repo_dirs:
        repo_dirs = (".",)

    for repo_dir in repo_dirs:
        if not exists(join(repo_dir, ".git")):
            continue

        _sys.stdout.write("## {:<40} ".format(repo_dir))

        with working_dir(repo_dir, quiet=True):
            output = call("git status -sb", quiet=True)

        _sys.stdout.write(output)
        _sys.stdout.flush()

@command(args=(_repo_name_arg, _output_dir_arg, _owner_arg))
def subrepo(repo_name, output_dir, owner=_config_owner):
    """
    Clone a repo from GitHub into an existing repo subdirectory
    """

    assert output_dir is not None

    run(f"git subrepo clone {repo_url(owner, repo_name)} {output_dir}")

@command(args=(_repo_name_arg, _owner_arg))
def url(repo_name, owner=_config_owner):
    """
    Print the URL for a GitHub repo
    """

    print(repo_url(owner, repo_name))

def main():
    module = _sys.modules[__name__]
    description = "Commands for working with my GitHub repos"

    PlanoCommand(module, description=description).main()
