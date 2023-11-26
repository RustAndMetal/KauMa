from typing import List


class Polynom:
    REDUCTION_POLYNOM = 1 << 128 | 1 << 7 | 1 << 2 | 1 << 1 | 1 << 0
    # REDUCTION_POLYNOM = 0x100000000000000000000000000000087

    def __init__(self, polynom: int):
        self.polynom: int = polynom

    @property
    def inverse(self) -> "Polynom":
        """Calculates the inverse of a polynom

        Returns:
            Polynom: the inverse of the polynom
        """
        return self ** (2**128 - 2)

    @staticmethod
    def from_block(block: bytes) -> "Polynom":
        """Converts a block of GCM to a polynomial

        Args:
            block (bytes): GCM Block

        Returns:
            Polynom: integer representation of the polynom
        """
        polynom = 0
        for index in range(128):
            byte_index = index // 8
            bit_index = 7 - (index % 8)
            if (block[byte_index] >> bit_index) & 1:
                polynom |= 1 << index
        return Polynom(polynom)

    def to_exponents(self) -> List[int]:
        """Converts a polynomial to a list of exponents

        Returns:
            List[int]: list of exponents
        """
        exponents = []
        for index in range(128):
            if (self.polynom >> index) & 1:
                exponents.append(index)
        return exponents

    def from_exponents(exponents: List[int]) -> "Polynom":
        """Converts a list of exponents to a polynomial

        Args:
            exponents (List[int]): list of exponents

        Returns:
            Polynom: the polynom
        """
        polynom = 0
        for exponent in exponents:
            polynom |= 1 << exponent
        return Polynom(polynom)

    def to_block(self) -> bytes:
        """Converts a polynomial to a block of GCM

        Returns:
            bytes: the block
        """
        block = bytearray(16)
        for index in range(128):
            byte_index = index // 8
            bit_index = 7 - (index % 8)
            if (self.polynom >> index) & 1:
                block[byte_index] |= 1 << bit_index
        return bytes(block)

    def __eq__(self, other: "Polynom") -> bool:
        """Method to compare two polynoms

        Args:
            other (Polynom): the other polynom

        Returns:
            bool: true if the polynoms are equal, false otherwise
        """
        return self.polynom == other.polynom

    def __add__(summand_a: "Polynom", summand_b: "Polynom") -> "Polynom":
        """Method to add two polynoms

        Args:
            summand_a (Polynom): first summand
            summand_b (Polynom): second summand

        Returns:
            Polynom: the sum of the polynoms
        """
        return Polynom(summand_a.polynom ^ summand_b.polynom)

    def __sub__(minuend: "Polynom", subtrahend: "Polynom") -> "Polynom":
        """Method to subtract two polynoms

        Args:
            minuend (Polynom): the minuend
            subtrahend (Polynom): the subtrahend

        Returns:
            Polynom: the difference of the polynoms
        """
        return minuend + subtrahend

    def __mul__(factor_a: "Polynom", factor_b: "Polynom") -> "Polynom":
        """Method to multiply two polynoms

        Args:
            factor_a (Polynom): first factor
            factor_b (Polynom): second factor

        Returns:
            Polynom: the product of the polynoms
        """
        product = 0
        a_factor = factor_a.polynom
        b_factor = factor_b.polynom
        # implemented russian peasant multiplication algorithm
        # https://en.wikipedia.org/wiki/Finite_field_arithmetic#C_programming_example
        while a_factor != 0 and b_factor != 0:
            if b_factor & 1:
                product ^= a_factor
            a_factor <<= 1
            if a_factor >> 128:
                a_factor ^= Polynom.REDUCTION_POLYNOM
            b_factor >>= 1
        return Polynom(product)

    def __truediv__(numerator: "Polynom", denumerator: "Polynom") -> "Polynom":
        """Method to divide two polynoms

        Args:
            numerator (Polynom): the numerator
            denumerator (Polynom): the denumerator

        Returns:
            Polynom: the quotient of the polynoms
        """
        return numerator * denumerator.inverse

    def __pow__(base: "Polynom", exponent: int) -> "Polynom":
        """Method to exponentiate a polynom

        Args:
            base (Polynom): the base
            exponent (int): the exponent

        Returns:
            Polynom: the exponentiated polynom
        """
        result = Polynom(1)
        while exponent > 0:
            if exponent & 1:
                result *= base
            exponent >>= 1
            base *= base
        return result
