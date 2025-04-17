'''Wrapper of `onecc optimize` command'''

from onecc._fs.workspace_registry import get_workspace as ws
from onecc._cli.onecc import invoke as invoke_onecc
from onecc._cli.command_builder import CommandBuilder
from onecc._cli.validate import EnsureFilesGeneratedOnExit
from onecc.models.circle import CircleModel

import configparser


def optimize(in_circle: CircleModel, *, O1=False, **kwargs) -> CircleModel:
  '''Optimize the given circle model.

  :param in_circle: Input circle model.
  :param O1: If True, basic optimization options will be applied.
             See here for details: https://pages.github.sec.samsung.net/AIP/ONE_User_Guide/
                                   latest/html/command_line_interface/group_option.html
  :param `**kwargs`: Extra kwargs are all passed to the `onecc optimize` subcommand,
                     with each keys are prefixed with '--'.
                     Example: `optimize(..., fuse_batchnorm_with_conv=True)`
  :returns: The optimized CircleModel.
  '''

  # Verify arguments
  if not isinstance(in_circle, CircleModel):
    raise TypeError('`in_circle` must be a CircleModel instance')

  # Get required information from workspace
  cfg_path = ws().get_unique_path(prefix=in_circle.name(), suffix='.opt.cfg')
  in_path = ws().get_unique_path(prefix=in_circle.name(), suffix='.opt.in.circle')
  out_path = ws().get_unique_path(prefix=in_circle.name(), suffix='.opt.out.circle')

  in_circle.save(in_path)

  # Write .cfg file
  config = configparser.ConfigParser()
  config['onecc'] = {}
  config['one-optimize'] = {}
  config['one-optimize']['input_path'] = str(in_path)
  config['one-optimize']['output_path'] = str(out_path)
  for k, v in kwargs.items():
    config['one-optimize'][k] = str(v)
  with open(cfg_path, 'w', encoding='utf-8') as f:
    config.write(f)

  # Build cli arguments
  builder = CommandBuilder()
  builder.append_raw_arg('optimize')
  if O1:
    builder.append_raw_arg('-O1')
  builder.append_raw_arg('-C')
  builder.append_raw_arg(str(cfg_path))
  args = builder.build()

  # Invoke `onecc`
  with EnsureFilesGeneratedOnExit([out_path]):
    invoke_onecc(args, workspace=ws())

  # Return the generated circle model
  return CircleModel(path=out_path)
