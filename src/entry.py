import re
from urllib.parse import urlparse

from js import Response


def on_get_posts():
    return Response.new('get_posts')


def on_get_post(id):
    return Response.new("get_post %s" % id)


def on_post_new():
    return Response.new('post_new')


def on_vote(id):
    return Response.new('post_new %s' % id)


async def on_fetch(request, env):
    method = request.method
    path = urlparse(request.url).path
    queries = urlparse(request.url).query
    if method == "GET":
        if path == "/posts":
            return on_get_posts()
        r = re.fullmatch(r"/posts/(\d+)", path)
        if r is not None:
            return on_get_post(r.group(1))
    if method == "POST":
        if path == "/posts":
            return on_post_new()
        r = re.fullmatch(r"/posts/(\d+)/vote", path)
        if r is not None:
            return on_vote(r.group(1))
    return Response.new('Hello, World!')
