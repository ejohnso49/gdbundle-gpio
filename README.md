# gdbundle-example

This is a [gdbundle](https://github.com/memfault/gdbundle) plugin example as part of my EOSS 2023 talk, Adding Coredumps To Your Debugging Toolkit. This plugin is for use with the Zephyr board, `qemu_cortex_m3`, which contains a GPIO peripheral based on the TI Stellaris GPIO. This plugin provides a simple command to print that state of the collected GPIO0 peripheral in a coredump.

## Compatibility

- GDB

## Installation

After setting up [gdbundle](https://github.com/memfault/gdbundle), clone the project and install locally.

```
$ git clone git@github.com:ejohnso49/gdbundle-gpio && pip install -e gdbundle-gpio
```

If you've decided to manually manage your packages using the `gdbundle(include=[])` argument,
add it to the list of plugins.

```
# .gdbinit

[...]
import gdbundle
plugins = ["gpio"]
gdbundle.init(include=plugins)
```

## Building

```
$ poetry build
$ poetry publish
```
