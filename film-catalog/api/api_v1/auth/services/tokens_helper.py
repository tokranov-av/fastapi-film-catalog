from abc import ABC, abstractmethod
import secrets


class AbstractTokensHelper(ABC):
    """
    Что мне нужно от обертки:
    - проверять на наличие токена
    - добавлять токен в хранилище
    - сгенерировать и добавить токены
    """

    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        """
        Check whether a token exists.

        :param token:
        :return:
        """

    @abstractmethod
    def add_token(
        self,
        token: str,
    ) -> None:
        """
        Save token in storage.

        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls):
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)

        return token

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Returns a list of tokens.

        :return:
        """

    @abstractmethod
    def delete_token(self, token: str) -> None:
        """
        Deletes a token.

        :param token:
        :return:
        """
