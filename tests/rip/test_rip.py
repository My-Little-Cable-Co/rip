import pytest
import subprocess
from rip.rip import Rip
from unittest.mock import patch


@pytest.mark.usefixtures('capsys')
@patch('rip.rip.subprocess.run')
def test_requirements_check__dvd_info_not_in_path(subprocess_run, capsys):
    def subprocess_run_side_effect(*args, **kwargs):
        if args == (['dvd_info', '--version'],):
            # For this test we are testing what happens when dvd_info is not
            # in the PATH, so we will mimic this condition by raising a
            # FileNotFoundError.
            raise FileNotFoundError('dvd_info not in PATH')
        elif args == (['HandBrakeCLI', '--version'],):
            # For this test we are focused on dvd_info, so we'll assume no
            # issues with HandBrakeCLI.
            pass
        else:
            raise ValueError(f'Unexpected arguments for mocked subprocess.run: {args}')

    subprocess_run.side_effect = subprocess_run_side_effect

    # assert the method returned False
    assert not Rip().requirements_check()

    stdout, stderr = capsys.readouterr()
    assert "ERROR, dependency not found: This program requires the 'dvd_info' binary to be in the PATH." in stdout


@pytest.mark.usefixtures('capsys')
@patch('rip.rip.subprocess.run')
def test_requirements_check__dvd_info_in_path(subprocess_run, capsys):
    def subprocess_run_side_effect(*args, **kwargs):
        if args == (['dvd_info', '--version'],):
            # For this test we are testing what happens when dvd_info is in
            # the PATH, so we will mimic this condition by doing nothing.
            pass
        elif args == (['HandBrakeCLI', '--version'],):
            # For this test we are focused on dvd_info, so we'll assume no
            # issues with HandBrakeCLI.
            pass
        else:
            raise ValueError(f'Unexpected arguments for mocked subprocess.run: {args}')

    subprocess_run.side_effect = subprocess_run_side_effect
    
    # assert the method returned True
    assert Rip().requirements_check()

    stdout, stderr = capsys.readouterr()
    # assert that nothing was output as the result of running this
    assert not stdout


@pytest.mark.usefixtures('capsys')
@patch('rip.rip.subprocess.run')
def test_requirements_check__handbrakecli_not_in_path(subprocess_run, capsys):
    def subprocess_run_side_effect(*args, **kwargs):
        if args == (['dvd_info', '--version'],):
            # For this test we are focused on HandBrakeCLI, so we'll assume no
            # issues with dvd_info.
            pass
        elif args == (['HandBrakeCLI', '--version'],):
            # For this test we are testing what happens when HandBrakeCLI is not
            # in the PATH, so we will mimic this condition by raising a
            # FileNotFoundError.
            raise FileNotFoundError('HandBrakeCLI not in PATH')
        else:
            raise ValueError(f'Unexpected arguments for mocked subprocess.run: {args}')

    subprocess_run.side_effect = subprocess_run_side_effect

    # assert the method returned False
    assert not Rip().requirements_check()

    stdout, stderr = capsys.readouterr()
    assert "ERROR, dependency not found: This program requires the 'HandBrakeCLI' binary to be in the PATH." in stdout


@pytest.mark.usefixtures('capsys')
@patch('rip.rip.subprocess.run')
def test_requirements_check__handbrakecli_in_path(subprocess_run, capsys):
    def subprocess_run_side_effect(*args, **kwargs):
        if args == (['dvd_info', '--version'],):
            # For this test we are focused on HandBrakeCLI, so we'll assume no
            # issues with dvd_info.
            pass
        elif args == (['HandBrakeCLI', '--version'],):
            # For this test we are testing what happens when HandBrakeCLI is in
            # the PATH, so we will mimic this condition by doing nothing.
            pass
        else:
            raise ValueError(f'Unexpected arguments for mocked subprocess.run: {args}')

    subprocess_run.side_effect = subprocess_run_side_effect
    
    # assert the method returned True
    assert Rip().requirements_check()

    stdout, stderr = capsys.readouterr()
    # assert that nothing was output as the result of running this
    assert not stdout
