# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest

def get_hero_next_image_content(request):
    # Retrieve the content based on the index or ID sent via AJAX
    index = int(request.GET.get('index', 0))
    # For this example, we're just cycling through a predefined list of content.
    # In practice, you would query the database here.
    content = [
        {
            'title': 'The Role of Media in Modern Politics',
            'image': 'https://foxiz.themeruby.com/presspulse/wp-content/uploads/sites/2/2024/07/e4-420x280.jpg',
            'summary': 'Great design seamlessly integrates with the user experience...',
            'date': 'July 22, 2024',
        },
        # Add more content items here...
    ]

    # Ensure the index loops back to 0 if it exceeds available content
    current_content = content[index % len(content)]
    
    # Render the content block (you can use a partial template for this)
    html_content = render(request, 'components/utils/hero_slider.html', {'content': current_content}).content.decode('utf-8')
    
    return JsonResponse({'html': html_content})


def rsd_view(request:HttpRequest):
    xml_content = render_to_string('components/utils/rsd_template.xml', {
        'site_url': request.build_absolute_uri('/'),  # Get the absolute URL of the site
    })
    return HttpResponse(xml_content, content_type='application/xml')


urlpatterns = [
    path("", include("website.main.main_app.urls")),
    path("rsd.xml", rsd_view, name="rsd"),
    path("hero/get-next-content/", get_hero_next_image_content, name="hero-slider"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    # Your stuff: custom urls includes go here
    # ...
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
