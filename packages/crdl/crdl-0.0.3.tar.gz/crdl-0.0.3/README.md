# Crunchy-Downloader

A Python application for downloading content from Crunchyroll with proper authentication and stream management.

## Features

- **Robust Token Management**: Automatically handles access token expiration with proper refresh
- **Stream Cleanup**: Ensures all streams are properly deleted when program exits
- **Content Selection**: Download specific episodes, seasons, or browse series
- **Quality Options**: Select between different quality options
- **Output Customization**: Configure output directory and naming conventions
- **Credential Storage**: Save your credentials securely for future use
- **Cross-Platform Support**: Works on Windows, macOS, and Linux with standardized configuration paths

## Requirements

- Python 3.6+
- N_m3u8DL-RE (must be in your PATH)
- ffmpeg (must be in PATH)
- mkvmerge (must be in PATH)
- mp4decrypt (must be in PATH)
- Valid Crunchyroll account credentials
- Widevine CDM for DRM content (placed in `~/.config/crdl/widevine/device.wvd`)

## Installation

There are three ways to install the Crunchy-Downloader:

### Method 1: Install using pip

The simplest way to install Crunchy-Downloader is using pip:

```bash
pip install crdl
```

### Method 2: Clone and Install as Package

1. Clone the repository:
```bash
git clone https://github.com/username/Crunchy-Downloader.git
cd Crunchy-Downloader
```

2. Install using pip:
```bash
pip install -e .
```

This will install the package in development mode, making the `crdl` command available globally.

## Usage

You can use Crunchy-Downloader either as a script or as an installed package.

### Using as an Installed Package

If you installed the package using Method 1 above, you can use the `crdl` command from anywhere:

```bash
# First time setup with credentials
crdl --username YOUR_USERNAME --password YOUR_PASSWORD --episode EPISODE_ID

# Subsequent usage
crdl --episode EPISODE_ID
crdl --series SERIES_ID
```

### Using as a Script

If you installed using Method 2, you can run the script directly:

#### First-Time Usage

The first time you run the application, you'll need to provide your Crunchyroll credentials:

```bash
python a.py --username YOUR_USERNAME --password YOUR_PASSWORD --episode EPISODE_ID
```

These credentials will be saved securely in `~/.config/crdl/credentials.json` for future use.

#### Subsequent Usage

After first use, you can simply run without providing credentials:

```bash
python a.py --episode EPISODE_ID
```

### Advanced Options

Both the installed command and the script accept the same options:

```bash
python a.py --series SERIES_ID
# or
crdl --series SERIES_ID
```

This will display all seasons for the series and allow you to select which season or episode to download.

### Command Line Arguments

- `--username`, `-u`: Crunchyroll username
- `--password`, `-p`: Crunchyroll password
- `--series`, `-s`: Series ID to browse
- `--season`: Season ID to download all episodes from
- `--episode`, `-e`: Specific episode ID to download
- `--locale`: Content locale (default: en-US)
- `--audio`, `-a`: Audio languages to download (comma-separated, e.g., "ja-JP,en-US" or "all")
- `--output`, `-o`: Custom output directory
- `--verbose`, `-v`: Enable verbose logging
- `--quality`, `-q`: Video quality (1080p, 720p, best, or worst)
- `--release-group`, `-r`: Release group name for filename

## Configuration Directory Structure

The application uses the following directory structure in your home directory:

```
~/.config/crdl/
  ├── credentials.json    # Saved Crunchyroll credentials
  ├── json/               # API responses and debug information
  ├── widevine/           # Widevine CDM files
  │   └── device.wvd      # Only one device file is required
  └── logs/               # Log files
      └── crunchyroll_downloader.log
```

## Technical Details

### Stream Management

The application employs a robust strategy for managing streams:

- **Token Refresh**: Automatically refreshes access tokens when they expire
- **Stream Tracking**: Tracks all active streams to ensure proper cleanup
- **Signal Handling**: Properly handles interruption signals (SIGINT, SIGTERM)
- **Exit Cleanup**: Uses atexit to ensure cleanup even during normal exits

This avoids the "TOO_MANY_ACTIVE_STREAMS" error that can occur when streams aren't properly deleted.

### Token Management

The application implements sophisticated token management:

- **Token Expiry Tracking**: Tracks when access tokens will expire
- **Proactive Refresh**: Refreshes tokens before they expire (60 seconds buffer)
- **Refresh Token Usage**: Uses refresh tokens for more efficient renewal
- **Rate Limiting**: Prevents too-frequent token refresh attempts

### Credential Storage

Credentials are securely stored in a JSON file in your user's home directory:

- First login saves credentials for future use
- You only need to enter your username and password once
- Works across platforms with standardized paths
- Delete `~/.config/crdl/credentials.json` to reset saved credentials

## DRM Content

For DRM-protected content, the application requires a valid Widevine CDM:

1. Place your Widevine `device.wvd` file in the `~/.config/crdl/widevine/` directory
2. Only a single device file is required
3. Make sure it's named `device.wvd`

## Troubleshooting

If you encounter issues:

1. Check that your credentials are correct
2. Ensure you have the latest N_m3u8DL-RE installed
3. Try with the `--verbose` flag to see more detailed logs
4. Make sure you're using a premium Crunchyroll account
5. Check the log file at `~/.config/crdl/logs/crunchyroll_downloader.log`
6. Verify that your Widevine CDM is correctly placed at `~/.config/crdl/widevine/device.wvd`

## License

This project is for educational purposes only. Always respect Crunchyroll's terms of service.

## Contributors

- Original author: TanmoyTheBoT 