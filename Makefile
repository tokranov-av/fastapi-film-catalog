redis_volume:
	docker volume create fastapi-film-catalog

redis_dev:
	docker container run --name redis-film-catalog -d -p 6379:6379 -v fastapi-film-catalog:/data redis

redis_test:
	docker container run --name redis-film-catalog-tests -d -p 6380:6379 redis
