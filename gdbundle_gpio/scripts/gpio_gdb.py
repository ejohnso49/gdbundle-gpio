import gdb


class Gpio(gdb.Command):
    """Prints state of GPIO0"""

    def __init__(self):
        super().__init__('gpio', gdb.COMMAND_USER)

    def invoke(self, _unicode_args, _from_tty):
        gpio_region = gdb.selected_inferior().read_memory(0x40004000, 0x1000)
        print(gpio_region)

Gpio()
