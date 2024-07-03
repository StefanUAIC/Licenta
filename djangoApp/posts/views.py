from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from posts.models import Post
from users.authentication import jwt_auth
from .schemas import PostSchema, PostOutSchema

posts_router = Router(tags=['Posts'])


@posts_router.post("/", auth=jwt_auth, response={201: PostOutSchema, 403: dict})
def create_post(request, payload: PostSchema):
    user = request.auth
    post = Post.objects.create(
        title=payload.title,
        content=payload.content,
        author=user,
        status='PENDING'
    )
    return 201, PostOutSchema(
        id=post.id,
        title=post.title,
        content=post.content,
        author=str(post.author),
        created_at=post.created_at,
        author_id=post.author.id
    )


@posts_router.post("/{post_id}/like", auth=jwt_auth, response={200: PostOutSchema, 404: dict})
def like_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    user = request.auth

    if user in post.dislikes.all():
        post.dislikes.remove(user)

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return 200, PostOutSchema(
        id=post.id,
        title=post.title,
        content=post.content,
        author=str(post.author),
        created_at=post.created_at,
        author_id=post.author.id,
        likes_count=post.like_count(),
        dislikes_count=post.dislike_count(),
        is_liked=user in post.likes.all(),
        is_disliked=user in post.dislikes.all()
    )


@posts_router.post("/{post_id}/dislike", auth=jwt_auth, response={200: PostOutSchema, 404: dict})
def dislike_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    user = request.auth

    if user in post.likes.all():
        post.likes.remove(user)

    if user in post.dislikes.all():
        post.dislikes.remove(user)
    else:
        post.dislikes.add(user)

    return 200, PostOutSchema(
        id=post.id,
        title=post.title,
        content=post.content,
        author=str(post.author),
        created_at=post.created_at,
        author_id=post.author.id,
        likes_count=post.like_count(),
        dislikes_count=post.dislike_count(),
        is_liked=user in post.likes.all(),
        is_disliked=user in post.dislikes.all()
    )


@posts_router.get("/", auth=jwt_auth, response=List[PostOutSchema])
def list_posts(request):
    posts = Post.objects.filter(status='ACCEPTED')
    user = request.auth
    return [PostOutSchema(
        id=post.id,
        title=post.title,
        content=post.content,
        author=str(post.author),
        created_at=post.created_at,
        author_id=post.author.id,
        likes_count=post.like_count(),
        dislikes_count=post.dislike_count(),
        is_liked=user in post.likes.all(),
        is_disliked=user in post.dislikes.all()
    ) for post in posts]
