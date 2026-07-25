# MISPFuse build. Requires Python 3.13 available locally so ucc-gen installs
# PyMISP against the matching interpreter.
TA      := mispfuse
VERSION := 2.0.0
OUT     := output/$(TA)

.PHONY: build package all clean appinspect

all: package

build:
	ucc-gen build --source package --ta-version $(VERSION)
	python3 post_build.py $(OUT)

package: build
	ucc-gen package --path $(OUT)

appinspect: package
	splunk-appinspect inspect $(TA)-$(VERSION).tar.gz \
		--mode precert --included-tags cloud

clean:
	rm -rf output *.tar.gz
