import pytest
import random
from app.lib import number_padder


class TestNumberPadder():

    def test_it_adds_a_leading_zero_to_single_digits_and_returns_as_a_string_in_a_list(self):
        result = number_padder.add_zero(9)
        assert result == ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']

    def test_it_does_not_add_leading_zeros_to_double_digit_numbers(self):
        result = number_padder.add_zero(15)
        assert result == ['00', '01', '02', '03', '04', '05', '06', '07', '08',
                          '09', '10', '11', '12', '13', '14', '15']
