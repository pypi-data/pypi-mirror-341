import shutil
import subprocess
import tempfile
from pathlib import Path
from cookiecutter.main import cookiecutter
from importlib_resources import files

from greening.greening_config import GreeningConfig
from greening.helpers import run_git

def deploy_site():
    """
    Public entrypoint: Renders the site-template via Cookiecutter
    and deploys it to the gh-pages branch of the current repo.
    """
    config = GreeningConfig()
    _render_site_template(config)

def help_deploy():
    print("""Usage: greening deploy [OPTIONS]

Deploy a documentation site using GitHub Pages.

This command generates and deploys a Jekyll site (using the Minimal Mistakes theme) based on your project metadata in greening.yaml.

It can also:
- Automatically push the site to the `gh-pages` branch of your GitHub repository
- Auto-configure Google Analytics if a tracking ID is defined in greening.yaml

Options:
  --help             Show this help message and exit

Examples:
  greening deploy
""")


def _render_site_template(config: GreeningConfig):
    """
    Renders the site template using Cookiecutter and deploys it.
    """
    template_path = files("greening") / "templates" / "site-template"

    with tempfile.TemporaryDirectory() as tmpdir:
        cookiecutter(
            str(template_path),
            no_input=True,
            extra_context=config.to_cookiecutter_context(),
            output_dir=tmpdir,
            overwrite_if_exists=True
        )

        rendered_path = Path(tmpdir) / config.data["project_slug"]
        _deploy_rendered_site(rendered_path, config)

def _deploy_rendered_site(rendered_path: Path, config: GreeningConfig):
    """
    Checks out or creates the gh-pages branch, clears the working tree,
    replaces it with the rendered site, commits and optionally pushes.
    """
    repo_root = config.path.parent
    should_push = config.data.get("push", False)

    try:
        run_git("git rev-parse --verify gh-pages", cwd=repo_root)
        run_git("git checkout gh-pages", cwd=repo_root)
    except subprocess.CalledProcessError:
        run_git("git checkout --orphan gh-pages", cwd=repo_root)

    run_git("git rm -rf .", cwd=repo_root)

    for item in rendered_path.iterdir():
        shutil.move(str(item), str(repo_root / item.name))

    run_git("git add .gitignore", cwd=repo_root)
    run_git("git add .", cwd=repo_root)
    run_git("git commit -m 'Deploy Jekyll site'", cwd=repo_root)

    if should_push:
        print("🚀 Pushing gh-pages to origin...")
        run_git("git push -f origin gh-pages", cwd=repo_root)
    else:
        print("⚠️  Push skipped (set push: true in greening.yaml to enable)")

    run_git("git checkout main", cwd=repo_root)
