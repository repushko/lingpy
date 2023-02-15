"""Implements the lingpy cache.

Some operations in lingpy may be time consuming, so we provide a mechanism to cache the
results of these operations.
"""
import pickle
import pathlib

from lingpy import __version__

DIR = pathlib.Path().joinpath(pathlib.Path().absolute(), "data/models/cache/2.6.9")

def path(filename, d=DIR):
    return d.joinpath(pathlib.Path(filename).name + '.pkl')


def load(filename, d=DIR):
    with path(filename, d=d).open('rb') as fp:
        return pickle.load(fp)


def dump(data, filename, d=DIR):
    return
#    if not d.exists():
#        d.mkdir(parents=True)  # pragma: no cover
#    with path(filename, d=d).open('wb') as fp:
#        pickle.dump(data, fp)
