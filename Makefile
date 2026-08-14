# Build with Python 3.13; the release gate tests all supported runtimes.
TA      := mispfuse
VERSION := 2.2.4
OUT     := output/$(TA)
PYTHON  ?= python3
PYTHON37 ?= python3.7
PYTHON39 ?= python3.9
PYTHON313 ?= python3.13
APPINSPECT_REPORT := $(TA)-$(VERSION)-appinspect-4.3.0.json

.PHONY: all build package test test-python37 test-python39 test-python313 appinspect release clean purge-bytecode

all: package

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v

test-python37:
	$(MAKE) test PYTHON=$(PYTHON37)

test-python39:
	$(MAKE) test PYTHON=$(PYTHON39)

test-python313:
	$(MAKE) test PYTHON=$(PYTHON313)

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
		--mode precert --included-tags cloud \
		--data-format json --output-file $(APPINSPECT_REPORT)

release: clean test-python37 test-python39 test-python313 appinspect
	@echo "Release candidate created: $(TA)-$(VERSION).tar.gz"
	@echo "AppInspect report created: $(APPINSPECT_REPORT)"

clean:
	rm -rf output *.tar.gz $(APPINSPECT_REPORT)
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
