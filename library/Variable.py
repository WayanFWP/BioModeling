from dataclasses import dataclass, fields
import math

@dataclass
class Angle:
    p: float = 0
    q: float = 0
    r: float = 0
    s: float = 0
    t: float = 0
    
    def to_radians(self):
        """Converts all non-zero angles in-place from degrees to radians."""
        for field in fields(self):
            value = getattr(self, field.name)
            if value != 0:
                # math.radians() is a handy function for this conversion
                setattr(self, field.name, math.radians(value))

@dataclass
class Amplitude:
    p: float = 0
    q: float = 0
    r: float = 0
    s: float = 0
    t: float = 0   
    
    def scale_by(self, factor):
        """Multiplies all numeric attributes by a given factor."""
        for field in fields(self):
            # Get the current value
            current_value = getattr(self, field.name)
            # Check if it's a number before multiplying
            if isinstance(current_value, (int, float)):
                # Update the value
                setattr(self, field.name, current_value * factor)