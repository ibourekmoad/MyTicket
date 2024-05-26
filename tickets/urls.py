from django.shortcuts import redirect
from django.urls import path

from tickets import views

urlpatterns = [
    path('', lambda request: redirect('dashboard')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new-ticket/', views.new_ticket, name='new-ticket'),
    path('view-ticket/', views.view_tickets, name='view-ticket'),
    path('detail-ticket/<str:ticket_id>', views.detail_tickets, name='detail-ticket'),
    path('update-ticket/<str:ticket_id>', views.update_ticket, name='update-ticket'),
    path('delete-ticket/<str:ticket_id>', views.delete_ticket, name='delete-ticket'),
]
