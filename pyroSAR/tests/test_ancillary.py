import os
import pytest
import subprocess as sp
import pyroSAR.ancillary as anc


def test_dissolve_with_lists():
    assert anc.dissolve([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert anc.dissolve([[[1]]]) == [1]
    assert anc.dissolve(((1, 2,), (3, 4))) == [1, 2, 3, 4]
    assert anc.dissolve(((1, 2), (1, 2))) == [1, 2, 1, 2]


def test_union():
    assert anc.union([1], [1]) == [1]


def test_dictmerge():
    assert anc.dictmerge({'a': 1, 'b': 2}, {'c': 3, 'd': 4}) == {'a': 1, 'b': 2, 'c': 3, 'd': 4}


def test_parse_literal():
    assert anc.parse_literal(['1', '2.2', 'a']) == [1, 2.2, 'a']
    with pytest.raises(IOError):
        anc.parse_literal(1)


def test_seconds():
    assert anc.seconds('test_20151212T234411') == 3658952651.0


def test_run(tmpdir, testdata):
    log = os.path.join(str(tmpdir), 'test_run.log')
    out, err = anc.run(cmd=['gdalinfo', testdata['tif']],
                       logfile=log, void=False)
    with pytest.raises(OSError):
        anc.run(['foobar'])
    with pytest.raises(sp.CalledProcessError):
        anc.run(['gdalinfo', 'foobar'])


def test_which():
    assert os.path.isfile(anc.which('gdalinfo'))


def test_multicore():
    def add(x, y, z):
        return x + y + z

    assert anc.multicore(add, cores=2, multiargs={'x': [1, 2]}, y=5, z=9) == [15, 16]
    assert anc.multicore(add, cores=2, multiargs={'x': [1, 2], 'y': [5, 6]}, z=9) == [15, 17]
