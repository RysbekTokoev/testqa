from utils.parser import Parser
from data.constants import TICKET_LEFT_COL_LABELS as LEFT, TICKET_RIGHT_COL_LABELS as RIGHT, TICKET_LABELS
import pytest


@pytest.mark.parametrize("pdf_path", ["test_task.pdf"])
def test_check_layout(pdf_path):
    """
    ''Механизм, проверяющий входящие pdf-файлы на наличие всех элементов и соответствие структуры (расположение на листе)''
    :param pdf_path:
    :return:
    """
    parser = Parser(pdf_path)
    for page in parser.pages:
        elements = parser.get_text_elements(page)
        # O(n^2) сопоставление лейблов их элементам
        elements = {
            label: el
            for label in TICKET_LABELS
            for el in elements
            if label in el.get_text()
        }

        # Если какой-то лейбл не совпал текстом или повторился - ловим багу
        if len(elements.keys()) != len(TICKET_LABELS):
            missing_or_wrong_labels = [x for x in TICKET_LABELS if x not in elements.keys()]
            pytest.fail(f"Неверно указаны или отсутствуют лейблы: {missing_or_wrong_labels}")

        # Проверяем что каждый элемент в своей колонке расположен ниже предыдущего
        last_label = LEFT[0]
        for label in LEFT[1:]:
            assert elements[label].y1 <= elements[last_label].y0

        last_label = RIGHT[0]
        for label in RIGHT[1:]:
            assert elements[label].y1 <= elements[last_label].y0


