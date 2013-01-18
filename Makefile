CFLAGS = -O2 \
		 -Isundown/src $(LUA_INCLUDE) \
		 -Wall -Wextra -Wno-missing-field-initializers -Wno-unused-parameter \
		 $(CFLAGS_EXTRA)


LDFLAGS = $(LUA_LIB) -llua -shared -fPIC

LUA_INCLUDE = -I$(HOME)/opt/openresty/luajit/include/luajit-2.0
LUA_LIB = -L$(HOME)/opt/openresty/luajit/lib




libsundown.so: sundown/src/buffer.c sundown/src/autolink.c sundown/src/stack.c sundown/src/markdown.c lua_sundown.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm libsundown.so
