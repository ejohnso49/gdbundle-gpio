import gdb


GPIO_DATA_OFFSET = 0x000
GPIO_DIR_OFFSET = 0x400
GPIO_DEN_OFFSET = 0x51C
GPIO_IS_OFFSET = 0x404
GPIO_IBE_OFFSET = 0x408
GPIO_IEV_OFFSET = 0x40C
GPIO_IM_OFFSET = 0x410
GPIO_MIS_OFFSET = 0x418
GPIO_ICR_OFFSET = 0x41C


class GpioPin():
    def __init__(self, memory, pin):
        self.pin = pin
        self.memory = memory

    @property
    def enabled(self):
        return "enabled" if int.from_bytes(self.memory[GPIO_DEN_OFFSET], "little") & (1 << self.pin) else "disabled"

    @property
    def direction(self):
        return "output" if int.from_bytes(self.memory[GPIO_DIR_OFFSET], "little") & (1 << self.pin) else "input"

    @property
    def value(self):
        raw_bits = int.from_bytes(self.memory[GPIO_DATA_OFFSET | (0xFF << 2)], "little")
        return "1" if raw_bits & (1 << self.pin) else "0"

    @property
    def interrupt_enabled(self):
        return "enabled" if int.from_bytes(self.memory[GPIO_IM_OFFSET], "little") & (1 << self.pin) else "disabled"

    @property
    def interrupt_trigger(self):
        level_type = int.from_bytes(self.memory[GPIO_IS_OFFSET], "little") & (1 << self.pin)
        if level_type:
            voltage_level = int.from_bytes(self.memory[GPIO_IEV_OFFSET], "little") & (1 << self.pin)
            return "high level" if voltage_level else "low level"
        else:
            both_edges = int.from_bytes(self.memory[GPIO_IBE_OFFSET], "little") & (1 << self.pin)
            if both_edges:
                return "both edges"
            edge_type = "rising" if int.from_bytes(self.memory[GPIO_IEV_OFFSET], "little") & (1 << self.pin) else "falling"
            return " ".join([edge_type, "edges"])

    def __str__(self):
        return f"""GPIO0 pin {self.pin}:
        enabled[{self.enabled}],
        direction[{self.direction}],
        value[{self.value}],
        interrupt enabled[{self.interrupt_enabled}],
        interrupt trigger[{self.interrupt_trigger}]
        """


class Gpio(gdb.Command):
    """Prints state of GPIO0"""

    def __init__(self):
        super().__init__('gpio', gdb.COMMAND_USER)

    def invoke(self, _unicode_args, _from_tty):
        gpio_region = gdb.selected_inferior().read_memory(0x40004000, 0x1000)
        for pin in range(8):
            gpio_pin = GpioPin(gpio_region, pin)
            print(gpio_pin)

Gpio()
