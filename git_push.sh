#!/bin/bash

# Optional: Pull latest changes to avoid conflicts
git pull origin main

# Add changes to git
git add .

# Commit changes
git commit -m "Automated Server Update"

# Push changes to GitHub
git push origin main
