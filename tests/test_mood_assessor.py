import pytest
import os
import datetime
from mood_assessor import assess_mood

class Tests:

  @pytest.fixture(scope="function")
  def data_clean(self):
    print("setup")
    f = open('data/mood_diary.txt', 'w')
    f.write('')
    f.close()

  def mock_datetime(self, mock_data, call_counter, monkeypatch):
    """
    Mock the datetime module's today function
    :param mock_data: Dictionary of data to mock.
    :param call_counter: Dictionary of counters for function calls
    :param monkeypatch: pytest's monkeypatch object
    """
    class MockDatetime:
      class date:
        def __init(self, year, month, day):
          return old_datetime.date(year, month, day)
        @classmethod
        def today(cls):
          call_counter['today'] += 1
          return mock_data['today'].pop(0)
    old_datetime = datetime # keep a backup of the original
    monkeypatch.setattr(datetime, 'date', MockDatetime.date)
    
  def mock_input(self, mock_data, call_counter, monkeypatch):
    """
    Mock the builtin input function
    :param mock_data: Dictionary of data to mock.
    :param call_counter: Dictionary of counters for function calls
    :param monkeypatch: pytest's monkeypatch object
    """
    # mock the input function
    def new_input(message):
      call_counter['input'] += 1
      return mock_data['input'].pop(0)
    monkeypatch.setattr('builtins.input', lambda x: new_input(x))
    
  def test_same_date(self, monkeypatch, data_clean):
    """
    Does the program ask for a mood input only once when run multiple times on the same day?
    :param monkeypatch: pytest's monkeypatch object, automatically supplied.
    :param data_clean: the pytest fixture to wipe out the data file, defined in this class.
    """
    global datetime
    
    # number of days for mock data
    num_days = 2

    # date for mocking
    date_today = datetime.date(2020, 6, 18) 

    mock_data = {
      'today': [date_today, date_today, date_today, date_today],
      'input': ['happy', 'sad']
    }
    call_counter = {
      'input': 0,
      'today': 0
    }
    # mock the input function
    self.mock_input(mock_data, call_counter, monkeypatch)

    # mock the datetime module's today function
    self.mock_datetime(mock_data, call_counter, monkeypatch)

    # run the program on the different days
    for i in range(num_days):
      assess_mood()

    # make sure the program only asked for input once
    assert call_counter['input'] == 1
    # datetime = old_datetime # restore it

  def test_different_dates(self, monkeypatch, data_clean):
    """
    Does the program allow the user to enter moods on two different days?
    :param monkeypatch: pytest's monkeypatch object, automatically supplied.
    :param data_clean: the pytest fixture to wipe out the data file, defined in this class.
    """
    global datetime

    # number of days for mock data
    num_days = 3

    # date for mocking
    date_today = datetime.date(2020, 6, 18)
    # generate different test dates
    dates = []
    for i in range(1, num_days + 1):
      test_date = datetime.date(2020, 1, i)
      dates.append(test_date)

    mock_data = {
      'today': [dates[0], date_today, dates[1], date_today, dates[2], date_today],
      'input': ['happy', 'sad', 'apathetic']
    }
    call_counter = {
      'input': 0,
      'today': 0
    }
    # mock the input function
    self.mock_input(mock_data, call_counter, monkeypatch)

    # mock the datetime module's today function
    self.mock_datetime(mock_data, call_counter, monkeypatch)

    # run the program on the different days
    for i in range(num_days):
      assess_mood()

    # make sure the program only asked for input once
    assert call_counter['input'] == 3

  def test_depressive(self, monkeypatch, capsys, data_clean):
    """
    Does the program diagnose depression correctly if there are 4 or more sads within the last 7 days
    :param monkeypatch: pytest's monkeypatch object, automatically supplied.
    :param capsys: pytest's capsys output capture fixture, automatically supplied.
    :param data_clean: the pytest fixture to wipe out the data file, defined in this class.
    """
    global datetime
    
    # number of days for mock data
    num_days = 7

    # date for mocking
    date_today = datetime.date(2020, 6, 18)
    # generate different test dates
    dates = []
    for i in range(1, num_days + 1):
      test_date = datetime.date(2020, 1, i)
      dates.append(test_date)

    mock_data = {
      'today': [dates[0], date_today, dates[1], date_today, dates[2], date_today, dates[3], date_today, dates[4], date_today, dates[5], date_today, dates[6], date_today],
      'input': ['sad', 'sad', 'happy', 'sad', 'happy', 'sad', 'happy']
    }
    call_counter = {
      'input': 0,
      'today': 0
    }
    # mock the input function
    self.mock_input(mock_data, call_counter, monkeypatch)

    # mock the datetime module's today function
    self.mock_datetime(mock_data, call_counter, monkeypatch)

    # run the program on the different days
    for i in range(num_days):
      assess_mood()

    # check the output for the correct diagnosis
    captured = capsys.readouterr()  # capture print output
    actual = captured.out.lower().strip()  # split by line break
    assert 'depressive' in actual or 'depression' in actual  # should be manic!
    
    # check that the input does not also contain an incorrect diagnosis
    wrong_diagnoses = ['happy', 'relaxed', 'apathetic', 'sad', 'angry', 'schizoid', 'manic', 'mania']
    for d in wrong_diagnoses:
      # other diagnoses should not be in any output line
      assert d not in actual

  def test_manic(self, monkeypatch, capsys, data_clean):
    """
    Does the program diagnose mania correctly if there are 5 happies within the last 7 days
    :param monkeypatch: pytest's monkeypatch object, automatically supplied.
    :param capsys: pytest's capsys output capture fixture, automatically supplied.
    :param data_clean: the pytest fixture to wipe out the data file, defined in this class.
    """
    global datetime
    
    # number of days for mock data
    num_days = 7

    # date for mocking
    date_today = datetime.date(2020, 6, 18)
    # generate different test dates
    dates = []
    for i in range(1, num_days + 1):
      test_date = datetime.date(2020, 1, i)
      dates.append(test_date)

    mock_data = {
      'today': [dates[0], date_today, dates[1], date_today, dates[2], date_today, dates[3], date_today, dates[4], date_today, dates[5], date_today, dates[6], date_today],
      'input': ['happy', 'sad', 'happy', 'apathetic', 'happy', 'happy', 'happy']
    }
    call_counter = {
      'input': 0,
      'today': 0
    }
    # mock the input function
    self.mock_input(mock_data, call_counter, monkeypatch)

    # mock the datetime module's today function
    self.mock_datetime(mock_data, call_counter, monkeypatch)

    # run the program on the different days
    for i in range(num_days):
      assess_mood()

    # check the output for the correct diagnosis
    captured = capsys.readouterr()  # capture print output
    actual = captured.out.lower().strip()  # split by line break
    assert 'manic' in actual or 'mania' in actual  # should be manic!
    
    # check that the input does not also contain an incorrect diagnosis
    wrong_diagnoses = ['happy', 'relaxed', 'apathetic', 'sad', 'angry', 'schizoid', 'depressive', 'depression']
    for d in wrong_diagnoses:
      # other diagnoses should not be in any output line
      assert d not in actual

  def test_schizoid(self, monkeypatch, capsys, data_clean):
    """
    Does the program diagnose schizoid disorder correctly if there are 6 apathetics within the last 7 days
    :param monkeypatch: pytest's monkeypatch object, automatically supplied.
    :param capsys: pytest's capsys output capture fixture, automatically supplied.
    :param data_clean: the pytest fixture to wipe out the data file, defined in this class.
    """
    global datetime
    
    # number of days for mock data
    num_days = 7

    # date for mocking
    date_today = datetime.date(2020, 6, 18)
    # generate different test dates
    dates = []
    for i in range(1, num_days + 1):
      test_date = datetime.date(2020, 1, i)
      dates.append(test_date)

    mock_data = {
      'today': [dates[0], date_today, dates[1], date_today, dates[2], date_today, dates[3], date_today, dates[4], date_today, dates[5], date_today, dates[6], date_today],
      'input': ['apathetic', 'apathetic', 'happy', 'apathetic', 'apathetic', 'apathetic', 'apathetic']
    }
    call_counter = {
      'input': 0,
      'today': 0
    }
    # mock the input function
    self.mock_input(mock_data, call_counter, monkeypatch)

    # mock the datetime module's today function
    self.mock_datetime(mock_data, call_counter, monkeypatch)

    # run the program on the different days
    for i in range(num_days):
      assess_mood()

    # check the output for the correct diagnosis
    captured = capsys.readouterr()  # capture print output
    actual = captured.out.lower().strip()  # split by line break
    assert 'schizoid' in actual  # should be a match!
    
    # check that the input does not also contain an incorrect diagnosis
    wrong_diagnoses = ['happy', 'relaxed', 'apathetic', 'sad', 'angry', 'manic', 'mania', 'depressive', 'depression']
    for d in wrong_diagnoses:
      # other diagnoses should not be in any output line
      assert d not in actual

  def test_average_mood(self, monkeypatch, capsys, data_clean):
    """
    Does the program outputs the average mood if no other disorder found.
    :param monkeypatch: pytest's monkeypatch object, automatically supplied.
    :param capsys: pytest's capsys output capture fixture, automatically supplied.
    :param data_clean: the pytest fixture to wipe out the data file, defined in this class.
    """
    global datetime
    
    # number of days for mock data
    num_days = 7

    # date for mocking
    date_today = datetime.date(2020, 6, 18)
    # generate different test dates
    dates = []
    for i in range(1, num_days + 1):
      test_date = datetime.date(2020, 1, i)
      dates.append(test_date)

    mock_data = {
      'today': [dates[0], date_today, dates[1], date_today, dates[2], date_today, dates[3], date_today, dates[4], date_today, dates[5], date_today, dates[6], date_today],
      'input': ['angry', 'happy', 'angry', 'happy', 'angry', 'happy', 'apathetic']
    }
    call_counter = {
      'input': 0,
      'today': 0
    }
    # mock the input function
    self.mock_input(mock_data, call_counter, monkeypatch)

    # mock the datetime module's today function
    self.mock_datetime(mock_data, call_counter, monkeypatch)

    # run the program on the different days
    for i in range(num_days):
      assess_mood()

    # check the output for the correct diagnosis
    captured = capsys.readouterr()  # capture print output
    actual = captured.out.lower().strip()  # split by line break
    assert 'apathetic' in actual  # should be a match!
    
    # check that the input does not also contain an incorrect diagnosis
    wrong_diagnoses = ['happy', 'relaxed', 'sad', 'angry', 'schizoid', 'manic', 'mania', 'depressive', 'depression']
    for d in wrong_diagnoses:
      # other diagnoses should not be in any output line
      assert d not in actual

  def test_analyze_only_last_week(self, monkeypatch, capsys, data_clean):
    """
    Does the program really only look at the past week's worth of moods?
    :param monkeypatch: pytest's monkeypatch object, automatically supplied.
    :param capsys: pytest's capsys output capture fixture, automatically supplied.
    :param data_clean: the pytest fixture to wipe out the data file, defined in this class.
    """
    global datetime
    
    # number of days for mock data
    num_days = 8

    # date for mocking
    date_today = datetime.date(2020, 6, 18)
    # generate 7 different test dates
    dates = []
    for i in range(1, num_days + 1):
      test_date = datetime.date(2020, 1, i)
      dates.append(test_date)

    mock_data = {
      'today': [dates[0], date_today, dates[1], date_today, dates[2], date_today, dates[3], date_today, dates[4], date_today, dates[5], date_today, dates[6], date_today, dates[7], date_today],
      'input': ['happy', 'happy', 'happy', 'happy', 'happy', 'apathetic', 'apathetic', 'apathetic']
    }
    call_counter = {
      'input': 0,
      'today': 0
    }
    # mock the input function
    self.mock_input(mock_data, call_counter, monkeypatch)

    # mock the datetime module's today function
    self.mock_datetime(mock_data, call_counter, monkeypatch)

    # run the program on different days
    for i in range(num_days):
      assess_mood()

    # check the output for the correct diagnosis
    captured = capsys.readouterr()  # capture print output
    actual = captured.out.lower().strip()  # split by line break
    assert 'manic' in actual or 'mania' in actual # should be a match from the first 7 days
    assert 'relaxed' in actual  # should be a match from the most recent 7 days
    
    # check that the input does not also contain an incorrect diagnosis
    wrong_diagnoses = ['happy', 'sad', 'angry', 'schizoid', 'depressive', 'depression']
    for d in wrong_diagnoses:
      # other diagnoses should not be in any output line
      assert d not in actual
