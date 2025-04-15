from kwasa.checks import main_checks


def test_checks():
    assert main_checks() is True
