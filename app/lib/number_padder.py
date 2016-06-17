def add_zero(number):
    all_numbers = range(0, number+1)
    return map(lambda number: str(number).zfill(2), all_numbers)
