CFLAGS = -O2 \
		 -Isundown/src -Isundown/html $(LUA_INCLUDE) \
		 -Wall -Wextra -Wno-missing-field-initializers -Wno-unused-parameter \
		 $(CFLAGS_EXTRA)


LDFLAGS = $(LUA_LIB) -llua -shared -fPIC

LUA_HOME = $(HOME)/opt/openresty/luajit
LUA_INCLUDE = -I$(LUA_HOME)/include/luajit-2.0
LUA_LIB = -L$(LUA_HOME)/lib

SRCS = sundown/src/*.c \
	   sundown/html/*.c \
	   lua_sundown.c

libsundown.so: $(SRCS)
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm libsundown.so
