import dataclasses
import os
import pathlib
import shutil
import tarfile
import urllib.request

import nox

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
        path="data/prep/multiclass/all-birds-vak-frame-classification-dataset-generated-231025_173401.tar.gz",
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
        path="results/multiclass/ results_231104_215302.tar.gz",
    ),
    DownloadItem(
        name="result",
        url="https://osf.io/xgujh/download",
        path="results/multiclass/results_231105_175621.tar.gz",
    ),
]



def copy_url(url: str, path: str) -> None:
    """Copy data from a url to a local file."""
    urllib.request.urlretrieve(url, path)


@nox.session(name='test-data-download-source')
def download(session) -> None:
    """
    Download and extract a .tar.gz file of 'source' test data, used by TEST_DATA_GENERATE_SCRIPT.
    """
    session.log(f'Downloading dataset: {DATASET_URL}')
    copy_url(url=SOURCE_TEST_DATA_URL, path=SOURCE_TEST_DATA_TAR)
    session.log(f'Extracting downloaded tar: {SOURCE_TEST_DATA_TAR}')
    with tarfile.open(SOURCE_TEST_DATA_TAR, "r:gz") as tf:
        tf.extractall(path='.')