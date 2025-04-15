"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import sys
import argparse
import subprocess
import os


def launch_studio():
    from iprm.util.env import Env
    studio_exe_name = f'iprm_studio{".exe" if Env.platform.windows else ""}'
    studio_exe_dir = os.path.join(os.path.dirname(__file__), 'bin')
    try:
        if Env.platform.windows:
            args = [
                os.path.join(studio_exe_dir, studio_exe_name),
                *sys.argv[1:],
            ]
            subprocess.Popen(
                args,
                creationflags=subprocess.DETACHED_PROCESS,
                start_new_session=True
            )
        else:
            # TODO: Add macos app bundle support to IPRM
            """
            args = [
                os.path.join(studio_exe_dir, f'{studio_exe_name}.app', 'Contents', 'MacOS', studio_exe_name),
                *sys.argv[1:],
            ] if Env.platform.macos else [
                os.path.join(studio_exe_dir, studio_exe_name),
                *sys.argv[1:],
            ]
            """
            subprocess.Popen(
                [
                    os.path.join(studio_exe_dir, studio_exe_name),
                    *sys.argv[1:],
                ],
                start_new_session=True
            )
        return 0

    except Exception as e:
        print(f"Unable to launch IPRM Studio: {e}", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(description="IPRM Studio")
    parser.add_argument(
        '-p', '--projdir',
        required=False,
        help='Root directory of the IPRM project'
    )
    parser.add_argument(
        '--plugindir',
        required=False,
        help='Root directory of the IPRM plugins to load'
    )

    parser.parse_args()
    sys.exit(launch_studio())


if __name__ == '__main__':
    main()
