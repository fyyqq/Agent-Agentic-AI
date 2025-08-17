
def factorial(n):
    """
    Calculate the factorial of a non-negative integer.

    The factorial of a non-negative integer n, denoted as n!, is the product 
    of all positive integers less than or equal to n. By definition, 0! = 1.

    Parameters
    ----------
    n : int
        The non-negative integer for which to compute the factorial.

    Returns
    -------
    int
        The factorial of the input integer n.

    Raises
    ------
    ValueError
        If n is negative.
    TypeError
        If n is not an integer.

    Examples
    --------
    >>> factorial(5)
    120
    >>> factorial(0)
    1
    >>> factorial(1)
    1

    Edge Cases
    ----------
    - n = 0: Returns 1, since 0! = 1 by definition.
    - n = 1: Returns 1, since 1! = 1.
    - n < 0: Raises ValueError, since factorial is not defined for negative numbers.
    - n is not an integer: Raises TypeError.

    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


import unittest

class TestFactorialFunction(unittest.TestCase):

    def test_basic_functionality(self):
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(3), 6)
        self.assertEqual(factorial(2), 2)

    def test_edge_cases(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)

    def test_error_negative_input(self):
        with self.assertRaises(ValueError):
            factorial(-1)
        with self.assertRaises(ValueError):
            factorial(-100)

    def test_error_non_integer_input(self):
        with self.assertRaises(TypeError):
            factorial(4.5)
        with self.assertRaises(TypeError):
            factorial("5")
        with self.assertRaises(TypeError):
            factorial(None)
        with self.assertRaises(TypeError):
            factorial([1,2,3])
        with self.assertRaises(TypeError):
            factorial({})

    def test_large_input(self):
        self.assertEqual(factorial(10), 3628800)
        self.assertEqual(factorial(15), 1307674368000)

    def test_bool_input(self):
        # in Python, bool is a subclass of int, so True == 1, False == 0
        self.assertEqual(factorial(True), 1)
        self.assertEqual(factorial(False), 1)

if __name__ == "__main__":
    unittest.main()