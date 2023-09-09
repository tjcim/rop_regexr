###
# ROP Regexr Makefile
###

.PHONY: build run down run_static
.DEFAULT_GOAL := run

# Variables
NAME = rop_regexr
INTERNAL_PORT = 5000
EXTERNAL_PORT = 5001

build:
	@echo "Building ${NAME}"
	docker build -t ${NAME} .

run:
	@echo "Running ${NAME} on random port"
	docker run --rm -d -p ${INTERNAL_PORT} --name="${NAME}" ${NAME}
	docker container port ${NAME}

run_static:
	@echo "Running ${NAME} on port ${EXTERNAL_PORT}"
	docker run --rm -d -p ${EXTERNAL_PORT}:${INTERNAL_PORT} --name="${NAME}" ${NAME}

down:
	@echo "Stopping ${NAME}"
	docker container stop ${NAME}
