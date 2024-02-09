
IMAGE_NAME=air-quality-server
RUN=docker run \
	--rm -it \
	--name $(IMAGE_NAME)-dev \
	-v $(PWD):/workdir \
	--network host \
	-it $(IMAGE_NAME)-dev:latest

build:
	docker build -t $(IMAGE_NAME)-dev:latest .

start:
	@docker-compose up -d

stop:
	@docker-compose down

sh:
	@$(RUN) sh
