# py-nvfan

py-nvfan is a Python application designed to monitor and control NVIDIA GPU fan speeds on Linux systems. It provides a command-line interface to adjust fan profiles, monitor GPU temperatures, and automate cooling based on user-defined thresholds.

## Features
- Monitor NVIDIA GPU temperatures and fan speeds
- Set custom fan speed profiles
- Automatic fan control based on temperature
- Command-line interface for easy usage
- Logging and status reporting

## Requirements
- Python 3.12+
- NVIDIA GPU with supported drivers
- Linux x86_64 operating system
- [nvidia-smi](https://developer.nvidia.com/nvidia-system-management-interface) installed and available in **PATH**
- [nvidia-settings](https://www.nvidia.com/en-us/) installed and available in **PATH**
- [pip](https://pypi.org/project/pip/) for project management or use the **pip**.

## Installation
1. Create activate a python virtual environment:
   ```bash
   cd any-directory
   python -m venv .venv # if you use pip
   ```
2. Activate the python virtual environment:
   ```bash
   source .venv/bin/activate.fish # if you use fish
   source .venv/bin/activate # if you use bash or zsh
   ```   
3. Install py-nvfan
   ```bash
   pip install py-nvfan
   ```   

## Usage

Run the application from the command line:

```bash
py-nvfan [OPTIONS]
```


## Options
- `-c`, `--config <path>`: Path to the config file (default: config.yaml)
- `-v`, `--version`: Show the version and exit

### Examples

Show the help:
```bash
py-nvfan --help
```

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

## Config File
By default, **py-nvfan** will create the ***config.yaml*** file (configuration file) in the directory
***/home/your-username/.config/py-nvfan/***

If you want to use a different configuration file, use the --config option

For example:
```bash
py-nvfan --config /path/to/another/dir/config.yaml
```

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer
Use this tool at your own risk. Improper fan control may cause hardware damage. Always monitor your GPU temperatures and ensure adequate cooling.
