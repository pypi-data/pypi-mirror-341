'''Wrapper of `onecc quantize` command'''

import h5py as h5  # type: ignore
import numpy as np  # type: ignore
import typing
from pathlib import Path

from onecc._fs.workspace_registry import get_workspace as ws
from onecc._cli.adapter import OptionNormalizer
from onecc._cli.adapter import OptionSchema
from onecc._cli.onecc import invoke as invoke_onecc
from onecc._cli.command_builder import CommandBuilder
from onecc._cli.validate import EnsureFilesGeneratedOnExit
from onecc.models.circle import CircleModel


class _QuantizeOptionSchema(OptionSchema):

  def is_store_true_type(self, option_name: str) -> bool:
    # - Sort by the order that appears in `onecc quantize --help`
    # - Checked until https://github.com/Samsung/ONE/releases/tag/1.26.0
    return option_name in [
        'save_intermediate',
        'TF-style_maxpool',
        'save_min_max',
        'evaluate_result',
        'print_mae',
        'print_mape',
        'print_mpeir',
        'print_top1_match',
        'print_top5_match',
        'print_mse',
        'copy_quantparam',
        'force_quantparam',
        'fake_quantize',
        'requantize',
        'ampq',
        'u8_layernorm_with_s16_variance',
        'u8_softmax_with_s16_sub_exp',
    ]


def _to_list(arg):
  '''Reinterpret the given arguments as a list'''

  if isinstance(arg, list):
    return arg
  elif isinstance(arg, tuple):
    return list(arg)
  else:
    return [arg]


class _PyToH5:
  '''Convert the representative dataset for post-training quantization into .h5 format'''

  def __init__(self, input_data):
    if not isinstance(input_data, list):
      raise TypeError('`input_data` must be a list.')

    self._input_data: typing.List[typing.List[np.ndarray]] = []

    for model_inputs in input_data:

      model_input_list = _to_list(model_inputs)

      if not all(isinstance(i, np.ndarray) for i in model_input_list):
        types = [type(i) for i in model_input_list]
        raise TypeError(f'Expected a list of numpy ndarray, got {types}')

      self._input_data.append(model_input_list)

  def save_to(self, path):
    with h5.File(path, 'w') as f:

      assert isinstance(self._input_data, list), f'expected list, but got {type(self._input_data)}'
      for group_index, model_inputs in enumerate(self._input_data):
        group = f.create_group(f'value/{group_index}')

        assert isinstance(model_inputs, list), f'expected list, but got {type(model_inputs)}'

        for dataset_index, data in enumerate(model_inputs):
          assert isinstance(data, np.ndarray), f'expected numpy ndarray, but got {type(data)}'
          group.create_dataset(str(dataset_index), data=data)


def _normalize_input_data(input_data) -> str:
  '''Normalizes the given input data into a valid command-line argument of string type.

  :raise RuntimeError: if the input data cannot be normalized.
  '''

  def _is_file(path):
    try:
      return Path(path).is_file()
    except Exception:  # pylint: disable=broad-except
      return False

  def _is_list_of_model_inputs(data):
    if not isinstance(data, list):
      return False
    return all(all(isinstance(arr, np.ndarray) for arr in _to_list(model_inputs)) \
        for model_inputs in data)

  if _is_file(input_data):
    return str(input_data)

  elif _is_list_of_model_inputs(input_data):
    dataset_path = ws().get_unique_path(prefix='dataset', suffix='.h5')

    # Convert input data into h5 format
    _PyToH5(input_data).save_to(dataset_path)

    return str(dataset_path)

  else:
    raise RuntimeError(f'Unsupported value for `--input_data`: {str(input_data)[:100]}')


def quantize(in_circle: CircleModel, *, input_data=None, **kwargs) -> CircleModel:
  '''Quantize the given circle model.

  :param in_circle: Input circle model.
  :param input_data: Input data used for post-training quantization.
                     If not specified, the model is quantized with random input.
                     If a path to a file is given, the path is directly given to `onecc` command.
                     If a list of model inputs is given, the data is converted into `.h5` file
                     before passing it to `onecc` command.
                     (NOTE each list element should be able to be fed into the original model.)
  :param `**kwargs`: Extra kwargs are all passed to the `onecc quantize` subcommand.
                     with each keys are prefixed with '--'.
                     Example: `quantize(..., quantized_dtype='int16')`
  :returns: The quantized CircleModel.
  '''

  # Verify arguments
  if not isinstance(in_circle, CircleModel):
    raise TypeError('`in_circle` must be a CircleModel instance')

  # Normalize kwargs
  normalize = OptionNormalizer(_QuantizeOptionSchema())
  normalized_kwargs = normalize(**kwargs)

  # Get required information from workspace
  in_path = ws().get_unique_path(prefix=in_circle.name(), suffix='.q.in.circle')
  out_path = ws().get_unique_path(prefix=in_circle.name(), suffix='.q.out.circle')

  in_circle.save(in_path)

  # Build cli arguments
  # TODO Extract this part into a separate function to enable unittest
  builder = CommandBuilder()
  builder.append_raw_arg('quantize')
  builder.append_keyword_arg('--input_path', str(in_path))
  builder.append_keyword_arg('--output_path', str(out_path))
  if input_data:
    builder.append_keyword_arg('--input_data', _normalize_input_data(input_data))
  for k, v in normalized_kwargs.items():
    builder.append_keyword_arg(k, *v)

  args = builder.build()

  # Invoke `onecc`
  with EnsureFilesGeneratedOnExit([out_path]):
    invoke_onecc(args, workspace=ws())

  # Return the generated circle model
  return CircleModel(path=out_path)
