import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TicketForm
from .models import Ticket

@login_required(login_url='/users/login/')
def dashboard(request):
    if request.user.is_customer:
        tickets = Ticket.objects.filter(customer=request.user)
        recent_tickets = tickets.order_by('-created_at')[:5]
        total_tickets = tickets.count()
        pending_tickets = tickets.filter(status=2).count()
        resolved_tickets = tickets.filter(status=3).count()
        active_tickets = tickets.filter(status=1).count()
        context = {
            'total_tickets': total_tickets,
            'pending_tickets': pending_tickets,
            'resolved_tickets': resolved_tickets,
            'active_tickets': active_tickets,
            'recent_tickets': recent_tickets,
        }
        return render(request, 'ticket/customer_dasboard.html', context)
    elif request.user.is_engineer:
        tickets = Ticket.objects.filter(engineer=request.user)
        total_tickets = tickets.count()
        pending_tickets = tickets.filter(status=1).count()
        resolved_tickets = tickets.filter(status=3).count()
        recent_tickets = tickets.order_by('-created_at')[:5]
        context = {
            'total_tickets': total_tickets,
            'pending_tickets': pending_tickets,
            'resolved_tickets': resolved_tickets,
            'recent_tickets': recent_tickets,
        }
        return render(request, 'ticket/engineer_dashboard.html', context)
    elif request.user.is_admin:
        return render(request, 'ticket/admin_dashboard.html')
    else:
        return HttpResponse('Invalid role')


def new_ticket(request):
    if request.user.is_customer:
        if request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.customer = request.user
                ticket.save()
                return redirect('dashboard')
            else:
                return HttpResponse('Something went wrong')
        else:
            form = TicketForm()
            return render(request, 'ticket/new_ticket.html', {'form': form})
    return HttpResponse('Unauthorized', status=401)


def view_tickets(request):
    if request.user.is_authenticated:
        if request.user.is_customer:
            tickets = Ticket.objects.filter(customer=request.user)
        elif request.user.is_engineer:
            tickets = Ticket.objects.filter(engineer=request.user)
        else:
            return HttpResponse('Unauthorized', status=401)
        return render(request, 'ticket/view_ticket.html', {'tickets': tickets})
    return HttpResponse('Unauthorized', status=401)


def detail_tickets(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if request.user.is_customer and ticket.customer == request.user:
        form = TicketForm(instance=ticket)
    elif request.user.is_engineer and ticket.engineer == request.user:
        form = TicketForm(instance=ticket)
    else:
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'ticket/detail_ticket.html', {'form': form, 'ticket': ticket})


def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if request.user.is_customer and ticket.customer == request.user:
        if request.method == 'POST':
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect('detail-ticket', ticket_id=ticket_id)
            return render(request, 'ticket/detail_ticket.html', {'form': form, 'ticket': ticket})
    elif request.user.is_engineer and ticket.engineer == request.user:
        if request.method == 'POST':
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid():
                ticket.status = 3
                form.save()
                return redirect('detail-ticket', ticket_id=ticket_id)
            return render(request, 'ticket/detail_ticket.html', {'form': form, 'ticket': ticket})
    return HttpResponse('Unauthorized', status=401)


def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if request.user.is_customer and ticket.customer == request.user:
        ticket.delete()
        return redirect('view-ticket')
    return HttpResponse('Unauthorized', status=401)
