# blame-g

[![PyPI Version](https://img.shields.io/pypi/v/blame-g)](https://pypi.org/project/blame-g/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/blame-g)](https://pypi.org/project/blame-g/)

`blame-g` is a command-line tool that analyzes git repositories and generates contributor statistics — including commits, lines added/deleted, files changed, pull requests, reverts, and more — beautifully rendered in a terminal table.

**Geddit?** Blame- *ji*? ;)

![in-action](https://raw.githubusercontent.com/mcking-07/blame-g/refs/heads/main/assets/blame-g.png)

## Features

- **Contributor Statistics:**  Aggregates commits, lines added/deleted, files changed, pull requests, and reverts for each contributor.
- **Rich Output:** Uses the `rich` library to provide a visually appealing and informative table of statistics in your terminal.
- **Branch Specific Analysis:**  Analyze a specific branch of your repository.
- **Pull Request & Revert Detection:** Detects PRs and reverts based on commit message patterns.
  > **Note:** The detection only works if you use the default PR message patterns for Bitbucket, GitHub, and GitLab. Custom commit message formats might not be recognized.
- **Git-Aware Context:** Automatically detects and works within the current Git repository.

## Installation

### Install from PyPI

```sh
pip3 install blame-g
```

### Clone and Run from Source

```sh
git clone https://github.com/mcking-07/blame-g.git
cd blame-g

pip3 install -r requirements.txt
python3 blame-g [repo_path] [branch_name]
```

### Editable Install

```sh
git clone https://github.com/mcking-07/blame-g.git
cd blame-g

pip3 install -e .
blame-g [repo_path] [branch_name]
```

## Usage

```sh
blame-g [repo_path](defaults to the current working directory) [branch_name](defaults to main or master)
```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
