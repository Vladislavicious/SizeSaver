import unittest

import pandas as pd
from Options.argHandler import ArgumentHandler
from Misc.codes import ResultCodes

class TestArgumentHandler(unittest.TestCase):
  def test_createArgParser(self):
    argHandler = ArgumentHandler()
    self.assertEqual(type(argHandler), ArgumentHandler)

  def test_parseNone(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse(None)
    self.assertEqual(type(result), dict)

    self.assertEqual(result["filepath"], "")

  def test_parseEmptyStr(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse("")
    self.assertEqual(type(result), dict)

    self.assertEqual(result["filepath"], "")

  def test_parseStrNoOptions(self):
    argHandler = ArgumentHandler()
    result = False
    try:
      result = argHandler.parse(["aboba"])
    except:
      result = True

    self.assertTrue(result)

  def test_parseStrFilepathOption(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse("--filepath aboba".split(" "))
    self.assertEqual(result["filepath"], "aboba")

  def test_parseStrFilepathOptionWithEqualSign(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse(["--filepath=aboba"])
    self.assertEqual(result["filepath"], "aboba")

  def test_parseStrInQuotationMarks(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse(["asdf asdf"])
    self.assertEqual(result["string"], "asdf asdf")

  def test_parseFilepathInQuotationMarks(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse(["--filepath", "asdf asdf"])
    self.assertEqual(result["filepath"], "asdf asdf")

  def test_parseFilepathInQuotationMarksWithEqualSign(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse(['--filepath=asdf asdf'])
    self.assertEqual(result["filepath"], "asdf asdf")

  def test_parseStrAndFilepathSimultinous(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse(["--filepath=asdf", "sheeh"])
    self.assertEqual(result["filepath"], "asdf")
    self.assertEqual(result["string"], "sheeh")

  def test_parseSaveFile(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse(["--save", "here"])
    self.assertEqual(result["save"], "here")

  def test_reactOnExistingFile(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse(["--filepath=./Tests/Files/TestFile1.txt"])

    result, description = argHandler.react()
    self.assertEqual(result, ResultCodes.OK, description)

  def test_reactOnNonExistingFile(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse(["--filepath=./Tests/Fil.txt"])

    result, description = argHandler.react()
    self.assertEqual(result, ResultCodes.NO_FILE, description)
