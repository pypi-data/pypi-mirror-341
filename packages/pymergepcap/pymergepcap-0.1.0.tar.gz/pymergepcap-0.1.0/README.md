# pymergepcap

A simple Python GUI tool to generate mergecap commands for merging multiple PCAP or CAP files using Wireshark's `mergecap.exe`.

---

![Screenshot](screenshot.png)

---

## Features

- **Easy GUI**: Built with PySimpleGUI for a user-friendly experience.
- **Configurable**: Set and update the path to `mergecap.exe` via the GUI.
- **Flexible Input**: Select a folder containing `.cap` or `.pcap` files to merge.
- **Output Selection**: Choose your target merged PCAP file.
- **Command Generation**: Generates the full Windows command for `mergecap.exe` with all paths properly quoted.
- **No Execution**: For safety, the tool only generates the command; you run it manually in your terminal.
- **Cross-Platform Python**: Works with Python 3.12+ on Windows.

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/fxyzbtc/pymergepcap.git
   cd pymergepcap
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   # or, if using PEP 621/pyproject.toml
   pip install .
   ```

## Usage

### GUI

- Run with Python:

- Or as a module:
  ```sh
  python -m pymergecap
  ```
- Or as a CLI script (if installed):
  ```sh
  pymergecap
  ```

### Steps

1. Set the path to your `mergecap.exe` (from Wireshark) in the GUI or via `config.ini`.
2. Select the folder containing your `.cap` or `.pcap` files.
3. Choose the output file path.
4. Click **Merge** to generate the command.
5. Copy and run the generated command in your Windows Command Prompt.

---

## Configuration

- The path to `mergecap.exe` is stored in `config.ini` under `[DEFAULT] MergecapPath`.
- You can update this path anytime using the **Change Mergecap** button in the GUI.

---

## Example Command

```
"C:/Program Files/Wireshark/mergecap.exe" -w "D:/py/pymergepcap/merged.cap" "D:/py/pymergepcap/test1.cap" "D:/py/pymergepcap/test2.cap"
```

---

## Screenshot

![GUI Screenshot](screenshot.png)

---

## License

MIT License

---

## Credits

- [Wireshark](https://www.wireshark.org/) for `mergecap.exe`
- [PySimpleGUI](https://pysimplegui.readthedocs.io/)
- [loguru](https://github.com/Delgan/loguru)

---

*Happy merging!*
