# py-nvfan

py-nvfan is a Python application designed to monitor and control NVIDIA GPU fan speeds on Linux systems. It provides a command-line interface to adjust fan profiles, monitor GPU temperatures, and automate cooling based on user-defined thresholds.

## Features
- Monitor NVIDIA GPU temperatures and fan speeds
- Set custom fan speed profiles
- Automatic fan control based on temperature
- Command-line interface for easy usage
- Logging and status reporting

## Requirements
- Python 3.13+
- NVIDIA GPU with supported drivers
- Linux x86_64 operating system
- [nvidia-smi](https://developer.nvidia.com/nvidia-system-management-interface) installed and available in **PATH**
- [nvidia-settings](https://www.nvidia.com/en-us/) installed and available in **PATH**
- [UV](https://github.com/astral-sh/uv) for project management or use the OLD pip.

## Installation
1. Create activate a python virtual environment:
   ```bash
   uv venv --python 3.14
   ```
2. Activate the python virtual environment:
   ```bash
   source .venv/bin/activate.fish # if you use fish
   source .venv/bin/activate # if you use bash or zsh
   ```   

## Usage

Run the application from the command line:

```bash
py-nvfan [OPTIONS]
```

### Options
- `-c`, `--config <path>`: Path to the config file (default: config.yaml)
- `-v`, `--version`: Show the version and exit

### Examples
Run with default configuration:
```bash
py-nvfan
```

Specify a custom configuration file:
```bash
py-nvfan --config /path/to/config.yaml
```

Show version information:
```bash
py-nvfan --version
```

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer
Use this tool at your own risk. Improper fan control may cause hardware damage. Always monitor your GPU temperatures and ensure adequate cooling.
