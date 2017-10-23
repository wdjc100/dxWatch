# wtDxLite
Python program to notify of DX cluster spots.

Possible use cases include:
* Looking out for a specific DX station - instead of checking the cluster every few minutes, get on with other tasks and receive a notification when they are spotted
* Monitoring your own callsign in a contest or DXpedition - it can be useful to know when you have been spotted as increased activity usually follows (so it would be a bad time to get that extra coffee.) Not all logging software includes this or, in the case of a shared log, might be looking for the wrong callsign.

## Installation

### Windows

Install Python 3 [https://www.python.org/downloads/] *(Important - when prompted, ensure you also install 'pip')*

Install PyQT4:
* Download latest WHL file for your Python 3 version from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4
* Install using `pip3 install [filename].whl` from the command line

Install PyZMQ:
* Install using `pip3 install zmq` from the command line

### Linux

Install Python 3 & PyQT4
* `apt-get install python3 python3-pip python3-pyqt4`

Install PyZMQ:
* `pip3 install zmq`

## Usage
Start dxWatch.py from the command line or double-click. Optionally provide the callsign as the first argument -if not, you will be prompted for this on start.

## Why is the icon so terrible?
Not being much of a graphic designer, for my personal use I have taken an image from the internet that I liked and thought was suitable. However, this means I don't own it and so would be inappropriate to upload alongside the project. I have included a placeholder image (dx.png) which you can replace with a PNG file of your choice.

## Credits
Thanks are due to Michael G7VJR for the DXLite tool which this program uses. (http://dxlite.g7vjr.org/) 

More info on the Zero Message Queue: http://g7vjr.org/2013/09/dxlite-implemented-as-a-zero-message-queue-json/