# project
TARGET  = erodr

# compiler
CC      = x86_64-w64-mingw32-gcc

# compiler specific flags
CSFLAGS = -fopenmp

# other flags
CFLAGS  = -O1 -std=c99 -Wall -pedantic

# linker
LINKER  = x86_64-w64-mingw32-gcc
LFLAGS  = -shared

# directories
OBJDIR  = obj
SRCDIR  = src
BINDIR  = .

SOURCES     := $(wildcard $(SRCDIR)/*.c)
INCLUDES    := $(wildcard $(SRCDIR)/*.h)
OBJECTS     := $(SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)

# targets
build: $(OBJDIR) $(TARGET)

$(BINDIR)/$(TARGET).dll: $(OBJECTS)
    $(LINKER) $(LFLAGS) $(CSFLAGS) $(OBJECTS) -o $@

$(OBJECTS): $(OBJDIR)/%.o : $(SRCDIR)/%.c
    $(CC) $(CFLAGS) $(CSFLAGS) -c $< -o $@

$(OBJDIR):
    mkdir $(OBJDIR)

clean:
    rm $(BINDIR)/$(TARGET).dll & rm $(OBJDIR)/*.o
