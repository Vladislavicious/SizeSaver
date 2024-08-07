import unittest
import os.path

import pandas as pd
from Options.argHandler import ArgumentHandler
from Misc.codes import ResultCodes
from DataWorker.worker import STANDARD_FILENAME

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

    df = argHandler.getRefinedData()
    self.assertTrue(type(df) is not None)


  def test_reactOnNonExistingFile(self):
    argHandler = ArgumentHandler()
    result = argHandler.parse(["--filepath=./Tests/Fil.txt"])

    result, description = argHandler.react()
    self.assertEqual(result, ResultCodes.NO_FILE, description)

  def test_fullCycleWithExistingString(self):
    argHandler = ArgumentHandler()
    saveFileName = "saveStringFile.csv"
    if os.path.exists(saveFileName):
      os.remove(saveFileName)
    self.assertFalse(os.path.exists(saveFileName))

    with open("./Tests/Files/TestFile1.txt", "r", encoding="utf-8") as file:
      string = file.read()

    result = argHandler.parse([string, "--save", saveFileName])
    result, description = argHandler.react()
    self.assertEqual(result, ResultCodes.OK, description)

    df = argHandler.getRefinedData()
    self.assertTrue(type(df) is not None)
    self.assertTrue(os.path.exists(saveFileName))

  def test_fullCycleWithExistingFile(self):
    argHandler = ArgumentHandler()
    saveFileName = "saveFile.csv"
    if os.path.exists(saveFileName):
      os.remove(saveFileName)
    self.assertFalse(os.path.exists(saveFileName))

    result = argHandler.parse(["--filepath", "./Tests/Files/TestFile1.txt", "--save", saveFileName])
    result, description = argHandler.react()
    self.assertEqual(result, ResultCodes.OK, description)

    df = argHandler.getRefinedData()
    self.assertTrue(type(df) is not None)
    self.assertTrue(os.path.exists(saveFileName))
