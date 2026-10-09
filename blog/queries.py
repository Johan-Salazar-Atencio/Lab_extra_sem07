"""Queries behind the views. Part 2 of the lab happens in this file."""
from django.db.models import Count, Q

from blog.models import Post


def all_posts():
    return Post.objects.all()


def post_by_id(post_id):
    return Post.objects.get(id=post_id)


def published_posts():
    return Post.published_objects.all()


def draft_posts():
    return Post.objects.filter(published=False)


def posts_with_title_containing(text):
    return Post.objects.filter(title__icontains=text)


def posts_between_dates(start, end):
    return Post.objects.filter(published_at__range=(start, end))


def posts_without_category():
    return Post.objects.filter(category__isnull=True)


def posts_with_more_than_n_comments(n):
    return Post.objects.annotate(n_comments=Count("comments")).filter(n_comments__gt=n)


def posts_by_author_country(country):
    return Post.objects.filter(author__profile__country=country)


def comments_of_category(category_name):
    from blog.models import Comment
    return Comment.objects.filter(post__category__name=category_name)


def most_recent_posts(limit=10):
    return Post.published_objects.order_by("-published_at")[:limit]


def most_commented_posts(limit=5):
    return Post.published_objects.annotate(n_comments=Count("comments")).order_by("-n_comments")[:limit]


def posts_for_front_page():
    return Post.published_objects.select_related("author").prefetch_related("tags").order_by("-published_at")
