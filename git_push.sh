#!/bin/bash
cd /media/myfiles/CapstoneSportsbook
# Optional: Pull latest changes to avoid conflicts
git pull origin main

# Add changes to git
git add .

# Commit changes
git commit -m "Testing Automated Server Update, IT WORKED!!!"

# Push changes to GitHub
git push origin main
