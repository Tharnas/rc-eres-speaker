import sys
from .main import main

#
# Dependencies:
# * gpiozero (for gpio)
# * luma & luma.core & luma.oled (for display)

name = "eres"

if __name__ == "__main__":
    sys.exit(main(sys.argv))