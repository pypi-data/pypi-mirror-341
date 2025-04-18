from setuptools import setup, find_packages
from setuptools.command.install import install
import shutil
import zipfile
from pathlib import Path

python_main_version = 3

python_minor_version = 8
package_minor_version = 1
python_version = f"{python_main_version}.{python_minor_version}"
package_version = f"{python_version}.{package_minor_version}"
src_dir = "src" + python_version


class CustomInstall(install):
    def run(self):
        install.run(self)
        self._deploy_files()

    @staticmethod
    def _extract_subdir(zip_path, target_subdir, output_dir):
        target_subdir = target_subdir.rstrip("/") + "/"
        output_dir = Path(output_dir)

        with zipfile.ZipFile(zip_path) as zip_file:
            for member in zip_file.namelist():
                if not member.startswith(target_subdir):
                    continue

                relative_path = member[len(target_subdir) :]
                if not relative_path:
                    continue

                dest_path = output_dir / relative_path

                if member.endswith("/"):
                    dest_path.mkdir(parents=True, exist_ok=True)
                else:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    with zip_file.open(member) as source, open(
                        dest_path, "wb"
                    ) as target:
                        shutil.copyfileobj(source, target)

    def _deploy_files(self):
        data_zip = Path(__file__).parent / src_dir / "winpython_embed" / "data.zip"
        py_tag = f"cp{python_main_version}{python_minor_version}"

        if hasattr(self, "install_lib") and self.install_lib:
            dest_dir = Path(self.install_lib).resolve()
        else:
            raise ValueError("install_lib is not set")

        print(f"Extracting {py_tag} from {data_zip} to {dest_dir}")
        self._extract_subdir(data_zip, py_tag, dest_dir)
        print("Python files deployment completed!")

        try:
            installed_zip = dest_dir / "winpython_embed" / "data.zip"
            if installed_zip.exists():
                installed_zip.unlink()
                print(f"Removed {installed_zip}")
        except Exception as e:
            print(f"Warning: Could not remove zip file: {e}")


setup(
    name="winpython-embed",
    version=package_version,
    description="Get WinPython from pip",
    author="Tanix",
    author_email="tanixlu@foxmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where=src_dir),
    package_dir={"": src_dir},
    package_data={
        "winpython_embed": [
            "data.zip",
        ],
    },
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development",
    ],
    cmdclass={
        "install": CustomInstall,
    },
)
