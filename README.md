# Implementing and visualizing slime mold algorithm

This tool allows you to draw your own maze, specify start and end points, and simulate the slime mold algorithm.

```
usage: SlimeMold.py [-h] [--custom | --example] [--videoname VIDEONAME] [--framerate FRAMERATE] [--rounds ROUNDS]

Simulate slime mold behavior in a maze. Creates MP4 video of simulation. If video creation does not work, you can
still see the frames in the images/ folder. For best results , make sure there is an actual path from source to sink!

optional arguments:
  -h, --help            show this help message and exit
  --custom              Allows you to draw a custom maze
  --example             Use the example (approximate) Nakagaki maze instead of making your own
  --videoname VIDEONAME
                        Specify filename to save simulation video as (.mp4 file).
  --framerate FRAMERATE
                        Framerate of video in frames/second
  --rounds ROUNDS       Number of time steps to simulate
  
  ```

### Python Dependencies
* Python 3.9 (probably works with lower versions of Python3 but haven't tested)
* pip : https://pip.pypa.io/en/stable/installing/
* tkinter : ``` pip install tk ```
* networkx : ``` pip install networkx ```
### System Dependencies
* ffmpeg : https://ffmpeg.org/download.html

### Notes
* Examples of GUI, terminal messages, start/end maze images, and animation video is available in ```examples/``` directory
* To create the mp4, ffmpeg needs to be installed on your system and added to system PATH, so the python script can run it
* If ffmpeg is not installed, you can still find the images of the algorithm's time steps in the images/ folder
* Default framerate of video is 1 frame / second. If you find this too slow, feel free to change it!
* Please pay attention to the terminal when the GUI pops up for custom maze drawing
* Only tested on Windows
* References provided in the PDF writeup
