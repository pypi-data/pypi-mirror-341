from .. import core


# clear(1), roughly modelled off the ncurses implementation.

parser = core.ExtendedOptionParser(
    usage="%prog [OPTION]...",
    description="Clear the terminal screen.",
)

parser.add_option(
    "-x", action="store_true", help="do not try to clear the scrollback buffer"
)


@core.command(parser)
def python_userland_clear(opts, args: list[str]) -> int:
    if args:
        return 1

    print("\x1b[2J\x1b[H", end="")

    if not opts.x:
        print("\x1b[3J", end="")

    return 0
