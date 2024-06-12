from django.core.management.base import BaseCommand
import random
from datetime import timedelta
from django.utils import timezone
from faker import Faker
from django.contrib.auth.models import User
from blog.models import Post, PostReaction

class Command(BaseCommand):
    help = 'Simulates user reactions on posts.'

    def handle(self, *args, **options):
        fake = Faker()

        users = User.objects.exclude(username='gorbenkoss')
        posts = list(Post.objects.all())
        max_posts = len(posts)

        if max_posts == 0:
            self.stdout.write(self.style.ERROR('No posts available to like or dislike.'))
            return

        for user in users:
            number_of_reactions = random.randint(5, max_posts)
            posts_to_react = random.sample(posts, number_of_reactions)

            reactions_to_create = []
            for post in posts_to_react:
                reaction_date = fake.date_time_between(start_date='-2d', end_date='now', tzinfo=timezone.utc)
                is_like = random.choice([True, False])

                reaction = PostReaction(
                    post=post,
                    user=user,
                    liked=is_like,
                    date_created=reaction_date
                )
                reactions_to_create.append(reaction)

            PostReaction.objects.bulk_create(reactions_to_create)
            self.stdout.write(self.style.SUCCESS(f'Processed {len(reactions_to_create)} reactions for user {user.username}'))
