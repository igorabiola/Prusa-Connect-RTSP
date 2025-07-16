@echo off
REM Configure your Prusa Connect credentials here
set TOKEN=YOUR_TOKEN_HERE
set FINGERPRINT=YOUR_FINGERPRINT_HERE
set RTSP_URL=rtsp://username:password@192.168.1.100/stream1
set UPLOAD_INTERVAL=5

REM Timelapse configuration
set ENABLE_TIMELAPSE=true
set TIMELAPSE_SAVE_INTERVAL=30
set TIMELAPSE_DIR=timelapse_frames
set TIMELAPSE_FPS=24

echo Starting Prusa proxy...
echo Upload interval: %UPLOAD_INTERVAL% seconds
echo Timelapse: %ENABLE_TIMELAPSE% (every %TIMELAPSE_SAVE_INTERVAL%s, %TIMELAPSE_FPS% FPS)
echo Timelapse folder: %TIMELAPSE_DIR%
echo Using OpenCV for video creation
echo New HTTP session for each frame (PrusaConnect fix)
echo New camera connection for each frame (fresh frames fix)
echo.
echo Press Ctrl+C to stop and create timelapse
echo.
python main.py
pause 