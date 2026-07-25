# Build with Python 3.13, matching the Splunk 10.2 runtime used by the app.
TA      := mispfuse
VERSION := 2.1.0
OUT     := output/$(TA)
PYTHON  ?= python3

.PHONY: all build package test appinspect release clean purge-bytecode

all: package

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v

purge-bytecode:
	find package tests -type d -name __pycache__ -prune -exec rm -rf {} +
	find package tests -type f -name '*.py[co]' -delete

build:
	$(MAKE) purge-bytecode
	ucc-gen build --source package --ta-version $(VERSION)
	$(PYTHON) post_build.py $(OUT)

package: build
	ucc-gen package --path $(OUT)

appinspect: package
	splunk-appinspect inspect $(TA)-$(VERSION).tar.gz \
		--mode precert --included-tags cloud

release: clean test appinspect
	@echo "Release candidate created: $(TA)-$(VERSION).tar.gz"

clean:
	rm -rf output *.tar.gz
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
