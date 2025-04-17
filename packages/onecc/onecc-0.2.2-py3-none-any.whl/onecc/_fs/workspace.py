'''Workspace managemenet to save temporary data'''

import tempfile

from pathlib import Path
import typing


class _Workspace:
  '''Wrapper of a directory to save temporary data generated from onecc.'''

  def __init__(self, path: Path):
    path = Path(path)
    assert path.is_dir()

    self._path: Path = path
    self._path_registry: typing.Dict[typing.Tuple[str, str], int] = {}

  def path(self) -> Path:
    return self._path

  def get_unique_path(self, *, prefix='model', suffix):
    if (prefix, suffix) not in self._path_registry:
      self._path_registry[(prefix, suffix)] = 0

    idx = self._path_registry[(prefix, suffix)]
    unique_path = self._path / f'{prefix}.{idx}{suffix}'
    self._path_registry[(prefix, suffix)] += 1
    return unique_path

  def can_delete(self):
    raise NotImplementedError  # Child class must override this

  def dont_delete(self):
    raise NotImplementedError  # Child class must override this


class TemporaryWorkspace(_Workspace):
  '''Global default workspace'''

  def __init__(self):
    temp_dir = tempfile.mkdtemp(prefix='onecc_')
    super().__init__(Path(temp_dir))

    self._can_delete = True

  def __del__(self):
    if hasattr(self, '_can_delete') and self._can_delete:
      if not any(self.path().iterdir()):
        self.path().rmdir()

  def can_delete(self):
    return self._can_delete

  def dont_delete(self):
    self._can_delete = False


class PermanentWorkspace(_Workspace):
  '''Permanent workspace with the given path path'''

  def __init__(self, path: Path):
    path = Path(path)
    assert not path.is_file()
    path.mkdir(parents=True, exist_ok=True)
    super().__init__(path)

  def can_delete(self):
    return False

  def dont_delete(self):
    pass
