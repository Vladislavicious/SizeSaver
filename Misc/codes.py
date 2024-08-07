from enum import Enum

class ResultCodes(Enum):
  OK = 0
  NO_FILE = 1
  EMPTY_FILE = 2
  BAD_DATA = 3
  NO_ELF_FILE_EXISTS = 4
  NO_OPTIONS = 5
  BAD_FILE_FORMAT = 6
  SIMULTUNANEOUS_OPTIONS = 7
  CANT_CREATE_FILE = 8
