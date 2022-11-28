from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class RuffError:
    location: str
    code: str
    message: str

    @property
    def file(self) -> str:
        return self.location.split(":")[0]

    @property
    def line_number(self) -> int:
        return int(self.location.split(":")[1])

    @classmethod
    def from_message_error(cls, message_error: str) -> RuffError:
        return RuffError(*message_error.split(" ", maxsplit=2))


def run_cli(*command_args) -> str:
    process = subprocess.Popen(command_args, stdout=subprocess.PIPE)
    stdout, _ = process.communicate()
    output = stdout.decode()
    print(f""">>> {' '.join(command_args)}""")
    logger.debug(output)
    return output


def ruff(*files: str):
    if not files:
        files = tuple(str(x) for x in Path(".").iterdir() if x.is_dir())

    print(f"{files=}")
    output = run_cli("ruff", *files)
    return [
        RuffError.from_message_error(error)
        for error in output.splitlines()
        if error.startswith(files)
    ]
