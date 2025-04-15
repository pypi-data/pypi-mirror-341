# Define custom exceptions
class GitClonerError(Exception):
    """Base class for all exceptions in GitCloner."""

    pass


class RepositoryAlreadyExistsError(GitClonerError):
    """Raised when the repository already exists in the target directory."""

    pass


class CloneFailedError(GitClonerError):
    """Raised when the cloning operation fails."""

    pass


class CleanupFailedError(GitClonerError):
    """Raised when cleaning up a failed clone fails."""

    pass
