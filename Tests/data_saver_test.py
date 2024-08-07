import unittest

import pandas as pd

from Misc.codes import ResultCodes
from DataWorker.worker import *

    # Передается файл для сохранения информации
    # Файл не передан, создается стандартный
    # Файл не передан, стандартный существует
    # Передан файл не с тем расширением
    # Запись DataFrame'а в файл

class TestFileDataWorker(unittest.TestCase):
  def common_DeleteFile(self, filename: str):
    if os.path.exists(filename):
      os.remove(filename)

  def test_InitFileDataWorkerWithFile(self):
    saver = FileDataWorker("file.csv")
    self.assertEqual(type(saver), FileDataWorker)

  def test_InitializeFileDataWorkerNoFile(self):
    saver = FileDataWorker(None)
    self.assertEqual(type(saver), FileDataWorker)

  def test_CheckFileValidityProperFile(self):
    saver = FileDataWorker("./Tests/Files/file.csv")
    result, description = saver.CheckFile()
    self.assertEqual(result, ResultCodes.OK)

  def test_CheckFileValidityBadFile(self):
    badName = "fil1234e.csv"
    self.common_DeleteFile(badName)
    self.assertFalse(os.path.exists(badName))

    saver = FileDataWorker(badName)
    result, description = saver.CheckFile()
    self.assertEqual(result, ResultCodes.OK)

    self.assertTrue(os.path.exists(badName))
    self.common_DeleteFile(badName)

  def test_CantCreateBadFile(self):
    badName = "/fil1234e.csv"
    self.assertFalse(os.path.exists(badName))
    self.common_DeleteFile(badName)

    saver = FileDataWorker(badName)
    result, description = saver.CheckFile()
    self.assertEqual(result, ResultCodes.CANT_CREATE_FILE)

    self.assertFalse(os.path.exists(badName))

  def test_CheckFileValidityStandartFile(self):
    saver = FileDataWorker(None)
    result, description = saver.CheckFile()
    self.assertEqual(result, ResultCodes.OK)
    self.common_DeleteFile(STANDARD_FILENAME)

  def test_CheckFileBadFormat(self):
    saver = FileDataWorker("file.bad")
    result, description = saver.CheckFile()
    self.assertEqual(result, ResultCodes.BAD_FILE_FORMAT)

  def test_WriteDfToStandardFile(self):
    saver = FileDataWorker(None)
    result, description = saver.CheckFile()
    self.assertEqual(result, ResultCodes.OK)

    df = pd.DataFrame(data=[1, 2, 3, 4, 5], columns=["data"])
    result, description = saver.WriteDfToFile(df)
    self.assertEqual(result, ResultCodes.OK)

    self.assertTrue(os.path.exists(STANDARD_FILENAME))
    self.common_DeleteFile(STANDARD_FILENAME)

  def test_ReadFromStandardFile(self):
    self.common_DeleteFile(STANDARD_FILENAME)

    saver = FileDataWorker(None)
    result, description = saver.CheckFile()
    self.assertEqual(result, ResultCodes.OK)
    self.assertTrue(os.path.exists(STANDARD_FILENAME))

    df = pd.DataFrame(data=[1, 2, 3, 4, 5], columns=["data"])
    df.to_csv(saver.getFilename(), index=False)

    newDf = saver.ReadDfFromFile()
    equal = df.equals(newDf)
    self.assertTrue(equal)
    self.common_DeleteFile(STANDARD_FILENAME)

  def test_AppendDataToStandardFile(self):
    self.common_DeleteFile(STANDARD_FILENAME)
    self.assertFalse(os.path.exists(STANDARD_FILENAME))

    saver = FileDataWorker(None)
    result, description = saver.CheckFile()
    self.assertEqual(result, ResultCodes.OK)
    self.assertTrue(os.path.exists(STANDARD_FILENAME))

    df = pd.DataFrame(data=[1, 2, 3, 4, 5], columns=["data"])
    result, description = saver.WriteDfToFile(df)
    self.assertEqual(result, ResultCodes.OK)

    result, description = saver.WriteDfToFile(df)
    self.assertEqual(result, ResultCodes.OK)

    newDf = pd.DataFrame(data=[1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
                         columns=["data"])
    readDf = saver.ReadDfFromFile()
    equal = newDf.equals(readDf)
    self.assertTrue(equal)
    self.common_DeleteFile(STANDARD_FILENAME)
