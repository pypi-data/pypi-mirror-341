# ducktools.env
# MIT License
# 
# Copyright (c) 2024 David C Ellis
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os.path
import sys

from .get_pip import retrieve_pip
from .._logger import log
from .. import _lazy_imports as _laz
from ..platform_paths import ManagedPaths


uv_versionspec = ">=0.6.5"
uv_versionre = r"^uv (?P<uv_ver>\d+\.\d+\.\d+)"

uv_download = "bin/uv.exe" if sys.platform == "win32" else "bin/uv"


def download_uv(paths: ManagedPaths):
    # Just the code to download UV from PyPI if it is otherwise unavailable
    pip_install = retrieve_pip(paths=paths)

    log("Downloading UV from PyPi")
    with paths.build_folder() as build_folder:

        install_folder = os.path.join(build_folder, "uv")

        uv_dl = os.path.join(install_folder, uv_download)

        pip_command = [
            sys.executable,
            pip_install,
            "--disable-pip-version-check",
            "install",
            "-q",
            f"uv{uv_versionspec}",
            "--only-binary=:all:",
            "--target",
            install_folder,
        ]

        # Download UV with pip - handles getting the correct platform version
        try:
            _laz.subprocess.run(
                pip_command,
                check=True,
            )
        except _laz.subprocess.CalledProcessError as e:
            log(f"UV download failed: {e}")
            uv_path = None
        else:
            # Copy the executable out of the pip install
            _laz.shutil.copy(uv_dl, paths.uv_executable)
            uv_path = paths.uv_executable

            version_command = [uv_path, "-V"]
            version_output = _laz.subprocess.run(version_command, capture_output=True, text=True)
            ver_match = _laz.re.match(uv_versionre, version_output.stdout.strip())
            if ver_match:
                uv_version = ver_match.group("uv_ver")
                with open(f"{uv_path}.version", 'w') as ver_file:
                    ver_file.write(uv_version)
            else:
                log(f"Unexpected UV version output {version_output.stdout!r}")
                uv_path = None

    return uv_path


def get_local_uv():
    uv_path = _laz.shutil.which("uv")
    if uv_path:
        try:
            version_output = _laz.subprocess.run([uv_path, "-V"], capture_output=True, text=True)
        except (FileNotFoundError, _laz.subprocess.CalledProcessError):
            return None

        ver_match = _laz.re.match(uv_versionre, version_output.stdout.strip())
        if ver_match:
            uv_version = ver_match.group("uv_ver")
            if uv_version not in _laz.SpecifierSet(uv_versionspec):
                log(
                    f"Local uv install version {uv_version!r} "
                    f"does not satisfy the ducktools.env specifier {uv_versionspec!r}"
                )
                return None

    return uv_path


def retrieve_uv(paths: ManagedPaths, reinstall: bool = False) -> str | None:
    uv_path = get_local_uv()

    if os.path.exists(paths.uv_executable):
        uv_path = paths.uv_executable
        uv_version = paths.get_uv_version()

        if reinstall or not uv_version or uv_version not in _laz.SpecifierSet(uv_versionspec):
            uv_versionfile = f"{uv_path}.version"
            os.remove(uv_path)
            os.remove(uv_versionfile)
            uv_path = None

    if uv_path is None:
        uv_path = download_uv(paths=paths)

    return uv_path


def get_available_pythons(uv_path: str) -> list[str]:
    """
    Get all python install version numbers available from UV

    :param uv_path: Path to the UV executable
    :return: list of version strings
    """
    # CPython installs listed by UV - only want downloadable installs
    version_re = _laz.re.compile(
        r"(?m)^cpython-(?P<version>\d+.\d+.\d+(?:a|b|rc)?\d*).*<download available>$"
    )
    data = _laz.subprocess.run(
        [
            uv_path,
            "python",
            "list",
            "--all-versions",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    matches = version_re.findall(data.stdout)

    return matches


def install_uv_python(*, uv_path: str, version_str: str) -> None:
    _laz.subprocess.run(
        [
            uv_path,
            "python",
            "install",
            version_str,
        ],
        check=True,
    )
