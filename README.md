# Screenshot to Text (S2T)

A crossplatform CLI utility to extract text from a screenshot. 

Run it, select an area on your screen and the text will be copied to your clipboard.

It relies on readily existing external tools for screenshotting, OCR, and clipboard management.

Built as a good enough solution until someone builds a cross platform super fast native rust application that does the same thing better :sweat_smile: 

## Status

![Ubuntu (X11)](https://img.shields.io/badge/Linux%20(X11)-passing-success) ![Ubuntu 15.04 (Wayland)](https://img.shields.io/badge/Linux%20(Wayland)-passing-success) ![macOS](https://img.shields.io/badge/macOS-passing-success)

<details>
<summary> Testing Details</summary>

| Platform | Tested On | Status
|-|-|-|
| Linux (X11)     | Native Ubuntu 24.04 (X11)      |![Status](https://img.shields.io/badge/passing-success) |
| Linux (Wayland) | Quickemu Ubuntu 25.04 (Wayland)|![Status](https://img.shields.io/badge/passing-success) |
| macOS | Quickemu macOS Sequoia         |![Status](https://img.shields.io/badge/passing-success) |

</details>

## Watch it in Action

![Demo](https://raw.githubusercontent.com/Alphan-Aksoyoglu/screenshot-to-text/d17bb4e974e6a2d5d069a38471703a21b6863fdb/media/screenshot-to-text-demo.gif)

## Dependencies

You will need to have one of the supported tools for each category installed on your system.

## Supported Platforms & Tools

| Platform        | Screenshot Tools                              | OCR        | Clipboard Tools           |
|-----------------|-----------------------------------------------|------------|---------------------------|
| Linux (X11)     | `flameshot`, `gnome-screenshot`               | `tesseract`| `xclip`                   |
| Linux (Wayland) | `flameshot`                                   | `tesseract`| `wl-copy`                 |
| macOS           | `flameshot`, `screencapture`                  | `tesseract`| `pbcopy`                  |

### Recommended Tool Installation

#### Linux (X11)

`sudo apt-get install gnome-screenshot tesseract-ocr xclip`

#### Linux (Wayland)

`sudo apt-get install flameshot tesseract-ocr wl-clipboard`

#### macOS

`brew install tesseract`



## Installation and Configuration (First Use)

We recommend installing with `pipx` or `uv`

```bash
pipx install screenshot-to-text
```

or

```bash
uv tool install screenshot-to-text
```

### Configuration

Before the first run, you need to configure the tool:

```bash
s2t config
```

This command will prompt you to select the tools you want to use for screenshotting, OCR, and clipboard operations from the available tools on your system. If your system is missing the necessary tools it will ask you to install them.

It will create a `config.toml` file in your user configuration directory.

## Usage

To take a screenshot and extract text to clipboard, run:

```bash
s2t run
```
It is recommended to attach `s2t run` to a hotkey for maximum convenience.

You can also use the alias `screenshot-to-text`.

The `run` command accepts the following options:
* `--keep-screenshot`: Overwrites the default config to keep the screenshot.
* `--no-keep-screenshot`: Overwrites the default config to not keep the screenshot.
* `--ocr-enabled`: Overwrites the default config to enable OCR.
* `--no-ocr-enabled`: Overwrites the default config to disable OCR.

## Supported Python Versions

Python versions `>=3.11` are supported.

## To-Do and Contribution Points

Contributions are welcome! Here are some areas where you can help:

-   **Add Windows Support:** The current implementation is focused on Linux and macOS. Adding support for Windows would be a great contribution. This would involve finding and integrating with Windows-native command-line tools for screenshots and clipboard management.
-   **Support More OS-Native Tools:** If you use a screenshot or clipboard tool that is not currently supported, feel free to open a pull request to add it.
-   **Add Support for AI OCR Libraries:** Currently, only Tesseract is supported for OCR. It would be great to add support for modern AI-based OCR libraries and services (e.g., Google's OCR, or local AI models).
-   **Improve Image Preprocessing:** The current image preprocessing is basic. You can contribute by improving the existing preprocessing steps or adding new ones to improve OCR accuracy. The preprocessing parameters could also be made configurable.
-   **Tweak Tesseract Parameters:** The parameters for Tesseract could be exposed in the configuration file to allow users to fine-tune them for their specific needs.
-   **Better CLI Flags and Flexibility:** Current CLI flags are not exactly useful implementations, these can be improved.  

Please open an issue or a pull request to discuss your ideas.
