from . import polynom
from typing import Optional


class MetaPolynom:
    def __init__(self, coefficients: list[polynom.Polynom]):
        """Initializes a MetaPolynom without leading zeros"""
        while len(coefficients) > 0 and coefficients[-1] == polynom.Polynom(0):
            coefficients.pop()
        self._coefficients: list[polynom.Polynom] = coefficients
        """coefficients == polynom.Polynom"""

    def __len__(self) -> int:
        """Returns number of coefficients"""
        return len(self._coefficients)

    def __getitem__(self, index: int) -> polynom.Polynom:
        """Returns the coefficient at the given index

        Args:
            index (int): the index

        Returns:
            polynom.Polynom: the coefficient
        """
        return (
            self._coefficients[index]
            if index < len(self._coefficients)
            else polynom.Polynom(0)
        )

    def __iter__(self) -> iter:
        """Returns an iterator over the coefficients

        Returns:
            iter: the iterator
        """
        return iter(self._coefficients)

    def __eq__(a: "MetaPolynom", b: "MetaPolynom") -> bool:
        """Checks if two polynomials are equal

        Args:
            a (MetaPolynom): The first polynomial
            b (MetaPolynom): The second polynomial

        Returns:
            bool: True if the polynomials are equal, False otherwise
        """
        return a._coefficients == b._coefficients

    def to_monic(self) -> "MetaPolynom":
        """Converts the polynomial to monic form

        Returns:
            MetaPolynom: The monic polynomial
        """
        if len(self) == 0:
            return self
        return self // MetaPolynom([self._coefficients[-1]])

    def __add__(summand_a: "MetaPolynom", summand_b: "MetaPolynom") -> "MetaPolynom":
        """Adds two polynomials

        Args:
            summand_a (MetaPolynom): first summand
            summand_b (MetaPolynom): second summand

        Returns:
            MetaPolynom: The sum of the polynomials as MetaPolynom
        """
        out = []
        for i in range(max(len(summand_a), len(summand_b))):
            out.append(summand_a[i] + summand_b[i])
        return MetaPolynom(out)

    def __sub__(minuend: "MetaPolynom", subtrahend: "MetaPolynom") -> "MetaPolynom":
        """Subtracts two polynomials

        Args:
            minuend (MetaPolynom): to be subtracted from
            subtrahend (MetaPolynom): subtracts from minuend
        Returns:
            MetaPolynom: The difference of the polynomials
        """
        return minuend + subtrahend

    def __mul__(factor_a: "MetaPolynom", factor_b: "MetaPolynom") -> "MetaPolynom":
        """Multiplies two polynomials

        Args:
            factor_a (MetaPolynom): first factor
            factor_b (MetaPolynom): second factor

        Returns:
            MetaPolynom: The product of the polynomials
        """
        out = [polynom.Polynom(0)] * (len(factor_a) + len(factor_b) - 1)
        for i in range(len(factor_a)):
            for j in range(len(factor_b)):
                out[i + j] += factor_a[i] * factor_b[j]
        return MetaPolynom(out)

    def __divmod__(
        numerator: "MetaPolynom", denominator: "MetaPolynom"
    ) -> tuple["MetaPolynom", "MetaPolynom"]:
        """Divides two polynomials

        Args:
            numerator (MetaPolynom): The numerator
            denominator (MetaPolynom): The denominator

        Returns:
            tuple[MetaPolynom, MetaPolynom]: The quotient and the remainder of the division
        """
        quotient = [polynom.Polynom(0)] * (len(numerator) - len(denominator) + 1)
        remainder = numerator
        while len(remainder) >= len(denominator):
            factor = remainder[len(remainder) - 1] / denominator[len(denominator) - 1]
            quotient[len(remainder) - len(denominator)] = factor
            remainder -= (
                MetaPolynom(quotient[: len(remainder) - len(denominator) + 1])
                * denominator
            )
        return MetaPolynom(quotient), MetaPolynom(remainder)

    def __mod__(dividend_mod: "MetaPolynom", modulo: "MetaPolynom") -> "MetaPolynom":
        """Calculates the remainder of the division of two polynomials

        Args:
            dividend_mod (MetaPolynom): The dividend to be divided
            modulo (MetaPolynom): The modulo to be divided by

        Returns:
            MetaPolynom: The remainder of the division
        """
        return divmod(dividend_mod, modulo)[1]

    def __floordiv__(dividend: "MetaPolynom", divisor: "MetaPolynom") -> "MetaPolynom":
        """Calculates the quotient of the division of two polynomials

        Args:
            dividend (MetaPolynom): The dividend to be divided
            divisor (MetaPolynom): The divisor to be divided by

        Returns:
            MetaPolynom: The quotient of the division
        """
        return divmod(dividend, divisor)[0]

    def __pow__(
        base: "MetaPolynom", exponent: int, modulo: Optional["MetaPolynom"] = None
    ) -> "MetaPolynom":
        """Raises a polynomial to a power

        Args:
            base (MetaPolynom): The polynomial to be raised to a power
            exponent (int): The power
            modulo (Optional[MetaPolynom], optional): The modulo. Defaults to None.

        Returns:
            MetaPolynom: The power of the polynomial
        """
        out = MetaPolynom([polynom.Polynom(1)])
        while exponent > 0:
            if exponent % 2 == 1:
                out *= base
            base *= base
            exponent //= 2
            if modulo is not None:
                out %= modulo
                base %= modulo
        return out

    def gcd(a: "MetaPolynom", b: "MetaPolynom") -> "MetaPolynom":
        """Calculates the greatest common divisor of two polynomials

        Args:
            a (MetaPolynom): The first polynomial
            b (MetaPolynom): The second polynomial

        Returns:
            MetaPolynom: The greatest common divisor of the polynomials
        """
        while len(b) > 0:
            a, b = b, a % b
        return a
