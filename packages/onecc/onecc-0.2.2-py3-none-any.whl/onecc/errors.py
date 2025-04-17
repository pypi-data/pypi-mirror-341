'''Errors for onecc'''


class CommandNotFoundError(RuntimeError):
  '''Failed to find a cli command'''


class CommandError(RuntimeError):
  '''Failed to run a cli command'''
