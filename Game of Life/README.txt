Game of Life v1.1:

This is a personal project of mine to play and visualize Conway's Game of Life.

This program is capable of playing the game of life with a randomly generated
initial board, and randomly generated colors with four theme options
(the default is entirely random). Additionally, this program allows you to
set your desktop wallpaper to be the game of life, updating with each
iteration.

One runs the program by typing:

$python3 gol.py [cool|warm|mono] [-w]

-w : Wallpaper mode

Features that will hopefully be added in the future:
- Reading initial board state from file (underway)
- Pre-programmed starting configurations
- Stopping and starting with a keypress
- Controls in window to change settings
- More intuitive size alterations
- Multithreaded buffering of desktops to rotate to ensure smooth transitions
  and speed in desktop switches, without overheating processor?
- Automatically rotating desktop backgrounds for Mac OS, so that your desktop
  can be the game of life. (working, but maybe improvements?)
