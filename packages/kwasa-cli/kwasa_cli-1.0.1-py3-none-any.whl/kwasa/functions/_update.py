import json
import os
import shutil
import subprocess
import sys
from contextlib import suppress
from typing import Any

from kwasa.libs.helper import HelperUtility
from kwasa.logger.log import get_logger

logger = get_logger("update")


class GitRepoUpdater(HelperUtility):
    """
    Handles safe update of a cloned project using metadata from the template repo.
    """

    def __init__(self) -> None:
        self.project_path = os.getcwd()
        self.kwasa_meta = os.path.join(self.project_path, ".git", ".kwasa")
        self.metadata_path = os.path.join(self.kwasa_meta, "metadata.json")
        self.template_repo = None
        self.user_remote = None

    def run(self) -> None:
        self._validate_git_repo()
        self._load_template_metadata()
        self._stage_untracked_files()
        self._swap_origin_and_add_template()
        self._fetch_and_merge_template()
        self._cleanup_and_re_init_git()
        self._restore_template_metadata()
        self._install_dependencies()

    def _validate_git_repo(self) -> None:
        if not os.path.exists(".git"):
            logger.error("❌ Not a git repo. Run this inside a cloned directory.")
            sys.exit(1)

        if not os.path.exists(self.metadata_path):
            logger.error("❌ No metadata found. Use `kwasa clone` to initialize.")
            sys.exit(1)

    def _load_template_metadata(self) -> None:
        with open(self.metadata_path) as f:
            meta = json.load(f)

        self.template_repo = meta.get("origin")
        if not self.template_repo:
            logger.error("❌ No 'origin' found in metadata.json.")
            sys.exit(1)

        logger.info("🔄 Starting safe update...")

    def _get_git_remote(self, name: str = "origin") -> str | None:
        try:
            result = subprocess.run(
                ["git", "-C", self.project_path, "remote", "get-url", name],
                capture_output=True,
                text=True,
                check=True,
            )
            print(result.stdout.strip())
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def _save_metadata(self, filename: str, data: Any) -> None:
        os.makedirs(self.kwasa_meta, exist_ok=True)
        with open(os.path.join(self.kwasa_meta, filename), "w") as f:
            json.dump(data, f)

    def _stage_untracked_files(self) -> None:
        try:
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                capture_output=True,
                text=True,
                check=True,
            )
            untracked_files = result.stdout.splitlines()

            if untracked_files:
                logger.warning(f"⚠️ Untracked files: {untracked_files}")
                subprocess.run(["git", "add"] + untracked_files, check=True)
                subprocess.run(
                    ["git", "commit", "-m", "updating untracked files"], check=True
                )
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ Could not stage untracked files: {e}")

    def _swap_origin_and_add_template(self) -> None:
        try:
            if self.user_remote:
                subprocess.run(
                    ["git", "remote", "rename", "origin", "user"], check=True
                )

            result = subprocess.run(
                ["git", "remote", "get-url", "template"], capture_output=True, text=True
            )
            if result.returncode == 0:
                subprocess.run(["git", "remote", "remove", "template"], check=True)
                logger.info("🧹 Removed existing 'template' remote.")

            subprocess.run(
                ["git", "remote", "add", "template", self.template_repo], check=True
            )
            subprocess.run(["git", "fetch", "template"], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Remote setup failed. {e}")
            sys.exit(1)

    def _fetch_and_merge_template(self) -> None:
        try:
            # Stash local changes before merge
            subprocess.run(["git", "stash", "--include-untracked"], check=True)

            # Merge from template remote
            subprocess.run(
                [
                    "git",
                    "merge",
                    "template/main",
                    "--allow-unrelated-histories",
                    "--no-edit",
                    "--strategy-option=theirs",
                ],
                check=True,
            )

            # Pop stashed changes
            stash_list = subprocess.run(
                ["git", "stash", "list"], capture_output=True, text=True
            )
            if stash_list.stdout.strip():
                try:
                    subprocess.run(["git", "stash", "pop"], check=True)
                    logger.info(
                        "✅ Merged updates and restored local changes from stash."
                    )
                except subprocess.CalledProcessError:
                    logger.warning(
                        "⚠️ Stash pop failed. You may need to resolve conflicts manually."
                    )
                    logger.warning(
                        "   Run: `git stash list` then `git stash apply` to retry."
                    )
            else:
                logger.info("✅ Merged updates; no stash to pop.")

        except subprocess.CalledProcessError as e:
            if e.stderr and "unmerged files" in e.stderr:
                logger.error("❌ Merge conflicts detected. Resolve manually.")
                with suppress(Exception):
                    subprocess.run(["git", "merge", "--abort"], check=True)
            else:
                logger.error(f"❌ Merge failed. {e}")
            sys.exit(1)

    def _cleanup_and_re_init_git(self) -> None:
        try:
            subprocess.run(["git", "remote", "remove", "template"], check=True)
        except subprocess.CalledProcessError:
            logger.warning("⚠️ Failed to remove template remote.")

        with suppress(Exception):
            shutil.rmtree(".git", ignore_errors=True)
            logger.info("🧹 Removed .git directory.")

        with suppress(Exception):
            self.manage_local_repository(True)

    def _restore_template_metadata(self) -> None:
        try:
            self._save_metadata("metadata.json", {"origin": self.template_repo})
            logger.info(f"🔁 Restored and saved remote: {self.user_remote}")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to restore original remote. {e}")

    def _install_dependencies(self) -> None:
        self.install_node_dependencies()
        self.install_python_dependencies()
