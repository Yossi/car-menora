import subprocess
import argparse
import requests
import mpremote.mip
import os


def download_file(url, path):
    """Downloads a file from a URL and saves it to a path. Returns the name of the file."""
    filename = url.rpartition("/")[2]
    response = requests.get(url)
    os.makedirs(os.path.dirname(f'{path}/{filename}'), exist_ok=True)
    with open(f'{path}/{filename}', 'wb') as file:
        file.write(response.content)
    return f'{path}/{filename}'

def run_mpremote_command(command):
    """Runs an mpremote command and returns the output as a string."""

    result = subprocess.run(["mpremote"] + command.split(), capture_output=True, text=True)

    if result.returncode == 0:
        return result.stdout
    else:
        return f"mpremote command failed: {result.stderr}"

def run_mpy_cross_command(command):
    """Runs mpy-cross command"""

    result = subprocess.run(["mpy-cross"] + command.split(), capture_output=True, text=True)

    if result.returncode == 0:
        return f'{command} compiled'
    else:
        return f"mpy-tool command failed: {result.stderr}"

def get_libs(args):
    from requirements import requirements
    for requirement in requirements:
        print(f'Checking for {requirement.name} | {requirement.url.rpartition("/")[2]} ...')
        if args.update or 'No such file or directory.' in run_mpremote_command(f'sha256sum {requirement.target}/{requirement.url.rpartition("/")[2]}'):
            print(f'Downloading {requirement.name} | {requirement.url.rpartition("/")[2]}')
            file = download_file(mpremote.mip._rewrite_url(requirement.url), requirement.target)
            if args.compile:
                run_mpy_cross_command(f"{file}")
                os.remove(file.replace('.py', '.mpy'))
    print('Uploading lib/ to pico...')
    print(run_mpremote_command(f"cp -r lib/ :lib/"))
    print('Done')


def upload_files(compile=False):
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
        if compile and file.endswith('.py') and file != 'main.py':
            run_mpy_cross_command(f"{file}")
            file = file.replace('.py', '.mpy')
        output = run_mpremote_command(f"cp {file} :")
        if output:
            print(output)
        else:
            print(f'copied {file}')
        if compile and file.endswith('.mpy'):
            os.remove(file)

def reformat(path=''):
    output = run_mpremote_command(f"ls --recursive :{path}")
    print(output)
    for file in output.split('\n')[1:-1]:
        filename = file.split(' ')[-1]
        if filename.endswith('/'): # recursively delete directories
            reformat(f'{path}{filename}')
        output = run_mpremote_command(f"rm --recursive :{path}{filename}")
        print(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', "--update", help="force redownload of libraries in lib/", action="store_true")
    parser.add_argument('-i', "--ignore", help="ignore libraries check entirely", action="store_true")
    parser.add_argument('-c', "--compile", help="compile .py files to .mpy", action="store_true")
    parser.add_argument('-r', "--reformat", help="reformat pi pico filesystem (wipe everything)", action="store_true")

    args = parser.parse_args()

    if args.reformat:
        reformat()
    else:
        if not args.ignore:
            get_libs(args)
        upload_files(args.compile)

    # command = "run main.py"
    # print(f'running {command}')
    # output = run_mpremote_command(command)
    # print(output)

# python setup.py -i; mpremote run main.py
