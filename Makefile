ENV_VARIABLES_FILE=env_variables
include $(ENV_VARIABLES_FILE)

WORK_DIR=$(shell pwd)
MOUNT_DIR_LOCAL="$(WORK_DIR)/test_mnt"
MOUNT_DIR_CONTAINER="/data"
PROJECT_NAME="cpp-training-bot"
IMAGE_FILE="$(PROJECT_NAME).tar"
#	--build-arg DATA_DIR=$(DATA_DIR) \

build:
	@docker build \
	--build-arg TELEGRAM_USER_ID=$(TELEGRAM_USER_ID) \
	--build-arg TELEGRAM_BOT_TOKEN=$(TELEGRAM_BOT_TOKEN) \
	--build-arg TZ=$(TZ) \
	-t \
	$(PROJECT_NAME) .
run:
	@docker run \
	-t \
	--rm \
	-v $(MOUNT_DIR_LOCAL):$(MOUNT_DIR_CONTAINER) \
	$(PROJECT_NAME)
run-it:
	@docker container run \
	--rm \
	-v $(MOUNT_DIR_LOCAL):$(MOUNT_DIR_CONTAINER) \
	-it $(PROJECT_NAME) /bin/bash
save:
	@docker save $(PROJECT_NAME) > $(IMAGE_FILE)
load:
	@docker load -i $(IMAGE_FILE)


