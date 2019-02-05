CC = g++
LD = g++
CPPFLAGS = -std=c++11 -g -Wall -pedantic
LDFLAGS =

all: sorter fileio list convexhull line

list:
	$(CC) $(CPPFLAGS) linked_list.cpp -o linked_list

sorter: sorter.cpp fileio.cpp sorter.hpp fileio.hpp
	$(CC) $(CPPFLAGS) fileio.cpp sorter.cpp -o sorter

fileio: testFileIO.cpp fileio.cpp fileio.hpp
	$(CC) $(CPPFLAGS) testFileIO.cpp fileio.cpp -o testFileIO

convexhull: ConvexHullApp.cpp ConvexHullApp.hpp HullAlgorithms.cpp structs.hpp HullAlgorithms.hpp
	$(CC) $(CPPFLAGS) `sdl-config --cflags` ConvexHullApp.cpp HullAlgorithms.cpp `sdl-config --libs` -lSDL_gfx -o ConvexHullApp

line: LineApp.cpp LineAlgorithm.cpp LineAlgorithm.hpp LineApp.hpp structs.hpp
	$(CC) $(CPPFLAGS) `sdl-config --cflags` LineAlgorithm.cpp LineApp.cpp `sdl-config --libs` -lSDL_gfx -o LineApp

testsort:
	python testsort.py

clean :
	rm -rf angleSort argcv sorter fileio linked_list ConvexHullApp LineApp testFileIO *.o *.dSYM out
