from django.db.models.signals import post_save
from django.dispatch import receiver
from extra.models import Action, Notif_Count

@receiver(post_save, sender=Action)
def action_saved(sender, instance, **kwargs):
    n, c = Notif_Count.objects.get_or_create(target=instance.target)
    n.count = n.count + 1
    n.save()
