#! /usr/bin/env python3

import json
import os
import os.path
import shlex
import subprocess
import sys
# import time


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

if __name__ == '__main__':

    json_file = "../../configurations/simulate_xsim.json"
    try:
        f = open(json_file, "r")
        json_data = json.load(f)
    except:
        print("Failed to open %s" % (json_file))
        sys.exit(-1)

    steps = sorted(json_data['flow_steps'].items())
    for step in steps:
        print("\n\nRunning Step: %s " % step[0])
        print("Executable: %s " % json_data['flow'][step[1]]['executable'])
        print("Arguments: %s " % json_data['flow'][step[1]]['arguments'])
        executable = json_data['flow'][step[1]]['executable']
        arguments = json_data['flow'][step[1]]['arguments']
        executable = which(executable)
        if arguments is None:
            command = executable
        else:
            command = executable + " " + str(arguments)

        print(command)
        command = shlex.split(command)
        p = subprocess.Popen(command)
        p.wait()
