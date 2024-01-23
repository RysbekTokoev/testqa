from typing import List

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTPage


class Parser:
    def __init__(self, pdf_path: str):
        """
        :param pdf_path: Путь к pdf файлу
        """
        self.pdf_path = pdf_path
        self.pages = extract_pages(pdf_path)

    @staticmethod
    def get_text_elements(page: LTPage) -> List[LTTextContainer]:
        """
        Достать все текста со страницы
        :return texts: Элементы текста на странице
        """
        texts = [el for el in page if isinstance(el, LTTextContainer)]
        return texts

    def get_labels(self, page, separator: str = ":"):
        """
        :param separator: Строка по которой определяется является ли текст лейблом, на случай если символ сменится
        :return texts: List[str] - Лейблы
        """
        texts = self.get_text_elements(page)
        labels = [s.get_text() for s in texts if separator in s.get_text()]
        return labels
