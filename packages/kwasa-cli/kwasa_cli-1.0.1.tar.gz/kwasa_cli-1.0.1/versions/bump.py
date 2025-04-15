import toml
from packaging.version import Version


def bump_patch_version(version_str):
    v = Version(version_str)
    return f"{v.major}.{v.minor}.{v.micro + 1}"


def bump_version(file_path="pyproject.toml"):
    with open(file_path, "r") as f:
        data = toml.load(f)

    current_version = data["project"]["version"]
    new_version = bump_patch_version(current_version)
    data["project"]["version"] = new_version

    with open(file_path, "w") as f:
        toml.dump(data, f)

    print(f"Version bumped from {current_version} → {new_version}")


if __name__ == "__main__":
    bump_version()
