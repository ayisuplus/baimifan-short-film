"""Repair only the CLI launcher, preserving installed packages and a rollback copy."""
from pathlib import Path
import shutil
import sys
from pip._vendor.distlib.scripts import ScriptMaker

ROOT = Path(__file__).resolve().parent
RUNTIME = Path('C:/Users/36322/.codex/runtimes/comfy-mcp')
BASE = Path('E:/Python/python.exe')
assert Path(sys.executable).resolve() == BASE.resolve()
launcher = RUNTIME / 'Scripts/comfy.exe'
backup = ROOT / 'comfy.exe.before'
if not backup.exists():
    shutil.copy2(launcher, backup)

class LocalLauncher(ScriptMaker):
    def _get_script_text(self, entry):
        return ('import sys\n'
                f'sys.path.insert(0, {str(RUNTIME / "Lib/site-packages")!r})\n'
                'import os\n'
                'from pathlib import Path\n'
                f'local_state = Path({str(RUNTIME / "local-state")!r})\n'
                'os.environ.setdefault("COMFY_CACHE_DIR", str(local_state / "cache"))\n'
                'from comfy_cli import jobs_state\n'
                'def local_job_state_dir():\n'
                '    path = local_state / "jobs"\n'
                '    path.mkdir(parents=True, exist_ok=True)\n'
                '    return path\n'
                'jobs_state.state_dir = local_job_state_dir\n'
                'from comfy_cli.__main__ import main\n'
                'if __name__ == "__main__":\n'
                '    sys.exit(main())\n')

staging = ROOT / 'launcher-candidate'
staging.mkdir(exist_ok=True)
maker = LocalLauncher(None, str(staging))
maker.executable = str(RUNTIME / 'Scripts/python.exe')
maker.variants = {''}
maker.clobber = True
maker.make('comfy = comfy_cli.__main__:main')
state = RUNTIME / 'local-state'
for source, target in [(Path.home() / '.cache/comfy-cli', state / 'cache'),
                       (Path.home() / 'AppData/Local/comfy-cli/jobs', state / 'jobs')]:
    target.mkdir(parents=True, exist_ok=True)
    for existing in source.glob('*.json'):
        if not (target / existing.name).exists():
            shutil.copy2(existing, target / existing.name)
shutil.copy2(staging / 'comfy.exe', launcher)
print('Replaced CLI entrypoint only; rollback:', backup)
