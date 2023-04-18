from .models import SiteConfig


def site_defaults(request):
    vals = SiteConfig.objects.all()
    contexts = {
        
    }
    for val in vals:
        contexts[val.key] = val.value

    return contexts
