#define LUA_LIB

#include <string.h>
#include <lauxlib.h>
#include <lua.h>
#include <lualib.h>

#include "markdown.h"
#include "html_blocks.h"
#include "buffer.h"

#define READ_UNIT 256
#define OUTPUT_UNIT 128

#define SUNDOWN_LIBRARY "sundown"
#define OVERHEAD_GUESS 1.3f

static int sundown_markdown(lua_State *L) {
    const char *indoc;
    size_t indocSize;
    struct buf *inbuf;
    struct buf *outbuf;
    struct sd_callbacks callbacks;
    struct sd_markdown *markdown;
    int targetSize;

    indoc = luaL_checklstring(L, 1, &indocSize);
    inbuf = bufnew(READ_UNIT);
    bufput(inbuf, indoc, indocSize);
    
    // Overhead guess inspired by Redcarpet.
    targetSize = (int)(indocSize * OVERHEAD_GUESS);
    outbuf = bufnew(OUTPUT_UNIT);
    bufgrow(outbuf, targetSize);

    markdown = sd_markdown_new(0, 16, &callbacks, NULL);
    sd_markdown_render(outbuf, inbuf->data, inbuf->size, markdown);
    sd_markdown_free(markdown);

    lua_pushlstring(L, outbuf->data, outbuf->size);
    
    bufrelease(inbuf);
    bufrelease(outbuf);
    
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
