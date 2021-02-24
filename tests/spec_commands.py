import pytest
from rclcd_drivers import commands as lcd


def test_set_invalid_cgram_addr():
    with pytest.raises(ValueError):
        lcd.set_cgram_addr(0x40)


def test_set_invalid_ddram_addr():
    with pytest.raises(ValueError):
        lcd.set_cgram_addr(0x80)
