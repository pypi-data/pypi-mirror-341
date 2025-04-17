'''Helper to run cli `onecc` application'''

import time
import typing
from pathlib import Path


class EnsureFilesGeneratedOnExit:
  '''Ensure new files are generated if there's no exception raised in the scope.'''

  def __init__(self, paths: typing.List[typing.Union[str, Path]]):
    if not isinstance(paths, list):
      raise TypeError('`paths` must be a list of str or pathlib.Path instances.')
    paths = [Path(p) for p in paths]

    self._paths = paths
    self._timestamp = None

  def __enter__(self):
    assert self._timestamp is None
    self._timestamp = time.time()

  def __exit__(self, exc_type, *args):
    if exc_type:
      return

    # No exception has been raised
    for path in self._paths:
      if not path.is_file():
        raise RuntimeError(f'{path} is not created.')
      # TODO Use higher resolution when timestamp comparison, without `int()` casting
      if int(path.stat().st_mtime) < int(self._timestamp):
        raise RuntimeError(f'{path} is not created ({path.stat().st_mtime} < {self._timestamp}).')
