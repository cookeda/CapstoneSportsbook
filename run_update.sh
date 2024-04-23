#!/bin/bash

# Load the user's bashrc in case it's needed for proper Conda initialization
source ~/.bashrc

# Activate the Conda environment
source /home/rkdconnor/anaconda3/bin/activate Capstone

# Run the Python script
python /media/myfiles/CapstoneSportsbook/Update.py

# Execute the Git push script
/media/myfiles/CapstoneSportsbook/git_push.sh