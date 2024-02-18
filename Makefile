
IMAGE_NAME=raq
RUN=docker run \
	--rm -it \
	--name $(IMAGE_NAME)-dev \
	-v $(PWD):/workdir \
	--network host \
	-it $(IMAGE_NAME)-dev:latest

build-dev:
	docker build -t $(IMAGE_NAME)-dev:latest --target dev .

build-server:
	@docker build -t $(IMAGE_NAME)-server:latest --target server . 

start:
	@docker-compose --profile dev up -d

stop:
	@docker-compose --profile dev down

make start-prod:
	@docker-compose --profile prod up -d

make stop-prod:
	@docker-compose --profile prod down

sh:
	@$(RUN) sh
