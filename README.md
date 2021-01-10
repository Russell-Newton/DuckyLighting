# DuckyLighting for Windows

![Built for Windows 10](https://img.shields.io/badge/Built%20for-Windows%2010-7fba00)
![Nearly Pure-Python 3](https://img.shields.io/badge/Python%203-100%25-blueviolet)
[![GPLv3 License](https://img.shields.io/github/license/Russell-Newton/DuckyLighting)](LICENSE) \
![Stars](https://img.shields.io/github/stars/Russell-Newton/DuckyLighting)
![Forks](https://img.shields.io/github/forks/Russell-Newton/DuckyLighting)
![Issues](https://img.shields.io/github/issues/Russell-Newton/DuckyLighting) \
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome!-55bb77)


Take control of your RGB Keyboard's lighting. Developed for the Ducky One2 RGB, expandable to others.

## Table of Contents

* [About](#about)
* [What Does it Look Like?](#what-does-it-look-like)
* [License](#license)
* [Download](#download)
* [Setup](#setup)
    * [Creating a Virtual Environment](#creating-a-virtual-environment)
    * [Installing Dependencies](#installing-dependencies)
* [Usage](#usage)
    * [Creating a Lighting Config](#creating-a-lighting-config)
    * [Running the Program](#running-the-program)
* [Expansion](#expansion)
    * [How to Determine Packet Protocols](#how-to-determine-packet-protocols)
* [Credits and Thanks](#credits-and-thanks)
* [Links](#links)

## About

DuckyLighting is a (nearly) Pure-Python 3.8 solution to the problem of [Ducky](https://www.duckychannel.com.tw)'s
RGBSeries software being lackluster at best. The software is useful but does not enable users to layer multiple effects.
Even the effects provided are limited.

When I think of keyboard RGB control, I think of [Razer Synapse 3](https://www.razer.com/synapse-3). Obviously, the
customization controls in Synapse only work for Razer RGB products, so my goal with this project was to get as close to
the effect options available in Synapse as I could.

Certain effects, like reactive ripples, are still in the works. That being said, Python makes development incredibly
easy for things like this. You just have to get creative.

DuckyLighting started as a fork of [Latedi's DuckyAPI](https://github.com/Latedi/DuckyAPI), which uses a C++ named pipe
API to communicate to a Scandinavian Ducky Shine 7, using instructions sent from a Python program. I made several
changes to the C++ API and overhauled the Python scripts. I moved the API into Python for easier changing, and
DuckyLighting was born. My goal was to create room for expansion to other keyboards and protocols, like the one for the
Shine 7.

## What Does it Look Like?

DuckyLighting doesn't have any fancy UI (yet), but I tried to make creating lighting configurations as easy as possible.
Setting up and running your own instance of the `DuckyOne2RGB` class can be done in only a few lines of code.

**Disclaimer: Please understand that this code is provided with no liability or warranty. This code could brick your
keyboard or expose your computer to security vulnerabilities. Only use code that you understand.**

***Use at your own risk!***

```python
from frontend.ducky import DuckyOne2RGB
from backend.utils import Color
from frontend.lighting.lightingschemes import SolidColorScheme
import configs.config as config


class MyConfig(config.Config):
    @config.layer()
    def solid_blue(self):
        """
        Creates a solid blue keyboard.
        """
        return SolidColorScheme(Color(0, 0, 255))


if __name__ == '__main__':
    my_ducky = DuckyOne2RGB()
    my_ducky.set_config(MyConfig())
    my_ducky.run()
```

An example Config is also provided in [flamestarlightbluepress.py](configs/flamestarlightbluepress.py). This
configuration creates a flame effect, a blue reactive effect, and a purple starlight effect (only on the function keys
and spacebar).

## License

DuckyLighting is provided under the GNU General Public License, version 3.0. DuckyLighting is packaged
with [HIDAPI](https://github.com/libusb/hidapi) binaries (under the terms of its GPL) and a modified version of
the [python-easyhid](https://github.com/ahtn/python-easyhid) library (under the terms of its MIT License).

This project is not intended to infringe on any existing licenses, trademarks, copyrights, etc. If this is found to be
the case, please contact me.

## Download

DuckyLighting can be downloaded from GitHub

```shell
git clone https://github.com/Russell-Newton/DuckyLighting.git
```

## Setup

### Creating a Virtual Environment

I recommend creating a unique virtual environment for your copy of this project. I personally
use [Anaconda](https://www.anaconda.com) to manage such environments. I used Python 3.8 to create this code, but it
should work for Python 3.6 (and potentially older versions of Python 3).

### Installing Dependencies

Most of the requirements can be installed with `pip`, but PyAudio (if you wish to use
a [Spectrogram Scheme](frontend/lighting/spectrogenerator.py)) has to be installed with another tool like `pipwin`. An
easy way to make sure you get all the dependencies correct is to run the following commands in a terminal.

```shell
pip install pipwin
pip install numpy
pip install keyboard
pip install noise
pip install cffi
pipwin install pyaudio
```

This set of commands has worked for me.

## Usage

### Creating a Lighting Config

`temporary filler, I would rather have this be through a Wiki`

### Running the Program

`temporary filler, I would rather have this be through a Wiki`

## Expansion

The packet protocol/setup that gives instructions to the Ducky One2 RGB can be modified for and expanded to other
keyboards, assuming their key colors can be set through instruction packets. It's also possible that this project could
be expanded to Linux, but that is beyond my knowledge and skill set.

Additionally, I tried to make it as simple as possible to create new LightingSchemes and ColorFunctions. Making new ones
just takes some creativity and overriding.

### How to Determine Packet Protocols

If there is a computer software that can tell a keyboard how to be colored, the protocols can be determined with a tool
such as [WireShark](https://www.wireshark.org) and [USBPcap](https://desowin.org/usbpcap/).

I used these tools to determine the packet structure for the color data packets by observing consistencies between
recurring packets. The protocol that I used was the one that the DuckyRGBSeries software uses when connected to Razer
Synapse with Razer Chroma Broadcast. I figured out that this connection sends over 8 packets, each containing some head
metadata followed by `r`, `g`, and `b` bytes corresponding to the various keys (and gaps between keys) on the keyboard.
Additionally, I used the opening and closing packets that [Latedi found](https://github.com/Latedi/DuckyAPI#how-to)
using these tools. These are required and tell the keyboard to listen for instructions over USB and then to stop
listening.

Similar analysis could be used to determine how to instruct other keyboards with different firmware how to light up.

## Credits and Thanks

| Name and Role | Links |
|:---:|:---:|
| ![Russell Newton](https://img.shields.io/badge/Russell%20Newton-Developer-7570ff) | [![Russell Newton GitHub](https://img.shields.io/badge/GitHub-707090)](https://github.com/Russell-Newton) [![Russell Newton LinkedIn](https://img.shields.io/badge/LinkedIn-707090)](https://www.linkedin.com/in/russellnewton01/) |

**And Special Thanks to:**

| Name and Reference | Links |
|:---:|:---:|
| [![DuckyAPI](https://img.shields.io/badge/Jonathan%20Schramm%20(Latedi)-DuckyAPI-violet)](https://github.com/Latedi/DuckyAPI) | [![Latedi Github](https://img.shields.io/badge/GitHub-707090)](https://github.com/Latedi) |
| [![libusb](https://img.shields.io/badge/libusb-hidapi-20bf00)](https://github.com/libusb/hidapi) | [![Latedi Github](https://img.shields.io/badge/GitHub-707090)](https://github.com/libusb) [![Latedi Github](https://img.shields.io/badge/Website-707090)](https://libusb.info)
| [![python-easyhid](https://img.shields.io/badge/ahtn-easyhid-df9f00)](https://github.com/ahtn/python-easyhid) | [![Latedi Github](https://img.shields.io/badge/GitHub-707090)](https://github.com/ahtn)|
## Links

In case none of the hyperlinks above work,

| Hyperlink Name  | Link |
|:----------:|------|
| Ducky | https://www.duckychannel.com.tw |
| Razer Synapse 3 | https://www.razer.com/synapse-3 |
| Latedi's DuckyAPI | https://github.com/Latedi/DuckyAPI |
| flamestarlightbluepress.py | https://www.github.com/Russell-Newton/DuckyLighting/blob/main/configs/flamestarlightbluepress.py |
| HIDAPI | https://github.com/libusb/hidapi |
| python-easyhid | https://github.com/ahtn/python-easyhid |
| Anaconda | https://www.anaconda.com |
| Spectrogram Scheme | https://www.github.com/Russell-Newton/DuckyLighting/blob/main/frontend/lighting/spectrogenerator.py |
| WireShark | https://www.wireshark.org |
| USBPcap | https://desowin.org/usbpcap/ |
| Latedi found | https://github.com/Latedi/DuckyAPI#how-to |
