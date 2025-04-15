# Netflix Open Content Helper

A command-line utility for downloading test frames from [Netflix Open Content](https://opencontent.netflix.com).

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/netflix-open-content-helper)]((https://pypi.org/project/netflix-open-content-helper/)
) [![Build Status](https://github.com/jdmacleod/netflix-open-content-helper/actions/workflows/python-package.yml/badge.svg)](https://github.com/jdmacleod/netflix-open-content-helper/actions/workflows/python-package.yml)
[![Documentation](https://img.shields.io/badge/doc-latest-blue.svg)](https://jdmacleod.github.io/netflix-open-content-helper/) [![PyPI - Version](https://img.shields.io/pypi/v/netflix-open-content-helper)](https://pypi.org/project/netflix-open-content-helper/)

[![GitHub License](https://img.shields.io/github/license/jdmacleod/netflix-open-content-helper)](https://github.com/jdmacleod/netflix-open-content-helper/blob/main/LICENSE)
[![Tests Status](./reports/junit/tests-badge.svg?dummy=8484744)](./reports/junit/report.html)
[![Coverage Status](./reports/coverage/coverage-badge.svg?dummy=8484744)](./reports/coverage/index.html)
[![codecov](https://codecov.io/gh/jdmacleod/netflix-open-content-helper/branch/main/graph/badge.svg)](https://codecov.io/gh/jdmacleod/netflix-open-content-helper)

## Prerequisites

You will need the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) installed and available in `$PATH` to download frame content. No AWS account is needed however, as we use `-no-sign-request` when downloading files.

## Quickstart

Install using [pip](https://pypi.org/project/pip/) or [pipx](https://pipx.pypa.io/stable/).

```bash
$ pip install netflix-open-content-helper
```

or

```bash
$ pipx install netflix-open-content-helper
```

This will provide the command-line utility `noc`.

### Using `noc` with Netflix Open Content

Download the first frame of [Sparks](https://opencontent.netflix.com/#h.d0oh6u8prqhe) to the current directory.

```bash
$ noc download sparks
Downloading: sparks frames 1-1
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:11
```

List the available Netflix Open Content Assets with frame content.

```bash
$ noc list
Available content with frames:
- chimera             : Live action footage, 4K. Download configured for the 23.98fps frame rate version. TIFF files.
- cosmoslaundromat    : Animated short film done in Blender, 2K 24p. EXR files.
- meridian            : Live action noir UHD short, 59.94fps. Mastered in Dolby Vision HDR. TIFF files.
- sparks              : Live action 4K HDR test short, 59.94fps, finished at 4000 nits. ACES EXR files.
```

Open a new web browser window to the [Netflix Open Content URL](https://opencontent.netflix.com).

```bash
$ noc browse
... (web browser opens)
```

## Examples

See [examples.md](./examples.md) for more examples.

## Changes

See the product [Change Log](https://github.com/jdmacleod/netflix-open-content-helper/blob/main/CHANGELOG.md) on GitHub for a history of changes.

## Problems?

Please submit [issues](https://github.com/jdmacleod/netflix-open-content-helper/issues) on GitHub.

## Want to contribute?

Details on the GitHub page: [https://github.com/jdmacleod/netflix-open-content-helper](https://github.com/jdmacleod/netflix-open-content-helper).
