from .models import UserProfile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    
    if created:
        user = instance
        profile = UserProfile.create(
            user = user,
            username = user.username,
            email = user.email
            
        )
        
@reciever(post_delete, sender=User)        
def delete_profile(sender, instance, **kwargs):
    
    user = instance.user
    user.delete()
    
    
        
        
        

        
        