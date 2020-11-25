import pytest

from lingpy.basic.wordlist import Wordlist
from lingpy import compat


def test_load_noexisting_cldf(test_data):
    with pytest.raises(compat.FileNotFoundError):
        wl = Wordlist.from_cldf(
            str(test_data / 'cldf/test-missing-metadata.json'),
            col="Language_ID".lower(),
            row="Parameter_ID".lower())


def test_load_non_wordlist_cldf(test_data):
    with pytest.raises(ValueError):
        wl = Wordlist.from_cldf(
            str(test_data / 'cldf/non-wordlist-metadata.json'),
            col="Language_ID".lower(),
            row="Parameter_ID".lower())


def test_load_from_cldf_metadatafree(test_data):
    wl = Wordlist.from_cldf(
        str(test_data / 'cldf/forms.csv'),
        col="Language_ID".lower(),
        row="Parameter_ID".lower())

    assert wl.width == 29
    assert wl.height == 1
    assert wl.entries[0] == 'alignment'
    assert wl.cols[0] == 'anuta'.lower()
    assert wl.cols[28] == 'wallisian'


def test_load_from_cldf_metadata(test_data):
    wl = Wordlist.from_cldf(
        str(test_data / 'cldf/test-metadata.json'),
        col="Language_ID".lower(),
        row="Parameter_ID".lower())

    assert wl.width == 29
    assert wl.height == 1
    assert wl.entries[0] == 'alignment'
    assert wl.cols[0] == 'anuta'.lower()
    assert wl.cols[28] == 'wallisian'


def test_load_cldf_and_write(test_data, tmppath):
    wl = Wordlist.from_cldf(
        str(test_data / 'cldf/test-metadata.json'),
        col="Language_ID".lower(),
        row="Parameter_ID".lower())
    wl.output('tsv', filename=str(tmppath / 'lingpycldf'))