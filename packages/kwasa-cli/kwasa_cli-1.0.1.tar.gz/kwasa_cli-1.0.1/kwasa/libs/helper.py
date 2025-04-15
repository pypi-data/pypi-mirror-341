import os
import subprocess
import platform
from contextlib import suppress
from typing import Any

from kwasa.logger.log import get_logger

logger = get_logger("utility")


class HelperUtility:
    def __init__(self, full_path: Any) -> None:
        self.full_path = full_path

    def manage_local_repository(self, installation: bool = True) -> None:
        os.chdir(self.full_path)

        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "checkout", "-b", "main"], check=True)
        subprocess.run(["git", "add", "--all"], check=True)
        subprocess.run(
            ["git", "commit", "-m", "Reinitialized the git repository after update."],
            check=True,
        )

        if installation:
            self.manage_virtualenv_and_install()

    def manage_virtualenv_and_install(self) -> None:
        """Set up virtual environment and install both Python and Node dependencies"""

        if not os.path.exists(".venv"):
            logger.info("🛠️ .venv not found. Creating virtual environment...")
            subprocess.run(["python", "-m", "venv", ".venv"], check=True)
            logger.info("✔️ .venv created successfully.")

        self.install_python_dependencies()
        self.install_node_dependencies()

    def install_python_dependencies(self) -> None:
        """Install Python dependencies from requirements.txt if it exists"""
        if not os.path.exists("requirements.txt"):
            logger.info(
                "ℹ️ No requirements.txt found. Skipping Python package installation."
            )
            return

        platform_name = platform.system()
        pip_cmd = (
            ".venv\\Scripts\\pip" if platform_name == "Windows" else ".venv/bin/pip"
        )
        logger.info(f"📦 Installing Python packages using {pip_cmd}...")

        with suppress(subprocess.CalledProcessError):
            subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
            logger.info("✔️ Python packages installed successfully.")
            return

        logger.warning("⚠️ Python package installation failed.")

    def install_node_dependencies(self) -> None:
        """Install Node.js dependencies using npm or pnpm"""
        if not os.path.exists("package.json"):
            logger.warning("📦 No package.json found. Skipping Node.js setup.")
            return

        if self.check_package_manager("npm"):
            logger.info("📦 Installing Node.js packages using npm...")
            with suppress(subprocess.CalledProcessError):
                subprocess.run(["npm", "install"], check=True)
                logger.info("✔️ Node.js packages installed successfully via npm.")
                return
            logger.warning("⚠️ Node.js package installation failed using npm.")

        elif self.check_package_manager("pnpm"):
            logger.info("📦 Installing Node.js packages using pnpm...")
            with suppress(subprocess.CalledProcessError):
                subprocess.run(["pnpm", "install"], check=True)
                logger.info("✔️ Node.js packages installed successfully via pnpm.")
                return
            logger.warning("⚠️ Node.js package installation failed using pnpm.")

        else:
            logger.warning("⚠️ No supported package manager found (npm or pnpm).")

    def check_package_manager(self, manager: Any) -> bool:
        """Check if a package manager like npm or pnpm is installed"""
        with suppress(subprocess.CalledProcessError):
            subprocess.run(
                [manager, "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logger.info(f"✔️ Found package manager: {manager}")
            return True

        logger.warning(f"⚠️ {manager} not found.")
        return False
