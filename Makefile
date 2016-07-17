DESTDIR := ""
PREFIX := /usr/local
home = ${PREFIX}/share/ghost

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
	scripts/configure-file bin/gh.in build/bin/gh ghost_home ${home}
	chmod 755 build/bin/gh

.PHONY: install
install: build
	scripts/install-files python ${DESTDIR}${home}/python \*.py
	scripts/install-files files ${DESTDIR}${home}/files \*
	scripts/install-files build/bin ${DESTDIR}${PREFIX}/bin \*

.PHONY: test
test: PREFIX := ${PWD}/install
test: clean install
	${PREFIX}/bin/gh --init-only

.PHONY: devel
devel: PREFIX := ${PWD}/install
devel: clean install
	${PREFIX}/bin/gh --help
