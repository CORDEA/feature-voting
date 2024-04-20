import re
from urllib.parse import urlparse

from js import Response


async def on_get_posts(env):
    result = await env.DB.prepare('SELECT * FROM Features').all()
    return Response.json(result.results)


async def on_get_post(env, id):
    result = await env.DB.prepare('SELECT * FROM Features WHERE ID = ?1').bind(id).all()
    if len(result.results) > 0:
        return Response.json(result.results[0])
    return Response.json({}, status=404)


def on_post_new(env):
    return Response.new('post_new')


def on_vote(env, id):
    return Response.new('post_new %s' % id)


async def on_fetch(request, env):
    method = request.method
    path = urlparse(request.url).path
    queries = urlparse(request.url).query
    if method == "GET":
        if path == "/posts":
            return on_get_posts(env)
        r = re.fullmatch(r"/posts/(\d+)", path)
        if r is not None:
            return on_get_post(env, r.group(1))
    if method == "POST":
        if path == "/posts":
            return on_post_new(env)
        r = re.fullmatch(r"/posts/(\d+)/vote", path)
        if r is not None:
            return on_vote(env, r.group(1))
    return Response.new('Hello, World!')
