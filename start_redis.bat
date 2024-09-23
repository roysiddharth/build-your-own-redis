@echo off

REM Activate the conda environment
CALL conda activate byo-redis

REM Run the Python script
cd D:\Projects\byo-redis\src
python main.py

pause