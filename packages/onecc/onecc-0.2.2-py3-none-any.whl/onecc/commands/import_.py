'''Wrapper of `onecc import` command'''

from pathlib import Path
import typing

from onecc._fs.workspace_registry import get_workspace as ws
from onecc._cli.onecc import invoke as invoke_onecc
from onecc._cli.adapter import OptionNormalizer
from onecc._cli.adapter import OptionSchema
from onecc._cli.command_builder import CommandBuilder
from onecc._cli.validate import EnsureFilesGeneratedOnExit
from onecc.models.circle import CircleModel


class _ImportOnnxOptionSchema(OptionSchema):
  '''CLI argument adapter for one-import-onnx'''

  def is_store_true_type(self, option_name: str) -> bool:
    return option_name in [
        'verbose',
        'unroll_rnn',
        'unroll_lstm',
        'keep_io_order',
        'save_intermediate',
        'experimental_disable_batchmatmul_unfold',
    ]


def import_onnx(in_path: typing.Union[str, Path], **kwargs) -> CircleModel:
  '''Import the given onnx model.

  :param in_path: Path of input onnx model file
  :param `**kwargs`: Extra kwargs are all passed to the `onecc import onnx` subcommand,
                     with each keys are prefixed with '--'.
                     Example: `import_onnx(..., unroll_lstm=True)`
  :returns: The optimized CircleModel.
  '''

  # Verify arguments
  in_path = Path(in_path)

  # Normalize kwargs
  normalize = OptionNormalizer(_ImportOnnxOptionSchema())
  normalized_kwargs = normalize(**kwargs)

  # Get required information from workspace
  out_path = ws().get_unique_path(prefix=in_path.stem, suffix='.import.circle')

  # Build cli arguments
  builder = CommandBuilder()
  builder.append_raw_arg('import')
  builder.append_raw_arg('onnx')
  builder.append_keyword_arg('--input_path', str(in_path))
  builder.append_keyword_arg('--output_path', str(out_path))
  for k, v in normalized_kwargs.items():
    builder.append_keyword_arg(k, *v)
  args = builder.build()

  # Invoke `onecc`
  with EnsureFilesGeneratedOnExit([out_path]):
    invoke_onecc(args, workspace=ws())

  # Return the generated circle model
  return CircleModel(path=out_path)


class _ImportTFLiteOptionSchema(OptionSchema):
  '''CLI argument adapter for one-import-tflite'''

  def is_store_true_type(self, option_name: str) -> bool:
    return option_name in [
        'verbose',
    ]


def import_tflite(in_path: typing.Union[str, Path], **kwargs) -> CircleModel:
  '''Import the given tflite model.

  :param in_path: Path of input tflite model file
  :param `**kwargs`: Extra kwargs are all passed to the `onecc import tflite` subcommand,
                     with each keys are prefixed with '--'.
  :returns: The optimized CircleModel.
  '''

  # Verify arguments
  in_path = Path(in_path)

  # Get required information from workspace
  out_path = ws().get_unique_path(prefix=in_path.stem, suffix='.import.circle')

  # Normalize kwargs
  normalize = OptionNormalizer(_ImportTFLiteOptionSchema())
  normalized_kwargs = normalize(**kwargs)

  # Build cli arguments
  builder = CommandBuilder()
  builder.append_raw_arg('import')
  builder.append_raw_arg('tflite')
  builder.append_keyword_arg('--input_path', str(in_path))
  builder.append_keyword_arg('--output_path', str(out_path))
  for k, v in normalized_kwargs.items():
    builder.append_keyword_arg(k, *v)

  args = builder.build()

  # Invoke `onecc`
  with EnsureFilesGeneratedOnExit([out_path]):
    invoke_onecc(args, workspace=ws())

  # Return the generated circle model
  return CircleModel(path=out_path)
