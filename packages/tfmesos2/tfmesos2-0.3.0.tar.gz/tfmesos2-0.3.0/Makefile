#Dockerfile vars
#vars
IMAGENAME=tensorflow-mesos
REPO=avhost
TAG=$(shell git describe --tags --abbrev=0)
BRANCH=$(shell git symbolic-ref --short HEAD | xargs basename)
BRANCHSHORT=$(shell echo ${BRANCH} | awk -F. '{ print $$1"."$$2 }')
BUILDDATE=$(shell date -u +%Y%m%d)
IMAGEFULLNAME=${REPO}/${IMAGENAME}
LASTCOMMIT=$(shell git log -1 --pretty=short | tail -n 1 | tr -d " " | tr -d "UPDATE:")

.PHONY: help build bootstrap all

help:
	    @echo "Makefile arguments:"
	    @echo ""
	    @echo "Makefile commands:"
	    @echo "build"
	    @echo "all"
			@echo "publish"
			@echo ${TAG}

.DEFAULT_GOAL := all

ifeq (${BRANCH}, master)
     BRANCH=latest
     BRANCHSHORT=latest
endif

build:	
	@echo ">>>> Build python module"
	@python3 setup.py sdist bdist_wheel

push:
	@echo ">>>> Publish docker image: " ${BRANCH}
	@docker buildx create --use --name buildkit
	@docker buildx build --sbom=true --provenance=true --platform linux/amd64 --push --build-arg TAG=${BRANCH} --build-arg BUILDDATE=${BUILDDATE} -t ${IMAGEFULLNAME}:${BRANCH} .
	@docker buildx build --sbom=true --provenance=true --platform linux/amd64 --push --build-arg TAG=${BRANCH} --build-arg BUILDDATE=${BUILDDATE} -t ${IMAGEFULLNAME}:${BRANCHSHORT} .
	@docker buildx build --sbom=true --provenance=true --platform linux/amd64 --push --build-arg TAG=${BRANCH} --build-arg BUILDDATE=${BUILDDATE} -t ${IMAGEFULLNAME}:latest .
	@docker buildx rm buildkit


upload:
	@python3 -m twine upload --repository pypi dist/*

install:	
	@echo ">>>> Install python module"
	@pip3 install .

install-dev:	
	@echo ">>>> Install python module development"
	@pip3 install -e .

docs:
	@echo ">>>> Build docs"
	$(MAKE) -C $@

all: build
