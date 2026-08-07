#!/bin/bash
# Automatically generated cron script for VU Quiz Agent
# This ensures the script runs with the correct directory and PATH context

# Navigate to the project directory
cd /Users/retailopakistan/Documents/FardeelAgenticProjects/langraph/vu_quiz_agent

# Set up the path so cron can find 'uv' and other tools
export PATH="/Users/retailopakistan/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# Run the agent and log the output for debugging
echo "--- Starting Agent at $(date) ---" >> output/cron.log
/Users/retailopakistan/.local/bin/uv run main.py >> output/cron.log 2>&1
echo "--- Agent finished ---" >> output/cron.log
