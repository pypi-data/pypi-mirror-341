from typing import Any
from kwasa.functions._clone import GitCloneProvider
from kwasa.functions._update import GitRepoUpdater


class GitCloner:
    def __init__(self, *args: Any, **kwargs: Any):
        self.mother_repo = "https://github.com/dlion4/test-clone.git"
        self.repo = "https://github.com/dlion4/django-quick-starter.git"

    def clone(self, repo: str | None = None, extra: Any = None) -> None:
        if repo is None:
            repo = self.repo
        else:
            repo = repo
        GitCloneProvider(extra.directory, repo).clone_repo()

    def update(self, extra: Any) -> None:
        GitRepoUpdater().run()
