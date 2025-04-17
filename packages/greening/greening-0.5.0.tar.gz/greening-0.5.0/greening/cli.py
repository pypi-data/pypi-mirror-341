import sys

from greening.commands.new import new, help_new
from greening.commands.deploy import deploy_site, help_deploy
from greening.commands.init import init, help_init
from greening.commands.help import general_help

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        general_help()
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "new":
        if "--help" in args:
            help_new()
        else:
            new()
    elif command == "init":
        if "--help" in args:
            help_init()
        else:
            init()
    elif command == "help":
        if args:
            cmd = args[0]
            if cmd == "new":
                help_new()
            elif cmd == "init":
                help_init()
            else:
                print(f"Unknown command: {cmd}")
                general_help()
        else:
            general_help()
    else:
        general_help()
