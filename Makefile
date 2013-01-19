CFLAGS = -O2 \
		 -Isundown/src -Isundown/html $(LUA_INCLUDE) \
		 -Wall -Wextra -Wno-missing-field-initializers -Wno-unused-parameter \
		 $(CFLAGS_EXTRA)


LDFLAGS = $(LUA_LIB) -llua -shared -fPIC

LUA_INCLUDE = -I$(HOME)/opt/openresty/luajit/include/luajit-2.0
LUA_LIB = -L$(HOME)/opt/openresty/luajit/lib

SRCS = sundown/src/*.c \
	   sundown/html/*.c \
	   lua_sundown.c

libsundown.so: $(SRCS)
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm libsundown.so
