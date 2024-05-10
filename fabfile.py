#!/usr/bin/python3
from fabric.api import *

@task
def run_hello():
    local("python3 hello.py")

