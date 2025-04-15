import os
import subprocess
import json
import shutil
from kwasa.libs.exceptions import (
    CleanupFailedError,
    CloneFailedError,
    RepositoryAlreadyExistsError,
)
from kwasa.libs.helper import HelperUtility
from kwasa.libs.permissions import on_rm_error
from kwasa.logger.log import get_logger

logger = get_logger("clone")


class GitCloneProvider(HelperUtility):
    def __init__(
        self,
        directory: str,
        repo_url: str = "https://github.com/dlion4/django-quick-starter.git",
    ):
        self.directory = directory
        self.repo_url = repo_url
        self.full_path = os.path.abspath(directory)
        self.git_dir = os.path.join(self.full_path, ".git")
        self.kwasa_meta_dir = os.path.join(self.full_path, ".git", ".kwasa")
        self.metadata_path = os.path.join(self.kwasa_meta_dir, "metadata.json")

    def clone_repo(self) -> None:
        if not os.path.exists(self.full_path):
            logger.info(f"📂 Creating directory '{self.directory}'...")
            os.makedirs(self.full_path)

        logger.info(f"📁 Cloning from '{self.repo_url}' into '{self.directory}'...")

        try:
            if os.path.exists(self.git_dir):
                raise RepositoryAlreadyExistsError(
                    f"{self.full_path} is already a git repository!"
                )
            else:
                subprocess.run(
                    ["git", "clone", self.repo_url, self.full_path], check=True
                )
                shutil.rmtree(self.git_dir, ignore_errors=True)
                subprocess.run(["git", "-C", self.full_path, "init"], check=True)
                try:
                    self.manage_local_repository(True)
                except Exception:
                    pass

                os.makedirs(self.kwasa_meta_dir, exist_ok=True)
                metadata = {"origin": self.repo_url}
                with open(self.metadata_path, "w") as f:
                    json.dump(metadata, f)
                logger.info("✅ Clone complete and git initialized.")
        except (
            subprocess.CalledProcessError,
            RepositoryAlreadyExistsError,
            CleanupFailedError,
            CloneFailedError,
        ) as e:
            logger.error(f"❌ Failed to clone repository. {e}")
            if os.path.exists(self.full_path):
                logger.warning("🧹 Cleaning up failed clone directory...")
                try:
                    shutil.rmtree(self.full_path, onexc=on_rm_error)
                except Exception as cleanup_error:
                    logger.error(f"⚠️ Cleanup failed: {cleanup_error}")
            raise e
