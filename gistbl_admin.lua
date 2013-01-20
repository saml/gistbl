local say = ngx.say
local uri = ngx.var.uri
local exit = ngx.exit
local htdocs = ngx.var.document_root
local method = ngx.req.get_method()
local POST = ngx.HTTP_POST
local INFO = ngx.INFO
local ERR = ngx.ERR
local log = ngx.log 

say(ngx.var.templatedir)
