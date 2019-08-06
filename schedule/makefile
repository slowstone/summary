CXX=g++

OBJS = utils.cpp main.cpp RMS.cpp utils.h RMS.h EDF.cpp EDF.h
OS = utils.o main.o RMS.o EDF.o

all : rtsim

rtsim : $(OS)
	$(CXX) -o rtsim $(OS)

$(OS) : $(OBJS) 
	$(CXX) -c -std=c++11 $(OBJS)

clean :
	rm $(OS)
	rm *.h.gch
	rm rtsim
