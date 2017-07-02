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

DESTDIR := ""
PREFIX := ${HOME}/.local
GHOST_HOME = ${PREFIX}/share/ghost

export PATH := ${PREFIX}/bin:${PATH}

.PHONY: default
default: devel

.PHONY: help
help:
	@echo "clean          Clean up the source tree"
	@echo "build          Build the code"
	@echo "install        Install the code"
	@echo "test           Run tests"
	@echo "devel          Clean, build, install, test"

.PHONY: clean
clean:
	find python -type f -name \*.pyc -delete
	find python -type d -name __pycache__ -delete
	rm -rf build
	rm -rf install

.PHONY: build
build:
	mkdir -p build/bin
	scripts/configure-file -a ghost_home ${GHOST_HOME} bin/ghost.in build/bin/ghost
	chmod 755 build/bin/ghost

.PHONY: install
install: build
	scripts/install-files -n \*.py python ${DESTDIR}${GHOST_HOME}/python
	scripts/install-files files ${DESTDIR}${GHOST_HOME}/files
	scripts/install-files build/bin ${DESTDIR}${PREFIX}/bin

.PHONY: test
test: PREFIX := install
test: devel

.PHONY: devel
devel: PREFIX := install
devel: clean install
	ghost --init-only status example
