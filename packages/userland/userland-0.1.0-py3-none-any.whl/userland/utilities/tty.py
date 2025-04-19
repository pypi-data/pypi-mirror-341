import os
import sys

from .. import core


parser = core.ExtendedOptionParser(
    usage="%prog [OPTION]",
    description="Print the path to the terminal connected to standard input.",
)

parser.add_option(
    "-s",
    "--silent",
    "--quiet",
    action="store_true",
    help="print nothing; only return an exit status",
)


@core.command(parser)
def python_userland_tty(opts, args: list[str]) -> int:
    parser.expect_nargs(args, 0)

    try:
        ttyname = os.ttyname(sys.stdin.fileno())
    except OSError:
        if not opts.silent:
            print("not a tty")  # to stdout, not stderr
        return 1

    if not opts.silent:
        print(ttyname)

    return 0
