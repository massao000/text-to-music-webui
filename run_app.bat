@echo off

cd /d %~dp0

py -m venv venv
call ./venv/Scripts/activate

pip install -r requirements.txt

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117

py app.py

pause