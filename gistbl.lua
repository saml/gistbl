local say = ngx.say
local uri = ngx.var.uri
local exit = ngx.exit
local htdocs = ngx.var.document_root
local INFO = ngx.INFO
local ERR = ngx.ERR
local log = ngx.log --function(...) ngx.log(ngx.ERR, ...) end

local sundown = require('sundown')
local pl_file = require('pl.file')
local pl_path = require('pl.path')
local pl_stringx = require('pl.stringx')
local pl_template = require('pl.template')
local pl_date = require('pl.Date')

local get_template = function()
    local template_path = htdocs .. '/template.html'
    return pl_file.read(template_path)
end

local get_title = function(uri)
    local file_name,_ = pl_path.splitext(pl_path.basename(uri))
    local title,_ = file_name:gsub('[-%s]+', ' ')
    return title
end

local get_markdown = function(uri)
    local left,_ = pl_path.splitext(uri)
    return htdocs .. left .. '.md'
end



local render = function()
    log(ERR, uri)
    local markdown_path = get_markdown(uri)
    local input = pl_file.read(markdown_path)
    if not input then
        exit(404)
        return
    end

    local title = get_title(uri)
    local content = sundown.markdown(input)
    local modified_at = pl_date(pl_file.modified_time(markdown_path))
    local template = get_template()
    say(pl_template.substitute(template, { 
        title = title, 
        content = content, 
        modified_at = tostring(modified_at) 
    }))
end

render()
