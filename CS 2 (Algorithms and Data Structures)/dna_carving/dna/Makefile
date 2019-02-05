CC = g++
LD = g++
CFLAGS = -std=c++11 -Wall -pedantic -ggdb `sdl-config --cflags`
SDLLIBS = `sdl-config --libs`
SRCDIR = src
OBJDIR = obj
BINDIR = bin


align: align.o
	$(LD) -o $@ $^

%.o: %.cpp
	$(CC) -c $(CFLAGS) $< -o $@

clean:
	rm -f align.o align

