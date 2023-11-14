import dataclasses
import os
import pathlib
import shutil
import sys
import tarfile
import time
import urllib.request

import nox


DIR = pathlib.Path(__file__).parent.resolve()
VENV_DIR = pathlib.Path('./.venv').resolve()


@nox.session(python="3.10.7")
def setup(session: nox.Session) -> None:
    """
    Sets up a python environment for the project.

    This session will:
    - Create a python virtualenv for the session
    - Install the `virtualenv` cli tool into this environment
    - Use `virtualenv` to create a global project virtual environment
    - Invoke the python interpreter from the global project environment to install
      the project and all its development dependencies.
    """
    session.install("virtualenv")
    # VENV_DIR here is a pathlib.Path location of the project virtualenv
    # e.g. .venv
    session.run("virtualenv", os.fsdecode(VENV_DIR), silent=True)

    # Use the venv's interpreter to install the project along with
    # all it's dev dependencies, this ensures it's installed in the right way
    python = os.fsdecode(VENV_DIR.joinpath("bin/python"))

    # NOTE we install vak with the specific commit used to run experiments
    session.run(python, "-m", "pip", "install", "vak @ git+https://github.com/vocalpy/vak@e73f6a396770870c303c1c3574071b53971fc16c", external=True)
    # then we install everything else
    session.run(python, "-m", "pip", "install", "-e", ".", external=True)


@dataclasses.dataclass
class DownloadItem:
    """Dataclass representing item to download:
    either the dataset on Zenodo, or results on OSF"""
    name: str
    url: str
    path: str


TO_DOWNLOAD = [
    # ---- dataset
    DownloadItem(
        name="dataset",
        url="https://zenodo.org/records/10098250/files/all-birds-vak-frame-classification-dataset-generated-231025_173401.tar.gz",
        path="data/prep/multiclass/BFSongRepo/all-birds-vak-frame-classification-dataset-generated-231025_173401.tar.gz",
    ),
    # ---- results
    DownloadItem(
        name="result",
        url="https://osf.io/jnd9x/download",
        path="results/multiclass/results_231025_200608.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/c6m2a/download",
        path="results/multiclass/results_231025_200702.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/snmfk/download",
        path="results/multiclass/results_231025_222720.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/qxndm/download",
        path="results/multiclass/results_231025_222812.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/xm4ps/download",
        path="results/multiclass/ results_231026_085351.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/j7h2f/download",
        path="results/multiclass/results_231026_103215.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/pmc2u/download",
        path="results/multiclass/results_231027_162429.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/sp927/download",
        path="results/multiclass/results_231027_162459.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/mryq5/download",
        path="results/multiclass/results_231028_080948.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/urdm8/download",
        path="results/multiclass/results_231028_124122.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/xd3y2/download",
        path="results/multiclass/results_231103_180218.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/y35j7/download",
        path="results/multiclass/results_231103_180825.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/rt6ej/download",
        path="results/multiclass/results_231104_064536.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/ph7qu/download",
        path="results/multiclass/ results_231104_092453.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/n5ay7/download",
        path="results/multiclass/results_231104_114724.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/br4n5/download",
        path="results/multiclass/results_231025_200608.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/j86bz/download",
        path="results/multiclass/results_231104_152144.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/jnd9x/download",
        path="results/multiclass/results_231104_194434.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/uafmj/download",
        path="results/multiclass/results_231104_215302.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/xgujh/download",
        path="results/multiclass/results_231105_175621.tar.gz",
    ),
]


def reporthook(count, block_size, total_size):
    """hook for urlretrieve that gives us a simple progress report
    https://blog.shichao.io/2012/10/04/progress_speed_indicator_for_urlretrieve_in_python.html
    """
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def copy_url(url: str, path: str) -> None:
    """Copy data from a url to a local file."""
    urllib.request.urlretrieve(url, path, reporthook)


@nox.session
def download(session) -> None:
    """
    Download and extract the dataset and the results.
    """
    session.log(f'Downloading dataset and results')
    for download_item in TO_DOWNLOAD:
        session.log(
            f"Downloading {download_item.name} from {download_item.url} to {download_item.path}"
        )
        copy_url(url=download_item.url, path=download_item.path)
        session.log("\n")
        session.log(f'Extracting downloaded tar: {download_item.path}')
        if download_item.name == "result":
            extract_dir = pathlib.Path(download_item.path).parent
        elif download_item.name == "dataset":
            extract_dir = "data/prep/multiclass"

        shutil.unpack_archive(
            filename=download_item.path,
            extract_dir=,
            format="gztar"
        )
