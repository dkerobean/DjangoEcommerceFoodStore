from .models import UserProfile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    
    if created:
        user = instance
        profile = UserProfile.objects.create(
            user = user, 
            email = user.email   
        )
        

@receiver(post_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    try:
        profile = instance.userprofile
        profile.delete()
    except UserProfile.DoesNotExist:
        pass
    
    
        
        
        

        
        