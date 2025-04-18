from .base import TerminalStateHandler
from .no_terminal import NoTerminalStateHandler
from .height import HeightBasedTerminalStateHandler
from .traj import RootPoseTrajTerminalStateHandler

# register all terminal state handlers
NoTerminalStateHandler.register()
HeightBasedTerminalStateHandler.register()
RootPoseTrajTerminalStateHandler.register()
