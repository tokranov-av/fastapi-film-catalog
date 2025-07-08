from unittest import TestCase

from api.api_v1.auth.services import redis_tokens


class RedisTokensHelperTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        expected_exists = True

        new_token = redis_tokens.generate_and_save_token()

        self.assertEqual(
            expected_exists,
            redis_tokens.token_exists(new_token),
        )
