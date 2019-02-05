#
# CS 11: Makefile for C track, assignment 5.
#

CC = gcc
CFLAGS = -g -Wall -Wstrict-prototypes -ansi -pedantic

all: one_d_life_array one_d_life_point

one_d_life_array: one_d_life_array.o memcheck.o
	$(CC) one_d_life_array.o memcheck.o -o one_d_life_array

one_d_life_point: one_d_life_point.o memcheck.o
	$(CC) one_d_life_point.o memcheck.o -o one_d_life_point

memcheck.o: memcheck.c memcheck.h
	$(CC) $(CFLAGS) -c memcheck.c

one_d_life_array.o: one_d_life_array.c
	$(CC) $(CFLAGS) -c one_d_life_array.c

one_d_life_point.o: one_d_life_point.c
	$(CC) $(CFLAGS) -c one_d_life_point.c

check:
	c_style_check one_d_life_array.c one_d_life_point.c

clean:
	rm -f *.o one_d_life_array one_d_life_point
