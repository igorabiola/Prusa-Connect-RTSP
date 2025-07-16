@echo off
echo Creating timelapse from frames (OpenCV)

REM Default values
set FRAMES_DIR=timelapse_frames
set FPS=24
set WIDTH=1920

REM Check if folder exists
if not exist "%FRAMES_DIR%" (
    echo Folder %FRAMES_DIR% does not exist
    echo First run main.py with ENABLE_TIMELAPSE=true
    pause
    exit
)

echo Frames folder: %FRAMES_DIR%
echo FPS: %FPS%
echo Width: %WIDTH%px
echo Method: OpenCV VideoWriter
echo.

REM Show preview
echo Frame preview:
python create_timelapse.py "%FRAMES_DIR%" --preview --fps %FPS%
echo.

REM Ask to continue
set /p answer=Do you want to create timelapse? (Y/N): 
if /i "%answer%" neq "Y" (
    echo Cancelled
    pause
    exit
)

REM Create timelapse
echo Creating timelapse...
python create_timelapse.py "%FRAMES_DIR%" --fps %FPS% --width %WIDTH%

echo.
echo Done!
pause 