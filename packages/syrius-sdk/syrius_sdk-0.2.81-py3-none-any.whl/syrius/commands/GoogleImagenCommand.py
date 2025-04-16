from typing import Literal

from syrius.commands.LoopInputCommand import loopType
from syrius.commands.abstract import AbstractCommand, Command


class GoogleImagenCommand(Command):
    id: int = 97
    prompt: str | AbstractCommand | loopType
    model: str | AbstractCommand | loopType = "imagen-3.0-generate-002"
    num_images: int | AbstractCommand | loopType = 1
    mimetype: str | AbstractCommand | loopType = 'image/png'

