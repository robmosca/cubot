# cubot

_A LEGO® MINDSTORMS® Rubik's cube solver with the Robot Inventor set, based on
[MindCuber](http://mindcuber.com)_

This is my attempt at a LEGO® MINDSTORMS® Rubik's cube solver, created with the
Robot Inventor set (plus a few spare parts and a Raspberry Pi 4B). The robot
itself is inspired on [MindCuber](http://mindcuber.com), by David Gilday. This
particular robot was built mainly by following the instructions I obtained
following the links in [this other YouTube video](https://youtu.be/s2HexyswxKY).
I modified the original instructions to replace the color sensor with a
Raspberry Pi 4B + CamV2 Module.

By clicking on the image, you can see the [Robot in action](https://youtu.be/T-D1KVIuvjA):

[![Watch the video](https://img.youtube.com/vi/K98Nth4gAg8/maxresdefault.jpg)](https://youtu.be/T-D1KVIuvjA)

In this repository you can find the code I used, both on the LEGO Hub
(`cubot.py`) and on the Raspberry Pi (`picube.py` and `cube.py`). The software
is customized on the specific cube I used (GAN Monster GO Magnetic).

To load the micropython module on the LEGO Hub I used VS Code with the
[LEGO® MINDSTORMS® Robot Inventor extension](https://github.com/robmosca/robotinventor-vscode) I wrote.
