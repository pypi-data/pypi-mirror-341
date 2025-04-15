"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import sys
import argparse
import subprocess
import os


def launch_nexus():
    from iprm.util.env import Env
    nexus_exe_name = f'iprm_nexus{".exe" if Env.platform.windows else ""}'
    nexus_exe_dir = os.path.join(os.path.dirname(__file__), 'bin')
    args = [
        os.path.join(nexus_exe_dir, nexus_exe_name),
        *sys.argv[1:],
    ]
    try:
        if Env.platform.windows:
            subprocess.Popen(
                args,
                creationflags=subprocess.DETACHED_PROCESS,
                start_new_session=True
            )
        else:
            subprocess.Popen(
                args,
                start_new_session=True
            )
        return 0

    except Exception as e:
        print(f"Unable to launch IPRM Nexus: {e}", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(description="IPRM Nexus")
    # TODO: define CLI, should have a mode to launch the main web server, and then launch the workers that attach
    #  themselves to a web server
    parser.parse_args()
    sys.exit(launch_nexus())


if __name__ == '__main__':
    main()
