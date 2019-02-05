CC = g++
DOCSGEN = doxygen
CFLAGS = -Wall -pedantic -ggdb -std=c++11 `sdl-config --cflags`  `xml2-config --cflags`
LIBS = -lm `sdl-config --libs` -lSDL_gfx  `xml2-config --libs` -lpthread
SRCDIR = src
OBJDIR = obj
BINDIR = bin
DOCSDIR = docs
OBJS = $(OBJDIR)/Material.o $(OBJDIR)/PointLight.o $(OBJDIR)/Ray.o \
	$(OBJDIR)/RaytracerApp.o $(OBJDIR)/RaytracerMultithreaded.o \
	$(OBJDIR)/RaytracerSinglethreaded.o $(OBJDIR)/Shader.o \
	$(OBJDIR)/Sphere.o $(OBJDIR)/Viewport.o $(OBJDIR)/World.o \
	$(OBJDIR)/XMLSceneParser.o

.PHONY: docs clean memcheck callgrind

raytracer: $(OBJS)
	$(CC) $(OBJS) $(LIBS) -o $(BINDIR)/raytracer

$(OBJDIR)/Material.o: $(SRCDIR)/Material.cpp $(SRCDIR)/Material.hpp \
    $(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/Material.cpp -o $(OBJDIR)/Material.o

$(OBJDIR)/Plane.o: $(SRCDIR)/Plane.cpp $(SRCDIR)/Plane.hpp \
    $(SRCDIR)/Entity.hpp $(SRCDIR)/Ray.hpp $(SRCDIR)/Material.hpp \
    $(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/Plane.cpp -o $(OBJDIR)/Plane.o

$(OBJDIR)/PointLight.o: $(SRCDIR)/PointLight.cpp \
    $(SRCDIR)/PointLight.hpp $(SRCDIR)/Light.hpp $(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/PointLight.cpp -o $(OBJDIR)/PointLight.o

$(OBJDIR)/Ray.o: $(SRCDIR)/Ray.cpp $(SRCDIR)/Ray.hpp \
    $(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/Ray.cpp -o $(OBJDIR)/Ray.o

$(OBJDIR)/RaytracerApp.o: $(SRCDIR)/RaytracerApp.cpp \
    $(SRCDIR)/RaytracerApp.hpp $(SRCDIR)/RaytracerBase.hpp \
    $(SRCDIR)/Shader.hpp $(SRCDIR)/World.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/RaytracerApp.cpp -o $(OBJDIR)/RaytracerApp.o

$(OBJDIR)/RaytracerMultithreaded.o: $(SRCDIR)/RaytracerMultithreaded.cpp \
    $(SRCDIR)/RaytracerMultithreaded.hpp $(SRCDIR)/RaytracerBase.hpp \
    $(SRCDIR)/World.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/RaytracerMultithreaded.cpp -o $(OBJDIR)/RaytracerMultithreaded.o

$(OBJDIR)/RaytracerSinglethreaded.o: $(SRCDIR)/RaytracerSinglethreaded.cpp \
    $(SRCDIR)/RaytracerSinglethreaded.hpp $(SRCDIR)/RaytracerBase.hpp \
    $(SRCDIR)/Shader.hpp $(SRCDIR)/World.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/RaytracerSinglethreaded.cpp -o $(OBJDIR)/RaytracerSinglethreaded.o

$(OBJDIR)/Shader.o: $(SRCDIR)/Shader.cpp $(SRCDIR)/Shader.hpp \
    $(SRCDIR)/Ray.hpp $(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/Shader.cpp -o $(OBJDIR)/Shader.o

$(OBJDIR)/Sphere.o: $(SRCDIR)/Sphere.cpp $(SRCDIR)/Sphere.hpp \
    $(SRCDIR)/Entity.hpp $(SRCDIR)/Ray.hpp $(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/Sphere.cpp -o $(OBJDIR)/Sphere.o

$(OBJDIR)/Viewport.o: $(SRCDIR)/Viewport.cpp $(SRCDIR)/Viewport.hpp \
    $(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/Viewport.cpp -o $(OBJDIR)/Viewport.o

$(OBJDIR)/World.o: $(SRCDIR)/World.cpp $(SRCDIR)/World.hpp \
    $(SRCDIR)/Ray.hpp $(SRCDIR)/Entity.hpp $(SRCDIR)/Light.hpp \
    $(SRCDIR)/Viewport.hpp $(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/World.cpp -o $(OBJDIR)/World.o

$(OBJDIR)/XMLSceneParser.o: $(SRCDIR)/XMLSceneParser.cpp \
    $(SRCDIR)/XMLSceneParser.hpp $(SRCDIR)/World.hpp $(SRCDIR)/Entity.hpp \
	$(SRCDIR)/Sphere.hpp $(SRCDIR)/Light.hpp $(SRCDIR)/PointLight.hpp \
	$(SRCDIR)/structs.hpp
	$(CC) $(CFLAGS) -c $(SRCDIR)/XMLSceneParser.cpp -o $(OBJDIR)/XMLSceneParser.o

clean:
	rm -f $(OBJDIR)/*.o $(BINDIR)/raytracer
	rm -rf $(DOCSDIR)/*

docs:
	$(DOCSGEN)

memcheck: $(OBJS)
	$(CC) $(CFLAGS) -c -DVALGRIND $(SRCDIR)/RaytracerApp.cpp -o $(OBJDIR)/RaytracerApp.o
	$(CC) $(OBJS) $(LIBS) -o $(BINDIR)/raytracer
	valgrind --tool=memcheck --leak-check=full $(BINDIR)/raytracer -m 2>&1 | tee memcheck.full

callgrind: $(OBJS)
	$(CC) $(CFLAGS) -c -DVALGRIND $(SRCDIR)/RaytracerApp.cpp -o $(OBJDIR)/RaytracerApp.o
	$(CC) $(OBJS) $(LIBS) -o $(BINDIR)/raytracer
	valgrind --tool=callgrind $(BINDIR)/raytracer -m
