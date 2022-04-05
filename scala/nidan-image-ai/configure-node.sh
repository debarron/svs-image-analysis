#!/bin/bash

echo "
# Hope this works
alias python=python3
" >> ~/.bashrc

source ~/.bashrc

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py --user

python -m pip install numpy --user
python -m pip install opencv-python --user

