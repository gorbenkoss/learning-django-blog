from django.core.management.base import BaseCommand
from django.db.models import Sum, Case, When, IntegerField
from blog.models import Post, PostReaction

class Command(BaseCommand):
    help = 'Recalculates and updates the ratings for each post based on PostReactions'

    def handle(self, *args, **options):
        # Process each post individually
        posts = Post.objects.all()
        for post in posts:
            # Calculate the sum of likes and dislikes as the rating
            reactions = PostReaction.objects.filter(post=post).aggregate(
                rating=Sum(
                    Case(
                        When(liked=True, then=1),
                        When(liked=False, then=-1),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            )

            # Ensure we handle cases where there are no reactions
            new_rating = reactions['rating'] if reactions['rating'] is not None else 0

            # Update the post's rating if it has changed
            if post.rating != new_rating:
                post.rating = new_rating
                post.save()
                self.stdout.write(self.style.SUCCESS(f'Updated rating for post "{post.title}" to {new_rating}.'))
            else:
                self.stdout.write(self.style.NOTICE(f'No update needed for post "{post.title}".'))

        self.stdout.write(self.style.SUCCESS('Finished updating post ratings.'))
