from redis import (
    Redis,
)

from core.config import (
    settings,
)

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.default,
    decode_responses=True,
)


def main() -> None:
    redis.set("name", "Artur")
    redis.set("foo", "bar")
    redis.set("number", "39")
    print("name:", redis.get("name"))
    print(
        [
            redis.get("foo"),
            redis.get("number"),
            redis.get("spam"),
        ],
    )
    redis.delete("name")
    print("name:", redis.get("name"))
    print("foo:", redis.get("foo"))


if __name__ == "__main__":
    main()
