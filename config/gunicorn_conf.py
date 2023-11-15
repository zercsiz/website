def post_request(worker, req, environ, resp):
    if req.path.endswith('.css'):
        resp.headers['Content-Type'] = 'text/css'

        