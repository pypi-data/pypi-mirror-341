from jst_aicommit.api import AI
from .git import Git
import questionary
from rich import print
from .exceptions import JstException


class JstAiCommit:

    def __init__(self) -> None: ...

    def run(self):
        """Ish tushurovchi funcsiya"""
        ai = AI()
        git = Git()
        status, changes = git.diff()
        if not status or len(changes.strip()) == 0:
            print("[red bold] No changes to commit.[/red bold]")
            exit()
        try:
            ai_text = ai.get_commit(changes)
        except JstException as e:
            if e.code == JstException.ERROR_MATCH:
                ai_text = e.message
            else:
                raise Exception("Nomalum xatolik yuz ber")
        commit = questionary.text("commit: ", default=ai_text).ask()
        if commit is not None:
            git.commit(commit)


def main():
    """Main funcsiya"""
    obj = JstAiCommit()
    obj.run()
