from blog.models import Post  # Replace 'blog' with your actual app name if different
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

fake = Faker()

users = User.objects.exclude(username='gorbenkoss')
posts_to_create = []

for user in users:
    for _ in range(25):  # Creates 25 posts per user
        title = fake.sentence(nb_words=6)  # Generates a random title
        content = fake.text(max_nb_chars=1000)  # Generates a random text
        date_posted = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.utc)  # Generates a random datetime within the last year

        post = Post(title=title, content=content, author=user, date_posted=date_posted)
        posts_to_create.append(post)

# Bulk create the posts
Post.objects.bulk_create(posts_to_create)
