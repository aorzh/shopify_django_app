from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
import shopify
from django.http.response import HttpResponseRedirect
from django.contrib import auth


def _return_address(request):
    return request.session.get('return_to') or reverse('root_path')


def login(request, *args, **kwargs):
    # Ask user for their ${shop}.myshopify.com address

    # If the ${shop}.myshopify.com address is already provided in the URL,
    # just skip to authenticate
    shop = request.POST.get('shop', request.GET.get('shop'))
    if shop:
        return authenticate(request)
    return render(request, 'shopify_app/login.html', {})


def authenticate(request, *args, **kwargs):
    shop = request.POST.get('shop', request.GET.get('shop'))
    if shop:
        scope = settings.SHOPIFY_API_SCOPE
        redirect_uri = request.build_absolute_uri(reverse('shopify_app_finalize'))
        permission_url = shopify.Session(shop.strip()).create_permission_url(scope, redirect_uri)
        return redirect(permission_url)

    return redirect(_return_address(request))


def finalize(request, *args, **kwargs):
    shop = request.POST.get('shop', request.GET.get('shop'))
    try:
        shopify_session = shopify.Session(shop, token=kwargs.get('token'))
        shopify_session.request_token(request.GET)
        # shopify_session = shopify.Session(shop)
        request.session['shopify'] = {
            "shop_url": shopify_session.url,
            "access_token": shopify_session.token
        }

    except Exception:
        # login_url = reverse(login)
        # return HttpResponseRedirect(login_url)
        messages.error(request, "Could not log in to Shopify store.")
        return redirect(reverse('shopify_app.views.login'))

    messages.info(request, "Logged in to shopify store.")

    # Attempt to authenticate the user and log them in.
    """
    user = auth.authenticate(myshopify_domain=shopify_session.url, token=shopify_session.token)
    if user:
        auth.login(request, user)

    return_address = _return_address(request)
    return HttpResponseRedirect(return_address)
    """
    response = redirect(_return_address(request))
    request.session.pop('return_to', None)
    return response


def logout(request):
    request.session.pop('shopify', None)
    shopify.ShopifyResource.clear_session()
    messages.info(request, "Successfully logged out.")

    return redirect(reverse('shopify_app_login'))
