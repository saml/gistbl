#define LUA_LIB

#include <string.h>
#include <lauxlib.h>
#include <lua.h>
#include <lualib.h>

#include "markdown.h"
#include "html.h"

#define READ_UNIT 256
#define OUTPUT_UNIT 128

#define SUNDOWN_LIBRARY "sundown"

/* sundown.markdown(input_string) ==> output_string */
static int sundown_markdown(lua_State *L) {
    const char *indoc;
    size_t indocSize;
    struct buf *inbuf;
    struct buf *outbuf;
    struct html_renderopt options;
    struct sd_callbacks callbacks;
    struct sd_markdown *markdown;

    /* read input_string */
    indoc = luaL_checklstring(L, 1, &indocSize);
    inbuf = bufnew(READ_UNIT);
    bufgrow(inbuf, indocSize);
    bufput(inbuf, indoc, indocSize);

    /* prepare for output_string */
    outbuf = bufnew(OUTPUT_UNIT);
    sdhtml_renderer(&callbacks, &options, 0);
    markdown = sd_markdown_new(0, 16, &callbacks, &options);

    /* write output_string */
    sd_markdown_render(outbuf, inbuf->data, inbuf->size, markdown);
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
