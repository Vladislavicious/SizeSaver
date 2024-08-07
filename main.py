import sys
from Options.argHandler import ArgumentHandler
from Misc.codes import ResultCodes

if __name__ == "__main__":
  handler = ArgumentHandler()
  args = handler.parse(sys.argv[1:])
  result, description = handler.react()
  if result != ResultCodes.OK:
    print(f"ERROR: {description}\n\n")
    handler.printHelp()
    exit(result.value)
