'''CLI command builder'''

import typing

KeyType = str
ValueType = typing.List[str]


class CommandBuilder:
  '''CLI command builder'''

  def __init__(self):
    # Command being built. Append order is preserved.
    self._cmd = []

    # Pairs of (option name, corresponding option value) for validation (e.g. reject duplication).
    self._args = {}  # TODO Deprecate
    self._kwargs: typing.Dict[KeyType, ValueType] = {}

  def append_raw_arg(self, arg):
    self._cmd.append(arg)

  def append_keyword_arg(self, key: str, *values: str) -> None:
    # Validate `key`
    if not isinstance(key, str):
      raise TypeError(f'Expected string-typed `key`, got: {type(key)}')
    if not key.startswith('--'):
      raise ValueError(f'`key` must start with "--", got: {key}')
    if key in self._kwargs:
      prev_values = self._kwargs[key]
      if len(values) != len(prev_values) or any(v1 != v2 for v1, v2 in zip(values, prev_values)):
        raise ValueError(f'"{key}" is already included in the command, with value "{prev_values}".')

    # Validate `values`
    if any(not isinstance(v, str) for v in values):
      raise TypeError(f'Expected string-typed values, got: {tuple(type(v) for v in values)}')

    # Update `self._kwargs` and `self._cmd`
    self._kwargs[key] = list(values)
    self.append_raw_arg(key)
    for value in values:
      self.append_raw_arg(value)

  def build(self):
    assert all(isinstance(arg, str) for arg in self._cmd)
    return self._cmd
