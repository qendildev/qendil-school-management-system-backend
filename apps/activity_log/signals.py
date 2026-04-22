from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.core.middleware import get_current_user

# Apps to skip logging for
SKIP_APPS = [
    'activity_log', 'admin', 'contenttypes', 'sessions',
    'authtoken', 'token_blacklist', 'migrations',
]

def get_model_module(model):
    return model._meta.app_label

def log_activity(sender, instance, action, **kwargs):
    # Ignore activity logs themselves and Django internal models
    if sender._meta.app_label in SKIP_APPS:
        return

    # Skip migration-related models
    if sender.__name__ in ['Migration', 'ContentType', 'Session']:
        return

    user = get_current_user()

    # Skip if no authenticated user (e.g. during migrations)
    if user and not user.is_authenticated:
        user = None

    try:
        object_id = str(instance.pk)
    except Exception:
        object_id = "unknown"

    try:
        details = str(instance)[:500]
    except Exception:
        details = ""

    try:
        # Lazy import to avoid circular imports and table-not-exist errors
        from apps.activity_log.models import ActivityLog
        ActivityLog.objects.create(
            user=user,
            action=action,
            module=get_model_module(sender),
            model_name=sender.__name__,
            object_id=object_id,
            details=details
        )
    except Exception:
        # Silently fail if the table doesn't exist yet (during migrations)
        pass

@receiver(post_save)
def post_save_handler(sender, instance, created, **kwargs):
    action = 'Created' if created else 'Updated'
    log_activity(sender, instance, action, **kwargs)

@receiver(post_delete)
def post_delete_handler(sender, instance, **kwargs):
    log_activity(sender, instance, 'Deleted', **kwargs)
