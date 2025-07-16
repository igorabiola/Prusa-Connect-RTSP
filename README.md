# Prusa Connect RTSP Proxy

A Python-based proxy that captures frames from RTSP cameras and forwards them to Prusa Connect webcam service. Features automatic timelapse creation and optimized connection handling.

## Features

- ✅ **RTSP Camera Support**: Connects to any RTSP-compatible camera
- 🔄 **Optimized Connection Handling**: New HTTP session and camera connection for each frame
- 🎬 **Automatic Timelapse Creation**: Creates MP4 timelapses from captured frames
- 📊 **Configurable Upload Intervals**: Adjustable frame upload frequency
- 🧹 **Automatic Cleanup**: Removes old frames to prevent disk space issues
- 📝 **Detailed Logging**: Comprehensive status reporting and error handling
- 🔧 **Environment Configuration**: Easy setup via environment variables

## Requirements

- Python 3.7 or higher
- OpenCV (opencv-python)
- requests library
- numpy (version < 2.0)

## Installation

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
+ gather your Fingerprint and Token as show in this Git repository from @JohnyHV
https://github.com/johnyHV/PrusaConnect_Camera?tab=readme-ov-file#here-is-a-manual-on-how-to-get-fingerprint-token-id-and-configure-script

## Configuration

### Environment Variables

Configure the proxy using these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `TOKEN` | `YOUR TOKEN HERE` | Your Prusa Connect token |
| `FINGERPRINT` | `YOUR HEX1 FINGERPRINT HERE` | Your printer fingerprint |
| `RTSP_URL` | *Required* | RTSP camera URL (e.g., `rtsp://user:pass@192.168.1.100/stream1`) |
| `UPLOAD_INTERVAL` | `5` | Upload interval in seconds |
| `ENABLE_TIMELAPSE` | `false` | Enable timelapse creation (`true`/`false`) |
| `TIMELAPSE_SAVE_INTERVAL` | `30` | Save frame for timelapse every X seconds |
| `TIMELAPSE_DIR` | `timelapse_frames` | Directory for timelapse frames |
| `TIMELAPSE_FPS` | `24` | Frames per second for timelapse video |

### Getting Prusa Connect Credentials

1. **Visit Prusa Connect**: Go to [connect.prusa3d.com](https://connect.prusa3d.com)
2. **Add your printer** to your account
3. **Get the token and fingerprint**:
   - Go to your printer settings
   - Navigate to the webcam section
   - Copy the token and fingerprint values

### RTSP Camera URL Format

The RTSP URL format depends on your camera model:

```
rtsp://[username:password@]host[:port]/[path]
```

**Examples:**
- `rtsp://admin:password@192.168.1.100/stream1`
- `rtsp://192.168.1.100:554/h264_stream`
- `rtsp://user:pass@camera.local/live/main`

## Usage

### Method 1: Using Batch Files (Windows)

1. **Edit configuration** in `run_prusa_proxy.bat`:
   - Set your `TOKEN` and `FINGERPRINT`
   - Set your `RTSP_URL`
   - Adjust other settings as needed

2. **Run the proxy**:
   ```cmd
   run_prusa_proxy.bat
   ```

3. **Create timelapse** (if enabled):
   ```cmd
   create_timelapse.bat
   ```

### Method 2: Using Environment Variables

1. **Set environment variables**:
   ```bash
   # Windows
   set TOKEN=your_token_here
   set FINGERPRINT=your_fingerprint_here
   set RTSP_URL=rtsp://user:pass@192.168.1.100/stream1
   set ENABLE_TIMELAPSE=true
   
   # Linux/Mac
   export TOKEN=your_token_here
   export FINGERPRINT=your_fingerprint_here
   export RTSP_URL=rtsp://user:pass@192.168.1.100/stream1
   export ENABLE_TIMELAPSE=true
   ```

2. **Run the proxy**:
   ```bash
   python main.py
   ```

### Method 3: Direct Python Execution

```bash
python main.py
```

Make sure to set the required environment variables first.

## Timelapse Creation

### Automatic Timelapse

When `ENABLE_TIMELAPSE=true`, the proxy will:
- Save frames at intervals defined by `TIMELAPSE_SAVE_INTERVAL`
- Store frames in the `TIMELAPSE_DIR` folder
- Create a timelapse video when you stop the proxy (Ctrl+C)

### Manual Timelapse Creation

Create timelapses from existing frames:

```bash
# Basic usage
python create_timelapse.py timelapse_frames

# Custom output and settings
python create_timelapse.py timelapse_frames -o my_timelapse.mp4 -f 30 -w 1920

# Preview mode (show info without creating video)
python create_timelapse.py timelapse_frames --preview
```

**Command line options:**
- `-o, --output`: Output filename
- `-f, --fps`: Frames per second (default: 24)
- `-w, --width`: Width to resize to
- `--preview`: Show information without creating video

## Troubleshooting

### Common Issues

1. **"Cannot connect to RTSP camera"**
   - Verify the RTSP URL is correct
   - Check camera credentials
   - Ensure the camera is accessible from your network

2. **"Rate limit exceeded"**
   - Increase the `UPLOAD_INTERVAL` value
   - Prusa Connect has rate limits for uploads

3. **"Video file was not created"**
   - Install OpenCV with video codec support
   - Try different output formats (MP4, AVI)

4. **Authentication errors (401)**
   - Verify your token and fingerprint are correct
   - Check if they're properly set in environment variables

### Camera Compatibility

The proxy works with most RTSP cameras, including:
- IP cameras (Hikvision, Dahua, etc.)
- USB cameras with RTSP firmware
- Network video recorders (NVR)
- Smartphone camera apps with RTSP support

### Performance Tips

- **Reduce upload interval**: Lower values = more frequent uploads but higher bandwidth usage
- **Adjust timelapse interval**: Higher values = fewer frames but smaller file sizes
- **Frame cleanup**: The proxy automatically removes old frames to prevent disk space issues

## File Structure

```
prusa-connect-rtsp-proxy-english/
├── main.py                 # Main proxy script
├── create_timelapse.py     # Timelapse creation script
├── run_prusa_proxy.bat     # Windows batch file for easy startup
├── create_timelapse.bat    # Windows batch file for timelapse creation
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── timelapse_frames/      # Directory for timelapse frames (created automatically)
```

## Technical Details

### Connection Handling

The proxy uses optimized connection handling:
- **New HTTP session** for each frame upload (fixes PrusaConnect issues)
- **New camera connection** for each frame (ensures fresh frames)
- **Connection pooling disabled** to prevent connection reuse issues

### Frame Processing

- Frames are captured using OpenCV
- JPEG encoding for web upload
- Automatic frame resizing for timelapse
- Buffer management for fresh frames

### Error Handling

- Comprehensive error reporting
- Automatic retry on connection failures
- Graceful handling of camera disconnections
- Rate limit detection and handling

## License

This project is provided as-is for educational and personal use. Please respect camera privacy and network policies when using this software.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this proxy.

---

**Happy printing with Prusa Connect! 🖨️** 
