__maintainer__ = "Niklas Wulff, Fabia Miorelli"
__license__ = "BSD-3-Clause"

import os
import yaml
import shutil
import pathlib
import click
import vencopy


@click.command()
@click.option(
    "--name",
    default="vencopy_user",
    prompt="Please type the user folder name:",
    help="The folder name of the venco.py user folder created at command line working directory",
)
@click.option(
    "--tutorials",
    default="false",
    help="Specify if tutorials should be copied to the user folder on set up." "Defaults to true",
)
def create(name: str, tutorials: bool):
    """
    Folder set up after installation.

    Args:
        name (str): _description_
        tutorials (bool): _description_
    """
    cwd = pathlib.Path(os.getcwd())
    target = cwd / name
    source = pathlib.Path(vencopy.__file__).parent.resolve()
    if not os.path.exists(target):
        os.mkdir(target)
        setup_folders(src=source, trg=target)
        click.echo(f"venco.py user folder created under {target}")
    elif os.path.exists(target) and not os.path.exists(target / "run.py"):
        setup_folders(src=source, trg=target)
        click.echo(f"venco.py user folder filled under {target}")
    else:
        click.echo(
            "File run.py already exists in specified folder, for a new setup please specify a non-existent "
            "folder name"
        )


def setup_folders(src: pathlib.Path, trg: pathlib.Path):
    """
    Setup function to create a vencopy user folder and to copy run, config and tutorial files from the package source.

    Args:
        src (pathlib.Path): Absolute path to the vencopy package source folder
        trg (pathlib.Path): Absolute path to the vencopy user folder
        tutorials (bool): Boolean, if true (default) tutorials are being copied from package source to user folder
    """
    os.mkdir(trg / "input")
    os.mkdir(trg / "output")
    os.mkdir(trg / "output" / "dataparser")
    os.mkdir(trg / "output" / "diarybuilder")
    os.mkdir(trg / "output" / "gridmodeller")
    os.mkdir(trg / "output" / "flexestimator")
    os.mkdir(trg / "output" / "profileaggregator")
    os.mkdir(trg / "output" / "postprocessor")
    shutil.copy(src=src / "__run.py", dst=trg / "run.py")
    shutil.copytree(src=src / "config", dst=trg / "config", dirs_exist_ok=True)
    # if tutorials:
    #     shutil.copytree(src=src / "tutorials", dst=trg / "tutorials")
    update_config(new_vencopy_root=trg, src=src)
    update_runfile(new_vencopy_root=trg)


def update_config(src, new_vencopy_root: pathlib.Path):
    """
    Update user_config file so that it works with a user installation.

    Args:
        new_vencopy_root (pathlib.Path): path to vencopy user folder
    """
    shutil.copy(
         src=src / "config" / "user_config.yaml.default",
         dst=new_vencopy_root / "config" / "user_config.yaml",
     )
    with open(new_vencopy_root / "config" / "user_config.yaml") as f:
        user_cfg = yaml.load(f, Loader=yaml.SafeLoader)

    user_cfg["global"]["absolute_path"]["vencopy_root"] = new_vencopy_root.__str__()

    with open(new_vencopy_root / "config" / "user_config.yaml", "w") as f:
        yaml.dump(user_cfg, f, allow_unicode=True)
    print("Now you can navigate into the folder you just created and open the user_config.yaml file to adjust the paths to point to your dataset.")


def update_runfile(new_vencopy_root):
    """
    Update run.py file so that it works with a user installation.

    Args:
        new_vencopy_root (pathlib.Path): path to vencopy user folder
    """
    # Read the file and modify its content
    with open(new_vencopy_root / "run.py", "r") as file:
        lines = file.readlines()

    # Modify the specific line
    with open(new_vencopy_root / "run.py", "w") as file:
        for line in lines:
            if 'base_path = Path(__file__).parent / "vencopy"' in line:
                line = "    base_path = Path(__file__).parent\n"
            file.write(line)


if __name__ == "__main__":
    create()
