# Implementing and visualizing slime mold algorithm

This tool is a fun 

```
usage: SlimeMold.py [-h] [--custom | --example] [--videoname VIDEONAME] [--framerate FRAMERATE] [--rounds ROUNDS]

Simulate slime mold behavior in a maze. Creates MP4 video of simulation. If video creation does not work, you can
still see the frames in the images/ folder. For best results , make sure there is an actual path from source to sink!

optional arguments:
  -h, --help            show this help message and exit
  --custom              Allows you to draw a custom maze
  --example             Use the example takagaki maze instead of making your own
  --videoname VIDEONAME
                        Specify filename to save simulation video as (.mp4 file).
  --framerate FRAMERATE
                        Framerate of video in frames/second
  --rounds ROUNDS       Number of time steps to simulate
  
  ```

### Python Dependencies
* Python 3.9 (probably works with lower versions but haven't tested)
* tkinter
* networkx
### System Dependencies
* ffmpeg

### Notes
* To create the mp4, ffmpeg needs to be installed on your system and added to system PATH, so the python script can run it
* If ffmpeg is not installed, you can still find the images of the algorithm's time steps in the images/ folder
* Default framerate of video is 1 frame / second. If you find this too slow, feel free to change it!
* Please pay attention to the terminal when the GUI pops up for custom maze drawing
* Close the GUI when you are finished drawing your maze
* I did have it working with multiple sinks but found the results to be inconsistent, so I removed this feature the final version
* Only tested on Windows 10
