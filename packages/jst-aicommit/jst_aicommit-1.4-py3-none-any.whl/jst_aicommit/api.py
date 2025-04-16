from typing import Union
from tenacity import retry, stop_after_attempt, retry_if_not_exception_type
from jst_aicommit.exceptions import JstException
from g4f.client import Client
from g4f.Provider import Pizzagpt
import re
import logging


class AI:
    block_chars = ["git commit -m", "git commit -m "]

    def __init__(self) -> None:
        self.client = Client()

    def _clean_response(self, text: Union[str]) -> Union[str]:
        for block in self.block_chars:
            text = text.replace(block, "")
        return text

    def _get_commit(self, text):
        response = re.search(r"```(.*?)```", text, re.DOTALL).group(1).strip()
        if response.startswith("bash"):
            response = response[6:]
        if response.startswith("git"):
            response = response[5:]
        if response.startswith('"'):
            response = response[1:]
        if response.endswith('"'):
            response = response[:-1]
        return response

    @retry(stop=stop_after_attempt(5), retry=retry_if_not_exception_type(JstException))
    def get_commit(self, text: Union[str]) -> Union[str]:
        """Commit generatsiya qilish uchun api request"""
        request_text = """
        Manabunga o'zbekcha git commit yozib ber iloji boricha qisqa bo'lsin```{}```
        """.format(
            text
        )
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                provider=Pizzagpt,
                messages=[{"role": "user", "content": request_text}],
            )
            response = self._clean_response(response.choices[0].message.content)
        except Exception as e:
            logging.error(e)
            raise Exception("API request except retry")
        try:
            return self._get_commit(response)
        except Exception as e:
            logging.error(e)
            raise JstException(response, code=JstException.ERROR_MATCH)
