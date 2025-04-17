'''Adapter to convert python kwargs into command-line arguments for argparse module'''

import typing

from onecc._cli.command_builder import ValueType as _CLIOptionValueType

PyOptionValueType = \
    typing.Union[bool, int, float, str, typing.Iterable[typing.Union[int, float, str]]]


class OptionSchema:
  '''This class knows the list of options names and their types of each onecc subcommand,
     as much as `onecc` package requires.'''

  def is_store_true_type(self, option_name: str) -> bool:
    '''Returns true if the given option is "store_true" type option.

    Question)

    Why do we need this feature?

    Answer)

    `argparse` does not recommend boolean typed arguments.

    From https://docs.python.org/3/library/argparse.html#type:
    > The bool() function is not recommended as a type converter. All it does is convert empty
    > strings to False and non-empty strings to True. This is usually not what is desired.

    Instead, it is a common practice to use "store_true" actions for arguments with boolean types.

    Checking if an argument is "store_true" type or not allows safely converting:
    * the python kwargs option `{"enable_something": True}`
    * into the command-line argument `["--enable_something"]`.
    '''
    raise NotImplementedError('Child class must override this method')


class OptionNormalizer:
  '''Helper class to convert python kwargs into command-line arguments for argparse module'''

  def __init__(self, option_schema):
    self._schema = option_schema

  def _normalize_option_name(self, option_name: str) -> str:
    '''Normalize the option name

    :param option_name: User-given option name, without the prefix '--'
    :returns: Normalized option name, with the prefix '--'
    '''

    if not isinstance(option_name, str):
      raise TypeError(f'Expected string for `option_name`, got {type(option_name)}')

    if option_name.startswith('--'):
      raise ValueError('Expected option name without the prefix "--"')

    return f'--{option_name}'

  def _normalize_option_value(self, option_name: str,
                              option_value: PyOptionValueType) -> _CLIOptionValueType:
    '''Normalize the option value

    :param option_name: Option name (without the prefix '--')
    :param option_value: Option value (of python primitive data type, or a list of them).
    :returns: Normalized option value (of a list of string type).
    '''

    if isinstance(option_value, bool):
      if self._schema.is_store_true_type(option_name):
        if option_value is True:
          return []
        else:
          assert option_value is False
          raise ValueError(f'`{option_name}` cannot accept `False` as argument')
      else:
        raise TypeError(f'`{option_name}` cannot accept booleans as argument')
    elif isinstance(option_value, (int, float)):
      return [str(option_value)]
    elif isinstance(option_value, str):
      return [option_value]
    elif isinstance(option_value, (list, tuple)):
      # NOTE Python returns `True` for `isinstance(True, int)`.
      # Therefore, the bool-check is done before int-check.
      if any(isinstance(v, bool) for v in option_value):
        raise TypeError('Failed to normalize `option_value`')
      elif all(isinstance(v, (str, int, float)) for v in option_value):
        return [str(v) for v in option_value]
      else:
        raise TypeError('Failed to normalize `option_value`')
    else:
      raise TypeError('Failed to normalize `option_value`')


  def _normalize_option(self, option_name: str, option_value: PyOptionValueType) \
                       -> typing.Tuple[str, _CLIOptionValueType]:
    '''Normalize the name and value of a keyword option.'''
    normalized_option_name = self._normalize_option_name(option_name)
    normalized_option_value = self._normalize_option_value(option_name, option_value)

    return normalized_option_name, normalized_option_value

  def __call__(self, **kwargs):
    '''Normalize the name and value of given keyword options.'''
    ret = {}
    for k, v in kwargs.items():
      nk, nv = self._normalize_option(k, v)
      ret[nk] = nv

    return ret
