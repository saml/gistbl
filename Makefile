CFLAGS = -O2 \
		 -Isundown/src \
		 -Wall -Wextra -Wno-unused-variable -Wno-unused-parameter -Wno-unused-but-set-variable \
		 $(CFLAGS_EXTRA)

LDFLAGS = -llua 

OBJDIR = target

all: 
