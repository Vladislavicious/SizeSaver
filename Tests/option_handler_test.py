import unittest

from Misc.codes import ResultCodes
from Options.handler import OptionsHandler

# Обработка пустой строки
# Определение, что в строке адрес файла
# Определение, что в строке ничего нет
# Определение, что строка содержит верную инфу
# Определение, что переданы неправильные параметры

class TestOptionsHandler(unittest.TestCase):
  def test_CreateOptionsHandler(self):
    handler = OptionsHandler("fakeOption")
    self.assertEqual(type(handler), OptionsHandler)

  def test_ParseFileAddressStr(self):
    handler = OptionsHandler("./Tests/Files/TestFile2.txt")
    result, description = handler.parse()
    self.assertEqual(result, ResultCodes.OK)

  def test_ParseEmptyOptions(self):
    handler = OptionsHandler("")
    result, description = handler.parse()
    self.assertEqual(result, ResultCodes.NO_OPTIONS)

  def test_ParseGoodOptionsStr(self):
    stroka = "   text	   data	    bss	    dec	    hex	filename\n648	      0	     15	    663	    297	./bin/uno/FirstProject/FirstProject_.elf\n"
    handler = OptionsHandler(stroka)
    result, description = handler.parse()
    self.assertEqual(result, ResultCodes.OK)

  def test_ParseWrongAddress(self):
    handler = OptionsHandler("./Test/f.txt")
    result, description = handler.parse()
    self.assertEqual(result, ResultCodes.NO_FILE)

  def test_ParseBadOptionsStr(self):
    stroka = "   text	   data	    bss	    dec	    hex	filename\ngcc	      +	     avr	    =	    evil	./bin/uno/FirstProject/FirstProject_.elf\n"
    handler = OptionsHandler(stroka)
    result, description = handler.parse()
    self.assertEqual(result, ResultCodes.OK)

    result, description = handler.parse_df()
    self.assertEqual(result, ResultCodes.BAD_DATA)

  def test_ParseDfGoodOptionsStr(self):
    stroka = "   text	   data	    bss	    dec	    hex	filename\n648	      0	     15	    663	    297	./bin/uno/FirstProject/FirstProject_.elf\n"
    handler = OptionsHandler(stroka)
    result, description = handler.parse()
    self.assertEqual(result, ResultCodes.OK)

    result, description = handler.parse_df()
    self.assertEqual(result, ResultCodes.OK, description)
