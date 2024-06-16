from blog.models import Post, Comment  # Replace 'blog' with your actual app name if different
from django.contrib.auth.models import User
import random
from django.utils import timezone
from faker import Faker

fake = Faker()

users = User.objects.exclude(username='gorbenkoss')
posts = list(Post.objects.all())
comments_to_create = []

for user in users:
    posts_to_comment = random.randint(300, len(posts))
    for post in random.sample(posts, posts_to_comment):
        content = fake.text(max_nb_chars=40)  # Generates a random text
        date_posted = fake.date_time_between(start_date='-2d', end_date='now', tzinfo=timezone.utc)  # Generates a random datetime within the last year
        comment = Comment(content=content, author=user, date_posted=date_posted, parent_post=post)
        comments_to_create.append(comment)

print(len(posts))
print(len(comments_to_create))   
# Bulk create the posts
Comment.objects.bulk_create(comments_to_create)
