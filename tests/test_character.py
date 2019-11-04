import unittest

import pressagio.character


class TestCharacter(unittest.TestCase):
    def test_first_word_character(self):
        assert pressagio.character.first_word_character("8238$§(a)jaj2u2388!") == 7
        assert pressagio.character.first_word_character("123üäö34ashdh") == 3
        assert pressagio.character.first_word_character("123&(/==") == -1

    def test_last_word_character(self):
        assert pressagio.character.last_word_character("8238$§(a)jaj2u2388!") == 13
        assert pressagio.character.last_word_character("123üäö34ashdh") == 12
        assert pressagio.character.last_word_character("123&(/==") == -1

    def test_is_word_character(self):
        assert pressagio.character.is_word_character("ä") == True
        assert pressagio.character.is_word_character("1") == False
        assert pressagio.character.is_word_character(".") == False
