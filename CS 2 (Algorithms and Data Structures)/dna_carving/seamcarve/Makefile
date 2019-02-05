CC = g++
LD = g++
DOCSGEN = doxygen
CFLAGS = -std=c++11 -Wall -pedantic -ggdb `sdl-config --cflags`
SDLLIBS = `sdl-config --libs`
SRCDIR = src
OBJDIR = obj
BINDIR = bin
DOCSDIR = docs

.PHONY: docs clean clean-docs

seamcarve: $(OBJDIR)/SeamCarveApp.o $(OBJDIR)/SeamCarveAlgorithm.o
	$(LD) $(OBJDIR)/SeamCarveApp.o $(OBJDIR)/SeamCarveAlgorithm.o $(SDLLIBS) -o $(BINDIR)/seamcarve

$(OBJDIR)/SeamCarveApp.o: $(SRCDIR)/SeamCarveApp.cpp $(SRCDIR)/SeamCarveApp.hpp
	$(CC) -c $(SRCDIR)/SeamCarveApp.cpp $(CFLAGS) -o $(OBJDIR)/SeamCarveApp.o

$(OBJDIR)/SeamCarveAlgorithm.o: $(SRCDIR)/SeamCarveAlgorithm.cpp \
$(SRCDIR)/SeamCarveApp.hpp
	$(CC) -c $(SRCDIR)/SeamCarveAlgorithm.cpp $(CFLAGS) -o $(OBJDIR)/SeamCarveAlgorithm.o

clean:
	rm -f $(OBJDIR)/*.o $(BINDIR)/*

docs:
	$(DOCSGEN)

clean-docs:
	rm -rf $(DOCSDIR)/*
