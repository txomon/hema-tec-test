# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import mock
import pytest

from program import extract_week_information, generate_week_summary, get_csv_paths, get_days, main, process_csv_file, \
    read_csv_file


@pytest.fixture
def mock_read_csv_file(mocker):
    return mocker.patch('program.read_csv_file')


@pytest.fixture
def mock_extract_week_information(mocker):
    return mocker.patch('program.extract_week_information')


@pytest.fixture
def mock_generate_week_summary(mocker):
    return mocker.patch('program.generate_week_summary')


@pytest.fixture
def mock_get_csv_paths(mocker):
    return mocker.patch('program.get_csv_paths')


@pytest.fixture
def mock_process_csv_file(mocker):
    return mocker.patch('program.process_csv_file')


@pytest.mark.parametrize('spec,output', (
        # All correct combinations
        ('mon', ['mon']),
        ('tue', ['tue']),
        ('wed', ['wed']),
        ('thu', ['thu']),
        ('fri', ['fri']),
        ('mon-tue', ['mon', 'tue']),
        ('mon-wed', ['mon', 'tue', 'wed']),
        ('mon-thu', ['mon', 'tue', 'wed', 'thu']),
        ('mon-fri', ['mon', 'tue', 'wed', 'thu', 'fri']),
        ('tue-wed', ['tue', 'wed']),
        ('tue-thu', ['tue', 'wed', 'thu']),
        ('tue-fri', ['tue', 'wed', 'thu', 'fri']),
        ('wed-thu', ['wed', 'thu']),
        ('wed-fri', ['wed', 'thu', 'fri']),
        ('thu-fri', ['thu', 'fri']),
        # Some incorrect
        ('mon-', []),
        ('-fri', []),
        ('sat-sun', []),
        ('fri-mon', ValueError),
        ('some-other-field', []),
        ('someotherfield', []),
        ('mon-itor-field', []),
))
def test_get_days(spec, output):
    if output == ValueError:
        with pytest.raises(output):
            list(get_days(spec))
    else:
        assert output == list(get_days(spec))


@pytest.mark.parametrize('path,output', (
        ('./csv_files', ['1.csv', '2.csv', '3.csv']),
        ('./cv_files', ValueError),  # Not existing dir
        (None, []),  # Empty dir
))
def test_get_csv_paths(path, output, tmpdir):
    if path is None:
        path = str(tmpdir)

    if output == ValueError:
        with pytest.raises(output):
            get_csv_paths(path)
    else:
        assert set(output) == set(k for k, _ in get_csv_paths(path))


@pytest.mark.parametrize('csv_content, output', (
        ('mon,tue\n1,2', (('mon', '1'), ('tue', '2'))),  # Normal csv file
        ('mon,tue\n1,2\n', (('mon', '1'), ('tue', '2'))),  # Normal with new line at the end of the file
        ('mon,tue\n1,2\n1,2', ValueError),  # 3 lines
        ('mon\n1,2', ValueError),
))
def test_read_csv_file(csv_content, output, tmpdir):
    file_csv = tmpdir.join('file.csv')
    file_csv.write(csv_content)

    if output == ValueError:
        with pytest.raises(output):
            tuple(read_csv_file(str(file_csv)))
    else:
        assert output == tuple(read_csv_file(str(file_csv)))


@pytest.mark.parametrize('entries, output', (
        (  # Valid entry
                [('mon', '1'), ('tue', '2'), ('wed', '3'), ('thu', '4'), ('fri', '5'), ('description', 'desc_1')],
                ('desc_1', {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5}),
        ),
        (  # Duplicate day
                [('mon', '1'), ('mon', '2'), ('wed', '3'), ('thu', '4'), ('fri', '5'), ('description', 'desc_1')],
                ValueError,
        ),
        (  # Not a number
                [('mon', 'a'), ('tue', '2'), ('wed', '3'), ('thu', '4'), ('fri', '5'), ('description', 'desc_1')],
                ValueError,
        ),
        (  # Duplicate description
                [('mon', '1'), ('tue', '2'), ('wed', '3'), ('thu', '4'), ('fri', '5'), ('description', 'desc_1'),
                 ('description', 'desc_2')],
                ValueError,
        ),
        (  # Valid entry
                [('mon', '1'), ('wed', '3'), ('thu', '4'), ('fri', '5'), ('description', 'desc_1')],
                ValueError,
        ),
        (  # No description
                [('mon', '1'), ('tue', '2'), ('wed', '3'), ('thu', '4'), ('fri', '5')],
                ValueError,
        ),
        (  # Valid entry with extra data
                [('mon', '1'), ('tue', '2'), ('wed', '3'), ('thu', '4'), ('fri', '5'), ('description', 'desc_1'),
                 ('data', 'col1')],
                ('desc_1', {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5}),
        ),
))
def test_extract_week_information(entries, output):
    if output == ValueError:
        with pytest.raises(output):
            extract_week_information(entries)
    else:
        assert output == extract_week_information(entries)


@pytest.mark.parametrize('input, output', (
        (
                ('d', {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5}),
                [
                    {'day': 'mon', 'description': 'd 1', 'square': 1, 'value': 1},
                    {'day': 'tue', 'description': 'd 4', 'square': 4, 'value': 2},
                    {'day': 'wed', 'description': 'd 9', 'square': 9, 'value': 3},
                    {'day': 'thu', 'description': 'd 8', 'double': 8, 'value': 4},
                    {'day': 'fri', 'description': 'd 10', 'double': 10, 'value': 5},
                ],
        ),
))
def test_generate_week_summary(input, output):
    assert output == generate_week_summary(*input)


def test_process_csv_file(mock_read_csv_file, mock_extract_week_information, mock_generate_week_summary, ):
    csv_file_path = object()
    description, week_info = object(), object()
    mock_extract_week_information.return_value = (description, week_info)
    result = process_csv_file(csv_file_path)

    mock_read_csv_file.assert_called_once_with(csv_file_path)
    mock_extract_week_information.assert_called_once_with(mock_read_csv_file.return_value)
    mock_generate_week_summary.assert_called_once_with(description, week_info)
    assert result == mock_generate_week_summary.return_value


def test_main(mock_get_csv_paths, mock_process_csv_file):
    fn1, fp1, fn2, fp2 = object(), object(), object(), object()
    mock_get_csv_paths.return_value = ((fn1, fp1), (fn2, fp2))

    main()

    assert mock_process_csv_file.mock_calls == [mock.call(fp1), mock.call(fp2)]
