import unittest

from Misc.codes import ResultCodes
from DataWorker.converter import DataConverter


class TestDataConverter(unittest.TestCase):
  def test_InitializeDataConverter(self):
    saver = DataConverter()
    self.assertEqual(type(saver), DataConverter)
