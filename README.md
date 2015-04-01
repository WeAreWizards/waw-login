# waw-login

This module is used in combination with the
[nginx auth_request_module](http://nginx.org/en/docs/http/ngx_http_auth_request_module.html)

We're pretty open but there are some parts of our infrastructure that
cannot - by nature - be public.

This module allows us to protect certain paths by delegating
authentication to this module. This module checks for a correct JWT
token.
