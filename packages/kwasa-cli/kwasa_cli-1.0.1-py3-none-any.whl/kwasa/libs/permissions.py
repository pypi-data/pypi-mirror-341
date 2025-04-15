import stat
import os
from typing import Any
from kwasa.libs.exceptions import CleanupFailedError
from kwasa.logger.log import get_logger

logger = get_logger("Permissions")


def on_rm_error(func: Any, path: Any, exc_info: Any) -> None:
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        logger.error(f"⚠️ Forced removal failed for {path}: {e}")
        raise CleanupFailedError(f"Failed to forcefully clean up {path}: {e}")
