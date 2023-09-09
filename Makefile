###
# ROP Regexr Makefile
###

.PHONY: build run down
.DEFAULT_GOAL := run

# Variables
NAME = rop_regexr
PORT = 5000

build:
	@echo "Building ${NAME}"
	docker build -t ${NAME} .

run:
	@echo "Running ${NAME} on random port"
	docker run --rm -d -p ${PORT} --name="${NAME}" ${NAME}
	docker container port ${NAME}

down:
	@echo "Stopping ${NAME}"
	docker container stop ${NAME}
