from __future__ import annotations
from gettext import install
from numbers import Number
import cmath

class OpticalField:
    '''
    Represent a coherent optical field.
    Stored as a complex number:  E = A * exp(i * phi)
    Where,
        A: Amplitude
        phi: Phase
    '''

    def __init__(self, field: complex):
        self._field = complex(field)

    @property
    def field(self) -> complex:
        '''Read-only access to field.'''
        return self._field

    @property
    def phase(self) -> float:
        '''Read-only access to phase in radians.'''
        return cmath.phase(self._field)

    @property
    def amplitude(self) -> float:
        '''Field Amplitude'''
        return abs(self._field)

    @property
    def intensity(self) -> float:
        '''Optical intensity proportional to |E|^2'''
        return abs(self._field)**2

    def phase_shift(self, phi: float) -> OpticalField:
        '''Return a new field with an added phase shift.'''
        return OpticalField(self._field * cmath.exp(1j * phi))

    def __add__(self, other: OpticalField) -> OpticalField:
        if not isinstance(other, OpticalField):
            return NotImplemented
        return OpticalField(self._field + other._field)

    def __sub__(self, other: OpticalField) -> OpticalField:
        if not isinstance(other, OpticalField):
            return NotImplemented
        return OpticalField(self._field - other._field)

    def __mul__(self, scalar: complex | float) -> OpticalField:
        if not isinstance(scalar, Number):
            return NotImplemented
        return OpticalField(self._field * scalar)

    def __rmul__(self, scalar: complex | float) -> OpticalField:
        return self * scalar

    def __truediv__(self, scalar: float) -> OpticalField:
        if not isinstance(scalar, Number):
            return NotImplemented
        return OpticalField(self._field / scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OpticalField):
            return NotImplemented
        return cmath.isclose(
            self._field,
            other._field,
            rel_tol=1e-12,
            abs_tol=1e-12
        )

    def __repr__(self) -> str:
        return f"OpticalField({self._field})"
