WORK_DIR=$(shell pwd)
MOUNT_DIR_LOCAL="$(WORK_DIR)/test_mnt"
MOUNT_DIR_CONTAINER="/data"
PROJECT_NAME="cpp-training-bot"
IMAGE_FILE="$(PROJECT_NAME).tar"
ENV_VARIABLES_FILE="env_variables"

build:
	@docker build -t $(PROJECT_NAME) .
run:
	@docker run \
	-t \
	--rm \
	-v $(MOUNT_DIR_LOCAL):$(MOUNT_DIR_CONTAINER) \
	--env-file=$(ENV_VARIABLES_FILE) \
	$(PROJECT_NAME)
run-it:
	@docker container run \
	--rm \
	-v $(MOUNT_DIR_LOCAL):$(MOUNT_DIR_CONTAINER) \
	--env-file=$(ENV_VARIABLES_FILE) \
	-it $(PROJECT_NAME) /bin/bash
save:
	@docker save $(PROJECT_NAME) > $(IMAGE_FILE)
load:
	@docker load -i $(IMAGE_FILE)


