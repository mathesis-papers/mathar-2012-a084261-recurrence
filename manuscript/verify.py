import argparse
from fractions import Fraction
import hashlib
import json
from math import comb, factorial
from pathlib import Path


def defining_sum(index, weight=1):
    return sum(comb(index, 2 * offset) * factorial(offset)
               * weight ** (index - 2 * offset)
               for offset in range(index // 2 + 1))


def coefficients(index):
    return {index - 2 * offset: comb(index, 2 * offset) * factorial(offset)
            for offset in range(index // 2 + 1)}


def determinant(matrix):
    entries = [row[:] for row in matrix]
    previous = 1
    for pivot in range(len(entries) - 1):
        value = entries[pivot][pivot]
        assert value != 0
        for row in range(pivot + 1, len(entries)):
            for column in range(pivot + 1, len(entries)):
                numerator = (entries[row][column] * value
                             - entries[row][pivot] * entries[pivot][column])
                assert numerator % previous == 0
                entries[row][column] = numerator // previous
            entries[row][pivot] = 0
        previous = value
    return entries[-1][-1]


def sibling_checks():
    for index in range(3, 121):
        residual = {}
        for multiplier, shift, offset in (
                (2, 0, 0), (-4, 1, 1), (2, 2, 2),
                (-index, 0, 2), (index - 2, 1, 3)):
            for exponent, value in coefficients(index - offset).items():
                degree = exponent + shift
                residual[degree] = residual.get(degree, 0) + multiplier * value
        assert all(value == 0 for value in residual.values())
    for index in range(1, 121):
        derivative = {exponent - 1: exponent * value
                      for exponent, value in coefficients(index).items()
                      if exponent}
        assert derivative == {exponent: index * value
                              for exponent, value in coefficients(index - 1).items()}
    for weight in (-2, -1, 0, 1, 2):
        for index in range(61):
            row = sum(comb(index, column) * factorial((index - column) // 2)
                      * weight ** column for column in range(index + 1)
                      if (index - column) % 2 == 0)
            assert row == defining_sum(index, weight)
        paths = {0: 1}
        for index in range(61):
            assert paths.get(0, 0) == defining_sum(index, weight)
            following = {}
            for height, value in paths.items():
                following[height + 1] = following.get(height + 1, 0) + value
                following[height] = following.get(height, 0) + weight * value
                if height:
                    following[height - 1] = (following.get(height - 1, 0)
                                             + ((height + 1) // 2) * value)
            paths = following
        for index in range(14):
            matrix = [[defining_sum(row + column, weight)
                       for column in range(index + 1)]
                      for row in range(index + 1)]
            product = 1
            for factor in range(1, index + 1):
                product *= ((factor + 1) // 2) ** (index + 1 - factor)
            assert determinant(matrix) == product
    return {
        'polynomial_recurrence_identities': 118,
        'appell_polynomial_identities': 120,
        'triangle_row_evaluations': 305,
        'continued_fraction_moment_coefficients': 305,
        'hankel_determinants': 70,
        'hankel_indices': [0, 13],
        'asymptotic_scope': 'Universal asymptotic formula has a written proof in note.tex.'
    }


def main():
    parser = argparse.ArgumentParser(description='Exact checks for OEIS A084261')
    parser.add_argument('--to', type=int, default=880)
    parser.add_argument('--oeis-table', type=Path)
    args = parser.parse_args()
    if not 3 <= args.to <= 2000:
        parser.error('--to must be between 3 and 2000')
    sequence = [defining_sum(index) for index in range(args.to + 1)]
    recurrence = [1, 1, 2]
    for index in range(3, args.to + 1):
        numerator = (4 * recurrence[-1] + (index - 2) * recurrence[-2]
                     - (index - 2) * recurrence[-3])
        assert numerator % 2 == 0, ('divisibility', index)
        recurrence.append(numerator // 2)
    assert sequence == recurrence, 'Sum and recurrence differ'
    for weight in (-2, -1, 0, 1, 2):
        polynomials = [defining_sum(index, weight) for index in range(121)]
        assert polynomials[:3] == [1, weight, weight * weight + 1]
        for index in range(3, 121):
            residual = (2 * polynomials[index] - 4 * weight * polynomials[index - 1]
                        + (2 * weight * weight - index) * polynomials[index - 2]
                        + weight * (index - 2) * polynomials[index - 3])
            assert residual == 0, ('weighted recurrence', weight, index)
    seed = lambda index: factorial(index // 2) if index % 2 == 0 else 0
    for index in range(201):
        assert (2 * seed(index + 3) + 2 * seed(index + 2)
                - 3 * seed(index + 1) - 2 * seed(index)
                == index * (seed(index + 1) + seed(index)))
    for index in range(121):
        coefficient = Fraction(factorial(index), factorial(2 * index))
        next_coefficient = Fraction(factorial(index + 1), factorial(2 * index + 2))
        assert (2 * (2 * index + 2) * (2 * index + 1) * next_coefficient
                == (2 * index + 2) * coefficient)
    result = {
        'status': 'pass',
        'arithmetic': 'exact integers and rational numbers',
        'sum_recurrence_indices': [0, args.to],
        'sum_recurrence_values': len(sequence),
        'first_values': sequence[:12],
        'weighted_parameters': [-2, -1, 0, 1, 2],
        'weighted_recurrence_indices': [3, 120],
        'weighted_recurrence_checks': 590,
        'parity_seed_indices': [0, 200],
        'differential_equation_even_coefficients': [0, 120],
        'scope': 'Finite exact checks; universal identities have written proofs in note.tex.'
    }
    result['siblings'] = sibling_checks()
    if args.oeis_table:
        records = {}
        for line in args.oeis_table.read_text().splitlines():
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            index, value = line.split()
            records[int(index)] = int(value)
        assert all(records[index] == value for index, value in enumerate(sequence))
        result['oeis_table_values_matched'] = len(sequence)
        result['oeis_table_sha256'] = hashlib.sha256(args.oeis_table.read_bytes()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
