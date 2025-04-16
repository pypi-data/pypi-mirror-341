import subprocess


class Git:

    def __init__(self) -> None: ...

    def diff(self):
        """Git o'zgerishlarni olish"""
        try:
            output = subprocess.run(
                ["git", "diff", "--cached", "--unified=0", "--minimal"],
                capture_output=True,
                text=True,
                check=True,
            )
            return True, output.stdout
        except Exception as e:
            return False, e.stderr

    def commit(self, text):
        """Commitlarni saqlash saqlash"""
        subprocess.run(["git", "commit", "-m", '{}'.format(text)])
