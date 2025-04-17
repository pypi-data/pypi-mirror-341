'''Experimental automatic configuration for `onecc optimize`'''

import typing
from onecc._cli.adapter import PyOptionValueType

# NOTE The implementation in this file follows the below guide.
# https://pages.github.sec.samsung.net/AIP/ONE_User_Guide/latest/html/command_line_interface/group_option.html


def _get_tv2_options() -> typing.Dict[str, PyOptionValueType]:
  return {
      'O1': True,
  }


def _get_tv2_onnx_options() -> typing.Dict[str, PyOptionValueType]:
  return {
      'convert_nchw_to_nhwc': True,
  }


def _get_tv2_tflite_options() -> typing.Dict[str, PyOptionValueType]:
  return {}


def _get_tv2_circle_options() -> typing.Dict[str, PyOptionValueType]:
  return {}


def get_options(*, model: str, backend: str) -> typing.Dict[str, PyOptionValueType]:
  options = {}

  # TODO Revisit the backend name
  if backend in ['tv2', 'triv2', 'triv23', 'triv24']:
    options.update(_get_tv2_options())

    if model == 'onnx':
      options.update(_get_tv2_onnx_options())
    elif model == 'tflite':
      options.update(_get_tv2_tflite_options())
    elif model == 'circle':
      options.update(_get_tv2_circle_options())
    else:
      raise NotImplementedError(f'Cannot get options for {model}')

  else:
    raise NotImplementedError(f'Cannot get options for backend {backend}')

  return options
