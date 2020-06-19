#!/bin/bash

# activating environment
source ~/.bashrc
conda activate mpl

# executing script
wd=$(dirname $0)
python $wd
