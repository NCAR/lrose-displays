#!/usr/bin/env python

#===========================================================================
#
# Run CIDD in docker. Wrapper script.
#
# This script performs the following steps:
#
#   1. clone lrose-core from git
#   2. clone lrose-netcdf from git
#   3. setup autoconf Makefile.am files
#   4. run configure to create makefiles
#   5. perform the build in 32-bit mode, and install
#   6. check the build
#
# You can optionally specify a release date.
#
# Use --help to see the command line options.
#
#===========================================================================

from __future__ import print_function

import os
import sys
from sys import platform
import shutil
import subprocess
from optparse import OptionParser
import time
from datetime import datetime
from datetime import date
from datetime import timedelta

def main():

    global options

    # parse the command line

    thisScriptName = os.path.basename(__file__)
    usage = "usage: " + thisScriptName + " [options]"
    homeDir = os.environ['HOME']
    
    parser = OptionParser(usage)

    parser.add_option('--debug',
                      dest='debug', default=True,
                      action="store_true",
                      help='Set debugging on')
    parser.add_option('--verbose',
                      dest='verbose', default=False,
                      action="store_true",
                      help='Set verbose debugging on')
    parser.add_option('--docker_image',
                      dest='docker_image',
                      default='ncareol/lrose-cidd',
                      help='Set the docker image to run. Should be in DockerHub.')
    parser.add_option('--params_url',
                      dest='params_url',
                      default='http://front.eol.ucar.edu/displayParams/CIDD.pecan',
                      help='Set URL for CIDD params file')

    (options, args) = parser.parse_args()
    
    # check OS - is this a mac?

    global isOsx
    isOsx = False
    if (platform.find("darwin") == 0):
        isOsx = True

    # set DISPLAY string

    if (isOsx):
        ipaddr = "localhost"
        ifconfig = subprocess.check_output(['ifconfig'])
        for line in ifconfig.split("\n"):
            if ((line.find("127.0.0.1") < 0) and line.find("inet ") >= 0):
                ipaddr = line.split(" ")[1]
            #print("line: ", line, file=sys.stderr)
        print("ipaddr: ", ipaddr, file=sys.stderr)
        lrose_display_number=subprocess.check_output(['ps', '-e'])
        #lrose_host_ip=$(ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}' |head -1)
        #lrose_display_number=`ps -e | grep 'Xquartz :\d' | grep -v xinit | awk '{ print substr($5,2); }'`
        displayStr = lrose_host_ip + " " + lrose_display_number
    else:
        displayStr = "-e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix"

    # debug

    if (options.debug):
        print("Running %s:" % thisScriptName, file=sys.stderr)
        print("  docker image: ", options.docker_image, file=sys.stderr)
        print("  CIDD params URL: ", options.params_url, file=sys.stderr)
        if (isOsx):
            print("  OS: this is a mac", file=sys.stderr)
        else:
            print("  OS: this is NOT a mac", file=sys.stderr)
        print("  displayStr: ", displayStr, file=sys.stderr)

    # set up call for running docker
    
    cmd = "docker run -v $HOME/.Xauthority:/root/.Xauthority "
    cmd += "-v /tmp/cidd_images:/root/images "
    cmd += displayStr + " "
    cmd += options.docker_image + " "
    cmd += "/usr/local/cidd/bin/CIDD -font fixed -p "
    cmd += options.params_url
    if (options.verbose):
        cmd += " -v 2"

    # run the command

    shellCmd(cmd)

    # exit

    sys.exit(0)

########################################################################
# Run a command in a shell, wait for it to complete

def shellCmd(cmd):

    print("Running cmd:", cmd, file=sys.stderr)
    
    try:
        retcode = subprocess.check_call(cmd, shell=True)
        if retcode != 0:
            print("Child exited with code: ", retcode, file=sys.stderr)
            sys.exit(1)
        else:
            if (options.verbose):
                print("Child returned code: ", retcode, file=sys.stderr)

    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
        sys.exit(1)

    print("    done", file=sys.stderr)
    
########################################################################
# Run - entry point

if __name__ == "__main__":
   main()
