from .common import *

def LogoutView(request):
    logout(request)
    return redirect('accounts:pn_login')