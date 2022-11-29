from machine import Pin
from time import sleep

try:
    from sr_74hc595_bitbang import SR
except ImportError:
    raise ImportError(
        "Please make sure sr_74hc595_bitbang.py file from https://github.com/mcauser/micropython-74hc595/blob/master/sr_74hc595_bitbang.py is present in the lib directory.")


class SevenSegment74HC595(SR):
    def __init__(self, *args, num_displays: int = 1, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_displays = num_displays
        self.number_to_bits_mapping = {
            0: 0b11111100,
            1: 0b01100000,
            2: 0b11011010,
            3: 0b11110010,
            4: 0b01100110,
            5: 0b10110110,
            6: 0b10111110,
            7: 0b11100000,
            8: 0b11111110,
            9: 0b11110110,
        }

    def show(self, value: int, latch: bool = False):
        # Pad the leading zeros
        digits = f"{value:0{self.num_displays}}"

        # Loop through the inverted list of digits
        for digit in list(digits)[::-1]:
            # Set the bits
            self.bits(self.number_to_bits_mapping[int(digit)], 8)

        # Optionally latch the value
        if latch:
            self.latch()
