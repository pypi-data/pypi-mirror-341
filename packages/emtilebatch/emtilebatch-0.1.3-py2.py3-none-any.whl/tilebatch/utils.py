import os
import re
import subprocess
import math
import glob

def ntiles_from_mrc_metadata(extracttiles_string):

    print(extracttiles_string)
    lines = extracttiles_string.split('\n')
    value = 0
    for l in lines:
        if l.lower().count("number of col"):
            value = int(l.split(' ')[-1])
    return value


def extract_dims_from_stack(filelist):
    inputfile = None
    if type(filelist) == type(list()):
        inputfile = filelist[0]
    else:
        inputfile = filelist

    dim_pattern_string = re.compile('.*(\d+x\d+).mrc')
    matched = re.search(dim_pattern_string, inputfile)

    if matched.group(1):
        dim_string = matched.group(1)
        dims_string = dim_string.lower().split('x')
        return [int(dims_string[0]), int(dims_string[1])]
    else:
        cmd = ["extracttilts", inputfile]

        try:
            cmd_out = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdo, stde  = cmd_out.communicate()
        except Exception as ex:
            print(" ".join(cmd), "produced", ex)
            return []

        size_of_dim = int(math.sqrt(ntiles_from_mrc_metadata(stdo.decode('utf8').strip())))

        return [size_of_dim,size_of_dim]


def source_shell_script(script):
    """Sometime you want to emulate the action of "source" in bash,
    settings some environment variables. Here is a way to do it."""

    output = subprocess.check_output(". %s; env" % script, shell=True, text=True)
    #env = dict((line.split("=", 1) for line in output.splitlines()))
    env = {}
    for line in output.splitlines():
        line = line.split("=", 1)
        if len(line) > 1:
            print(line)
            env[line[0]] = line[1]

    os.environ.update(env)


def check_load():
    """obtain the five minute load average of this server using uptime"""

    output = None
    try:
        output = subprocess.check_output(["uptime"])
    except Exception as ex:
        raise

    load_avg = float(output.decode("utf-8").split(",")[-1])
    return load_avg

def has_been_processed(_location):
    """ check if <root>/*-Tiled.tif exists; return True if so """

    root = _location
    if os.path.isfile(_location):
        root = os.path.dirname(_location)

    txt_file = os.path.join(root,"*_overlaps.txt")
    result_file = os.path.join(root,"*-Tiled.tif")

    value = glob.glob(result_file) and glob.glob(txt_file)

    return value
