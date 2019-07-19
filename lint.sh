#!/bin/bash

find . -iname "*.py" | xargs autopep8 --in-place --aggressive --aggressive --max-line-length 160
