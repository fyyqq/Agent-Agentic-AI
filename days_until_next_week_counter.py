
import datetime

def count_days_to_next_week():
    """
    Prints the dates from today up to the next week (7 days), inclusively.
    
    Description:
        This function starts at the current date and prints out the date for each day,
        up to and including the date 7 days later (i.e., 8 days total, counting today).
        Useful for generating a sequence of dates for scheduling, logging, or reminders
        over the course of a week starting from the present.

    Parameters:
        None

    Returns:
        None
        This function only prints output to the console.

    Example Usage:
        >>> count_days_to_next_week()
        Counting from today (2024-06-09) to the next 7 days:
        Day 0: 2024-06-09
        Day 1: 2024-06-10
        ...
        Day 7: 2024-06-16

    Edge Cases:
        - Handles year/month/day roll-over (e.g., if today is December 28, dates will cross to the next month/year).
        - Relies on system local date; if the system clock is incorrect, results may vary.
        - There is no input parameter. To get dates from a specific start date, modify the function
          to accept a parameter.

    Limitations:
        - The function does not return the dates as a data structure (e.g., list). To access the dates
          programmatically, adapt the function to return them.
        - No timezone awareness: uses local "naive" dates.
    """
    today = datetime.date.today()
    print("Counting from today ({}) to the next 7 days:".format(today))
    for i in range(8):  # inclusive of today (0) to day 7
        next_day = today + datetime.timedelta(days=i)
        print(f"Day {i}: {next_day}")

# Example usage:
# count_days_to_next_week()


import unittest
from unittest.mock import patch
import datetime

def count_days_to_next_week():
    """
    Prints the dates from today up to the next week (7 days), inclusively.
    
    Description:
        This function starts at the current date and prints out the date for each day,
        up to and including the date 7 days later (i.e., 8 days total, counting today).
        Useful for generating a sequence of dates for scheduling, logging, or reminders
        over the course of a week starting from the present.

    Parameters:
        None

    Returns:
        None
        This function only prints output to the console.

    Example Usage:
        >>> count_days_to_next_week()
        Counting from today (2024-06-09) to the next 7 days:
        Day 0: 2024-06-09
        Day 1: 2024-06-10
        ...
        Day 7: 2024-06-16

    Edge Cases:
        - Handles year/month/day roll-over (e.g., if today is December 28, dates will cross to the next month/year).
        - Relies on system local date; if the system clock is incorrect, results may vary.
        - There is no input parameter. To get dates from a specific start date, modify the function
          to accept a parameter.

    Limitations:
        - The function does not return the dates as a data structure (e.g., list). To access the dates
          programmatically, adapt the function to return them.
        - No timezone awareness: uses local "naive" dates.
    """
    today = datetime.date.today()
    print("Counting from today ({}) to the next 7 days:".format(today))
    for i in range(8):  # inclusive of today (0) to day 7
        next_day = today + datetime.timedelta(days=i)
        print(f"Day {i}: {next_day}")

class TestCountDaysToNextWeek(unittest.TestCase):

    @patch('datetime.date')
    def test_basic_functionality(self, mock_date):
        """Test that the function outputs the correct range of dates for a normal day."""
        mock_today = datetime.date(2023, 7, 15)
        mock_date.today.return_value = mock_today
        mock_date.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)
        expected_output = [
            "Counting from today (2023-07-15) to the next 7 days:\n"
        ]
        for i in range(8):
            output_line = f"Day {i}: {mock_today + datetime.timedelta(days=i)}\n"
            expected_output.append(output_line)
        with patch('sys.stdout') as mock_stdout:
            mock_stdout.write = lambda s: super(type(mock_stdout), mock_stdout).write(s) if hasattr(mock_stdout, 'write') else None
            import io
            mock_stdout = io.StringIO()
            with patch('sys.stdout', mock_stdout):
                count_days_to_next_week()
            self.assertEqual(mock_stdout.getvalue(), ''.join(expected_output))

    @patch('datetime.date')
    def test_year_rollover(self, mock_date):
        """Test the function on a year-end boundary (Dec 28)."""
        mock_today = datetime.date(2023, 12, 28)
        mock_date.today.return_value = mock_today
        mock_date.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)
        expected_output = [
            "Counting from today (2023-12-28) to the next 7 days:\n"
        ]
        for i in range(8):
            output_line = f"Day {i}: {mock_today + datetime.timedelta(days=i)}\n"
            expected_output.append(output_line)
        import io
        mock_stdout = io.StringIO()
        with patch('sys.stdout', mock_stdout):
            count_days_to_next_week()
        self.assertEqual(mock_stdout.getvalue(), ''.join(expected_output))

    @patch('datetime.date')
    def test_leap_year_boundary(self, mock_date):
        """Test if February 27 in a leap year properly outputs Feb 29."""
        mock_today = datetime.date(2024, 2, 27)
        mock_date.today.return_value = mock_today
        mock_date.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)
        expected_output = [
            "Counting from today (2024-02-27) to the next 7 days:\n"
        ]
        for i in range(8):
            output_line = f"Day {i}: {mock_today + datetime.timedelta(days=i)}\n"
            expected_output.append(output_line)
        import io
        mock_stdout = io.StringIO()
        with patch('sys.stdout', mock_stdout):
            count_days_to_next_week()