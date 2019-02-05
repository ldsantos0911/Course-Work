CC = g++
DOCSGEN = doxygen
CFLAGS = -std=c++11 -Wall -pedantic -ggdb `sdl-config --cflags`
LIBS = `sdl-config --libs` -lSDL_gfx
SRCDIR = src
OBJDIR = obj
BINDIR = bin
DOCSDIR = docs
OBJS = $(OBJDIR)/Quadtree.o $(OBJDIR)/QuadtreeNode.o \
	$(OBJDIR)/QuadtreeVisualizerApp.o

.PHONY: quadtree docs clean

quadtree: $(OBJS)
	$(CC) $(OBJS) $(LIBS) -o $(BINDIR)/quadtree

$(OBJDIR)/Quadtree.o: $(SRCDIR)/Quadtree.cpp $(SRCDIR)/Quadtree.hpp \
	$(SRCDIR)/QuadtreeNode.cpp $(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/Quadtree.cpp -o $(OBJDIR)/Quadtree.o

$(OBJDIR)/QuadtreeNode.o: $(SRCDIR)/QuadtreeNode.cpp $(SRCDIR)/QuadtreeNode.cpp \
	$(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/QuadtreeNode.cpp -o $(OBJDIR)/QuadtreeNode.o

$(OBJDIR)/QuadtreeVisualizerApp.o: $(SRCDIR)/QuadtreeVisualizerApp.cpp \
	$(SRCDIR)/QuadtreeVisualizerApp.hpp $(SRCDIR)/Quadtree.hpp $(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/QuadtreeVisualizerApp.cpp -o $(OBJDIR)/QuadtreeVisualizerApp.o

docs:
	doxygen

clean:
	rm -f $(OBJDIR)/*.o $(BINDIR)/*
	rm -rf $(DOCSDIR)/*
