'''Experimental automatic configuration for `onecc import`'''

import typing
from onecc._cli.adapter import PyOptionValueType


def _get_tv2_tflite_options() -> typing.Dict[str, PyOptionValueType]:
  return {}


def _get_tv2_onnx_options() -> typing.Dict[str, PyOptionValueType]:
  return {
      'unroll_lstm': True,
      'keep_io_order': True,
      'experimental_disable_batchmatmul_unfold': True,
  }


def _get_tv2_circle_options() -> typing.Dict[str, PyOptionValueType]:
  return {}


def get_options(*, model: str, backend: str) -> typing.Dict[str, PyOptionValueType]:
  options = {}

  # TODO Revisit the backend name
  if backend in ['tv2', 'triv2', 'triv23', 'triv24']:
    if model == 'onnx':
      options.update(_get_tv2_onnx_options())
    elif model == 'tflite':
      options.update(_get_tv2_tflite_options())
    elif model == 'circle':
      options.update(_get_tv2_circle_options())
    else:
      raise NotImplementedError(f'Cannot get options for {model}')

  else:
    raise NotImplementedError(f'Cannot get options for {backend}')

  return options
