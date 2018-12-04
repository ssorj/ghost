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

.NOTPARALLEL:

DESTDIR := ""
PREFIX := ${HOME}/.local
INSTALLED_GHOST_HOME = ${PREFIX}/share/ghost

export GHOST_HOME = ${CURDIR}/build/ghost
export PATH := ${CURDIR}/build/bin:${PATH}
export PYTHONPATH := ${GHOST_HOME}/python:${CURDIR}/python:${PYTHONPATH}

BIN_SOURCES := $(shell find bin -type f -name \*.in)
BIN_TARGETS := ${BIN_SOURCES:%.in=build/%}

PYTHON_SOURCES := $(shell find python -type f -name \*.py)
PYTHON_TARGETS := ${PYTHON_SOURCES:%=build/ghost/%} ${PYTHON_SOURCES:%.in=build/ghost/%}

.PHONY: default
default: build

.PHONY: help
help:
	@echo "build          Build the code"
	@echo "install        Install the code"
	@echo "clean          Clean up the source tree"
	@echo "test           Run tests"

.PHONY: clean
clean:
	find python -type f -name \*.pyc -delete
	find python -type d -name __pycache__ -delete
	rm -rf build

.PHONY: build
build: ${BIN_TARGETS} ${PYTHON_TARGETS} build/prefix.txt
#	scripts/smoke-test

.PHONY: install
install: build
	scripts/install-files build/bin ${DESTDIR}$$(cat build/prefix.txt)/bin
	scripts/install-files build/ghost ${DESTDIR}$$(cat build/prefix.txt)/share/ghost

#	scripts/install-files -n \*.py python ${DESTDIR}${GHOST_HOME}/python
#	scripts/install-files files ${DESTDIR}${GHOST_HOME}/files
#	scripts/install-files build/bin ${DESTDIR}${PREFIX}/bin

.PHONY: test
test: build
	scripts/test-ghost

build/prefix.txt:
	echo ${PREFIX} > build/prefix.txt

build/bin/%: bin/%.in
	scripts/configure-file -a ghost_home=${INSTALLED_GHOST_HOME} $< $@

build/ghost/python/%: python/% python/commandant.py python/plano.py
	@mkdir -p ${@D}
	cp $< $@

.PHONY: update-%
update-%:
	curl "https://raw.githubusercontent.com/ssorj/$*/master/python/$*.py" -o python/$*.py
