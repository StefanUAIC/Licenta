from typing import List

from ninja import Router

from posts.models import Post
from users.authentication import jwt_auth
from .schemas import PostSchema, PostOutSchema

posts_router = Router(tags=['Posts'])


@posts_router.post("/", auth=jwt_auth, response={201: PostOutSchema, 403: dict})
def create_post(request, payload: PostSchema):
    user = request.auth
    if not user.role == 'teacher':
        return 403, {"error": "Only teachers can create posts"}
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
        created_at=post.created_at
    )


@posts_router.get("/", auth=jwt_auth, response=List[PostOutSchema])
def list_posts(request):
    posts = Post.objects.filter(status='ACCEPTED')
    return [PostOutSchema(
        id=post.id,
        title=post.title,
        content=post.content,
        author=str(post.author),
        created_at=post.created_at
    ) for post in posts]
