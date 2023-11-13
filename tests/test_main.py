from pytest import approx, raises

from program.main import Program


def test_cosine_dist():
    x = [1, 1, 1, 1]
    y = [2, 2, 2, 2]
    assert Program.cosine_dist(x, y) == approx(0.0)

    x = [1, 2, 3]
    y = [-1, -2, -3]
    assert Program.cosine_dist(x, y) == approx(2.0)

    x = [3, -3]
    y = [-3, 3]
    assert Program.cosine_dist(x, y) == approx(2.0)

    x = [3, 3]
    y = [3, -3]
    assert Program.cosine_dist(x, y) == approx(1.0)

    x = [-2, 3]
    y = [5, 7]
    assert Program.cosine_dist(x, y) == approx(0.645346)


def test_open_wav_file_not_found():
    with raises(FileNotFoundError):
        _ = Program.open_wav('')


def test_open_wav_existing_file():
    _ = Program.open_wav('tests/test.wav')
