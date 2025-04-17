'''Experimental automatic configuration for `onecc quantize`'''

import typing
from onecc._cli.adapter import PyOptionValueType


def _get_tv2_options() -> typing.Dict[str, PyOptionValueType]:
  return {
      'granularity': 'channel',
  }


def get_options(*, model: str, backend: str) -> typing.Dict[str, PyOptionValueType]:

  del model  # TODO

  options = {}

  # TODO Revisit the backend name
  if backend in ['tv2', 'triv2', 'triv23', 'triv24']:
    options.update(_get_tv2_options())
  else:
    raise NotImplementedError(f'Cannot get options for {backend}')

  return options
