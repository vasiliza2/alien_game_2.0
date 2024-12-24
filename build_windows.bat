@echo off
pyinstaller --noconfirm --onefile --windowed ^
--name "AlienInvasion" ^
--icon=resources/Images/ship.bmp ^
--add-data "resources/Images;resources/Images" ^
--add-data "resources/sounds;resources/sounds" ^
alien_invasion.py
pause
