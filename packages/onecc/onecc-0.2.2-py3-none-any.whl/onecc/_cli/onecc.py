'''Helper to run cli `onecc` application'''

import shutil
import subprocess
from pathlib import Path

from onecc.errors import CommandError, CommandNotFoundError
from onecc._fs.workspace import _Workspace

URL_INSTALL_LATEST_DEBIAN_PACKAGE = 'https://pages.github.sec.samsung.net/AIP/ONE_User_Guide' \
                                    '/latest/html/getting_started/setup_linux.html' \
                                    '#install-triv-toolchain-for-latest-package'
URL_REPORT_ONECC_ISSUE = 'https://github.com/Samsung/ONE/issues'


class GenerateIssueReportGuideOnError:
  '''Generate issue report format when an error occurs while running the onecc command line app.'''

  def __init__(self, *, workspace: _Workspace):
    if not isinstance(workspace, _Workspace):
      raise TypeError('`workspace` must be a `onecc._fs.workspace._Workspace` instance')

    self._workspace = workspace

  def __enter__(self):
    pass

  def __exit__(self, exn_type, exn_val, *args):
    if exn_type is not subprocess.CalledProcessError:
      return

    assert isinstance(exn_val.cmd, list)  # FIX Python UNLESS
    assert Path(exn_val.cmd[0]).name == 'onecc', 'This class is only for `onecc` cli app.'

    # CalledProcessError has been raised
    self._workspace.dont_delete()

    cmd_str = ' '.join(exn_val.cmd)

    msg = f'Error while running command:\n\n  $ {cmd_str}\n'
    msg += '\n'
    msg += '[EXIT CODE]\n'
    msg += f'{exn_val.returncode}\n'
    msg += '[STDOUT]\n'
    msg += exn_val.stdout.decode()
    msg += '[STDERR]\n'
    msg += exn_val.stderr.decode()
    msg += '\n'
    msg += 'Try re-running the command from the command line.\n'
    msg += '\n'
    msg += 'If you see the same error message from the command line,\n'
    msg += f'You are ready report an issue to: {URL_REPORT_ONECC_ISSUE}.\n'
    msg += '\n'
    msg += 'When reporting an issue, please make sure you attach the below information.\n'
    msg += '  1. Installed one-compiler version (can be found with `dpkg-query -s one-compiler`)\n'
    msg += '  2. Full command and the necessary files to reproduce the error\n'
    msg += f'     (The required files are under "{str(self._workspace.path())}")'
    msg += '\n'

    raise CommandError(msg) from exn_val


def invoke(args, *, workspace):
  '''Invoke the cli application `onecc` with the given arguments

  :param workspace: A workspace that contains all required files to run the command.

  :raise CommandNotFoundError: if `onecc` command cannot be found
  :raise CommandError: if `onecc` command exits with non-zero exit code.
  '''
  if not isinstance(args, list):
    raise TypeError('`args` must be a list')
  if not all(isinstance(a, str) for a in args):
    raise TypeError('`args` must be a list of string')

  onecc = shutil.which('onecc')

  if onecc is None:
    msg = 'Cannot find `onecc` on your `PATH`.\n'
    msg += '\n'
    msg += 'Please install the `triv2-toolchain-latest` debian package following the below guide.\n'
    msg += f'{URL_INSTALL_LATEST_DEBIAN_PACKAGE}\n'
    msg += '\n'
    msg += 'After the successful installation, '
    msg += 'you should be able to run `$ onecc` on your command line.\n'
    raise CommandNotFoundError(msg)

  cmd = [onecc] + args

  with GenerateIssueReportGuideOnError(workspace=workspace):
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
