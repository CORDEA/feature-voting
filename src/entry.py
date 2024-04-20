import re
from datetime import datetime
from urllib.parse import urlparse

from js import Response
from pyodide.ffi import JsException


async def on_get_posts(env):
    result = await env.DB.prepare('SELECT * FROM Features').all()
    return Response.json(result.results)


async def on_get_post(env, pid):
    result = await env.DB.prepare('SELECT * FROM Features WHERE ID = ?1').bind(pid).all()
    if len(result.results) > 0:
        return Response.json(result.results[0])
    return Response.json({}, status=404)


async def on_post_new(env, body):
    try:
        created_at = datetime.fromisoformat(body.CreatedAt)
    except ValueError:
        return Response.json({}, status=500)
    try:
        votes = int(body.Votes)
    except ValueError:
        return Response.json({}, status=500)
    title = body.Title
    body = body.Body
    if len(title) <= 0 or len(body) <= 0:
        return Response.json({}, status=500)
    result = await env.DB.prepare(
        'INSERT INTO Features (CreatedAt, Title, Body, Votes) '
        'VALUES (?1, ?2, ?3, ?4)'
    ).bind(created_at.isoformat(), title, body, votes).all()
    if result.success:
        return Response.json({}, status=201)
    return Response.json({}, status=500)


async def on_vote(env, pid):
    result = await env.DB.prepare('SELECT Votes FROM Features WHERE ID = ?1').bind(pid).all()
    if len(result.results) <= 0:
        return Response.json({}, status=500)
    vote = int(result.results[0].Votes)
    result = await env.DB.prepare('UPDATE Features SET Votes = ?1 WHERE ID = ?2').bind(vote + 1, pid).all()
    if result.success:
        return Response.json({}, status=200)
    return Response.json({}, status=500)


async def on_fetch(request, env):
    method = request.method
    path = urlparse(request.url).path
    if method == 'GET':
        if path == '/posts':
            return on_get_posts(env)
        r = re.fullmatch(r'/posts/(\d+)', path)
        if r is not None:
            return on_get_post(env, r.group(1))
    if method == 'POST':
        if path == '/posts':
            try:
                body = await request.json()
            except JsException:
                body = {}
            return on_post_new(env, body)
        r = re.fullmatch(r'/posts/(\d+)/vote', path)
        if r is not None:
            return on_vote(env, r.group(1))
    return Response.json({}, status=404)
