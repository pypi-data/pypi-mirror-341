'''Workspace registry

Decide where to save the temporary files.
'''
from typing import Dict, Any
from onecc._fs.workspace import TemporaryWorkspace, PermanentWorkspace
from contextlib import ContextDecorator
from pathlib import Path


class _Singleton(type):
  _instances: Dict[type, Any] = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super().__call__(*args, **kwargs)
    return cls._instances[cls]


class _WorkspaceStack(metaclass=_Singleton):
  """Workspace stack"""

  def __init__(self):
    self.default_workspace = TemporaryWorkspace()
    self.stack = [self.default_workspace]

  def push(self, ws):
    self.stack.append(ws)

  def pop(self):
    assert not self.empty(), "_WorkspaceStack must not be empty"
    self.stack.pop()

  def top(self):
    assert not self.empty(), "_WorkspaceStack must not be empty"
    return self.stack[len(self.stack) - 1]

  def empty(self):
    return len(self.stack) == 0

  def __new__(cls):
    return super(_WorkspaceStack, cls).__new__(cls)


def get_workspace():
  """
  By default, return `TemporaryWorkspace`
  - Used by default if the "scoped workspace" does not exist.
  - Use temporary workspace to enable automatic deletion of temporary files.

  Inside ScopedWorkspaceContext, return `PermanentWorkspace`
  - Nesting is allowed.
  - Use permanent workspace with the user-provided path.

  Returns:
    TemporaryWorkspace|PermanentWorkspace
  """
  return _WorkspaceStack().top()


class ScopedWorkspaceContext(ContextDecorator):
  '''scoped workspace context.

  Inside this context, calling get_workspace() will return :class:`PermanentWorkspace`
  '''

  def __init__(self, path):
    self._path: Path = Path(path)

  def __enter__(self):
    _WorkspaceStack().push(PermanentWorkspace(self._path))

  def __exit__(self, *args):
    assert isinstance(_WorkspaceStack().top(), PermanentWorkspace)
    assert _WorkspaceStack().top().path() == self._path
    _WorkspaceStack().pop()
