#define LUA_LIB

/*
gcc -Isundown/src -I/home/sam/opt/openresty/luajit/include/luajit-2.0 sundown/src/buffer.c sundown/src/autolink.c sundown/src/stack.c sundown/src/markdown.c lua_sundown.c -shared -fPIC -L /home/sam/opt/openresty/luajit/lib -llua
gcc -Isundown/src -I/home/sam/opt/openresty/luajit/include/luajit-2.0 sundown/src/buffer.c sundown/src/autolink.c sundown/src/stack.c sundown/src/markdown.c lua_sundown.c -shared -fPIC -L /home/sam/opt/openresty/luajit/lib -llua -o libsundown.so
 
 */

#include <string.h>
#include <lauxlib.h>
#include <lua.h>
#include <lualib.h>

#include <stdio.h>
#include "markdown.h"

#define READ_UNIT 256
#define OUTPUT_UNIT 128

#define SUNDOWN_LIBRARY "sundown"
#define OVERHEAD_GUESS 1.3f

static int sundown_markdown(lua_State *L) {
    const char *indoc;
    size_t indocSize;
    struct buf *inbuf;
    struct buf *outbuf;
    struct sd_callbacks callbacks = {0};
    struct sd_markdown *markdown;
    int targetSize;

    indoc = luaL_checklstring(L, 1, &indocSize);
    
    inbuf = bufnew(READ_UNIT);
    bufput(inbuf, indoc, indocSize);

    targetSize = (int)(indocSize * OVERHEAD_GUESS);
    outbuf = bufnew(OUTPUT_UNIT);
    bufgrow(outbuf, targetSize);

    markdown = sd_markdown_new(0, 16, &callbacks, NULL);
    sd_markdown_render(outbuf, inbuf->data, inbuf->size, markdown);
    printf("%d\n", outbuf->size);
    lua_pushlstring(L, (const char*) outbuf->data, outbuf->size);
    bufrelease(inbuf);
    bufrelease(outbuf);
    sd_markdown_free(markdown);
    
    return 1;
}

// Register the library.
static const struct luaL_reg sundown[] = {
    {"markdown", sundown_markdown},
    {NULL, NULL}
};
int luaopen_sundown(lua_State *L) {
    luaL_register(L, SUNDOWN_LIBRARY, sundown);
    return 1;
}
