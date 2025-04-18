# py_volume_watcher

`py_volume_watcher` is a lightweight Python library that lets you monitor a folder or volume (e.g., a mounted Docker volume) for new or changed files — **only after they are fully written and stable**.

This is especially useful in containerized environments, where file updates might be streamed or take time to finish. Instead of reacting to partial file writes, `py_volume_watcher` waits until the file's content hash (`sha256`) stops changing before emitting an event.

---

## 🔧 Features

- Detects new or modified files
- Ignores unchanged files
- Polling-based (no inotify), so it works across platforms (including Docker volumes)
- Waits for file stability before triggering an event
- Safe shutdown with context manager or manual control

---

## 📦 Installation

```bash
pip install py_volume_watcher
```

> _(You can also copy the code directly if it's not published on PyPI yet.)_

---

## 🐍 Requirements

- **Python 3.9+**  
  The code uses modern typing features like `str | Path` and `Queue[Path]`, which require Python 3.9 or newer.

- **No external dependencies**  
  `py_volume_watcher` relies only on the Python standard library:
  - `hashlib`
  - `pathlib`
  - `logging`
  - `threading`
  - `queue`
  - `time`

This makes it lightweight and portable — perfect for containerized or minimal environments.

## 🧠 How it Works

Every `polling_interval_sec` (default: `0.5s`), the watcher:

- Scans the directory using a glob pattern (e.g., `*.json`)
- Computes the SHA256 hash of each file
- If a new file appears or its hash changes, it's added to the event queue
- You can consume these events using a simple iterator interface

---

## ✅ Recommended Usage (Context Manager)

```python
from py_volume_watcher import FileWatcher

with FileWatcher("/path/to/volume", pattern="*.json") as watcher:
    for file in watcher:
        print(f"Detected stable file: {file}")
        # You can break safely; the thread will stop properly
        if file.name == "stop.json":
            break
```

- ✅ Thread starts automatically on `__enter__()`
- ✅ Thread stops gracefully on `__exit__()` — even on `Ctrl+C`, `break`, or exceptions

---

## ❌ Incorrect Usage (Without Context Manager)

```python
watcher = FileWatcher("/path/to/volume", pattern="*.json")

for file in watcher:
    print(file)
    break  # ❌ This breaks the loop but leaves the thread running in background
```

If you must manage lifecycle manually, call `__enter__()` and `__exit__()` yourself:

```python
watcher = FileWatcher("/path/to/volume", pattern="*.json")
watcher.__enter__()

try:
    for file in watcher:
        print(file)
        break
finally:
    watcher.__exit__(None, None, None)
```

---

## 📂 Typical Use Case in Docker

Mount a volume and use the watcher to wait for "complete" files:

```bash
docker run -v $(pwd)/input:/data your-image
```

In Python:

```python
from py_volume_watcher import FileWatcher

with FileWatcher("/data", pattern="*.csv") as watcher:
    for file in watcher:
        print(f"✅ Ready to process: {file}")
```

This avoids processing files that are still being copied into the container.

---

## ⚙️ Parameters

| Parameter              | Type           | Default    | Description                         |
| ---------------------- | -------------- | ---------- | ----------------------------------- |
| `base`                 | `str \| Path`  | _required_ | Directory to watch                  |
| `pattern`              | `str`          | `"*"`      | Glob pattern to match files         |
| `polling_interval_sec` | `float \| int` | `0.5`      | Interval in seconds between scans   |
| `on_exit_timeout`      | `float \| int` | `1.0`      | Max time to wait for thread to join |

---

## 📄 License

MIT License — free to use and modify.

---

## 🧪 Tips

- Use longer polling intervals if files are large or written slowly.
- Combine with file naming conventions (e.g., temp + rename) for extra safety.
- Logging is available via the `py_volume_watcher` logger.

---

Happy watching! 🔍
