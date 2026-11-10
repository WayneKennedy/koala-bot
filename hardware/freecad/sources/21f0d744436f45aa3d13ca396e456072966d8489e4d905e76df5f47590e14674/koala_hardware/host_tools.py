# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Run external CAD helpers on the host when FreeCAD lives in a Flatpak.

freecad-run provides a short-lived authenticated connection, limited to Node
and PrusaSlicer. Ordinary FreeCAD installs execute those programs directly.
"""
import os
import subprocess
from multiprocessing.connection import Client


def run(command, *, check=False, capture_output=False, text=False, **kwargs):
    endpoint=os.environ.get('KOALA_HOST_TOOLS')
    if not endpoint:return subprocess.run(command,check=check,capture_output=capture_output,text=text,**kwargs)
    with Client(('127.0.0.1',int(endpoint)),authkey=bytes.fromhex(os.environ['KOALA_HOST_KEY'])) as connection:
        connection.send((command,kwargs))
        response=connection.recv()
    if 'error' in response:raise RuntimeError(response['error'])
    stdout,stderr=response['stdout'],response['stderr']
    if not text:stdout=stdout.encode();stderr=stderr.encode()
    result=subprocess.CompletedProcess(command,response['returncode'],stdout,stderr)
    if not capture_output:
        import sys
        sys.stdout.write(response['stdout']);sys.stderr.write(response['stderr'])
    if check:result.check_returncode()
    return result


def check_output(command,*,text=False,**kwargs):
    return run(command,check=True,capture_output=True,text=text,**kwargs).stdout
