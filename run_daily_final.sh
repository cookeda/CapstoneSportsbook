#!/bin/bash

# Load the user's bashrc in case it's needed for proper Conda initialization
source ~/.bashrc

# Activate the Conda environment
source /home/rkdconnor/anaconda3/bin/activate Capstone

# Execute the Git push script
/media/myfiles/CapstoneSportsbook/git_pull.sh

# Run the Python script
python /media/myfiles/CapstoneSportsbook/Daily.py

# Push Changes
/media/myfiles/CapstoneSportsbook/git_push.sh
