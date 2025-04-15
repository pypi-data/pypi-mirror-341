# BoxManager
[![Python Package](https://github.com/rajatasusual/box-manager/actions/workflows/python-publish.yml/badge.svg)](https://github.com/rajatasusual/box-manager/actions/workflows/python-publish.yml)
[![PyPI version](https://badge.fury.io/py/box-manager.svg)](https://pypi.org/project/box-manager/)

BoxManager is a lightweight Python library for orchestrating systemd services and adjusting process priorities on Debian-based systems. Perfect for embedded systems, robotics, or any scenario where performance context switching is essential.

## Features
- ✅ Suspend/resume systemd services
- ✅ Deprioritize or prioritize running processes by keyword
- ✅ Automatically restore system state after execution
- ✅ YAML or JSON config support
- ✅ Decorator or imperative-style usage
- ✅ CLI for direct service and process control

---

## Installation
```bash
pip install box-manager
```

Or if developing locally:
```bash
git clone https://github.com/yourusername/box-manager.git
cd box-manager
pip install -e .
```

---

## Usage

### Basic Example
```python
from box_manager import BoxManager

manager = BoxManager()

@manager.with_orchestration(
    stop_services=["nginx"],
    deprioritize=["chrome"]
)
def critical_task():
    print("Doing performance-critical work...")

critical_task()
```

### Using Config File
```yaml
# config.yaml
orchestration:
  stop_services:
    - nginx
  start_services:
    - my_custom_service
  deprioritize:
    - chrome
  prioritize:
    - ros_node
```

```python
manager.load_config_and_orchestrate("config.yaml", func=my_task)
```

---

## CLI
Use the command line interface to quickly control services:

```bash
box-manager start nginx
box-manager stop nginx
box-manager status nginx
box-manager restart nginx
```

### Available Commands
- `start <service>`: Start a systemd service
- `stop <service>`: Stop a systemd service
- `status <service>`: Check if a service is active
- `restart <service>`: Restart a systemd service

---

## License
MIT License

---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## Author
Made with ☕ by [Rajat](mailto:rajatasusual@github.com)

