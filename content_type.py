from blog.models import PostReaction
from django.forms.models import model_to_dict

# Get the model fields as a dictionary
post_r = PostReaction.objects.all()

# Extract the field names
for i in post_r:
    print(i)