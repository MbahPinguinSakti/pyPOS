from django.shortcuts import redirect


def index(request):
    """Redirect root path to store dashboard."""
    return redirect('store_index')
