#!/bin/bash
cd /home/sairam_achanta/Documents/Doorstep_mobile_services/backend
export PYTHONPATH=$PYTHONPATH:.
echo "Killing existing uvicorn..." > startup.log
pkill -f uvicorn
echo "Fixing schema..." >> startup.log
python3 fix_schema.py >> startup.log 2>&1
echo "Starting seeding and uvicorn..." >> startup.log
nohup python3 -m uvicorn app.main:app --port 8000 --host 0.0.0.0 --reload >> startup.log 2>&1 &
echo "Done." >> startup.log
