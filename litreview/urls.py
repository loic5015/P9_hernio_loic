"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView, PasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static
import authentication.views
import books.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('change_password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'
    ), name='password_change'),
    path('change_password_done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'
    ), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', books.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('books/create_ticket/', books.views.create_ticket, name='create-ticket'),
    path('books/<int:ticket_id>/create', books.views.create_review, name='create-review'),
    path('books/create_critique', books.views.create_review_ticket, name='create-review-ticket'),
    path('books/subscribe/', books.views.subscribe_user, name='subscribe-page'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
