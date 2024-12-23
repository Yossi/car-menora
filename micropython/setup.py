import subprocess
import argparse


def run_mpremote_command(command):
    """Runs an mpremote command and returns the output as a string."""

    result = subprocess.run(["mpremote"] + command.split(), capture_output=True, text=True)

    if result.returncode == 0:
        return result.stdout
    else:
        return f"mpremote command failed: {result.stderr}"

def run_mpy_tool_command(command):
    """Runs an mpy-tool command and returns the output as a string."""

    result = subprocess.run(["mpy-tool"] + command.split(), capture_output=True, text=True)

    if result.returncode == 0:
        return result.stdout
    else:
        return f"mpy-tool command failed: {result.stderr}"

def get_libs(update):
    from requirements import requirements
    for requirement in requirements:
        print(f'Checking {requirement.name} | {requirement.url.rpartition("/")[2]} ...')
        if update or 'No such file or directory.' in run_mpremote_command(f'sha256sum {requirement.target}/{requirement.url.rpartition("/")[2]}'):
            output = run_mpremote_command(f"mip --target {requirement.target} install {requirement.url}")
            print(output)
        else:
            print('OK')

def upload_files():
    files = (
        'main.py',
        'RGBsetup.py',
        'requirements.py',
        'connect.py',
        'networks.py',
        'host.py',
        'RGBserver.py',
        'menorah.py',
        'shiftregister.py',
        'index.html'
    )
    for file in files:
        # run_mpy_tool_command(f"{file}")
        output = run_mpremote_command(f"cp {file} :")
        if output:
            print(output)
        else:
            print(f'copied {file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', "--update", help="force redownload of libraries in lib/", action="store_true")
    parser.add_argument('-i', "--ignore", help="ignore libraries check entirely", action="store_true")

    args = parser.parse_args()

    if not args.ignore:
        get_libs(args.update)

    upload_files()

    command = "run main.py"
    print(f'running {command}')
    output = run_mpremote_command(command)
    print(output)
