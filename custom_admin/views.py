from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from gifts.models import Gift
import random

User = get_user_model()

def is_santa(user):
    return user.is_authenticated and user.is_staff

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. Only Santa allowed.")
    else:
        form = AuthenticationForm()
    return render(request, 'custom_admin/login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@user_passes_test(is_santa, login_url='admin_login')
def dashboard(request):
    today = timezone.now()
    total_users = User.objects.count()
    total_gifts = Gift.objects.count()
    gifts_delivered = User.objects.filter(received_gift_at__isnull=False).count()
    users_waiting = User.objects.filter(received_gift_at__isnull=True).exclude(is_staff=True).count()
    
    # Simple kindness leader logic
    top_contributors = User.objects.annotate(gift_count=Count('gifts_given')).filter(gift_count__gt=0).order_by('-gift_count')[:5]

    context = {
        'today': today,
        'total_users': total_users,
        'total_gifts': total_gifts,
        'gifts_delivered': gifts_delivered,
        'users_waiting': users_waiting,
        'top_contributors': top_contributors,
    }
    return render(request, 'custom_admin/dashboard.html', context)

@user_passes_test(is_santa, login_url='admin_login')
def users_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    contrib_filter = request.GET.get('contrib', '')
    
    users = User.objects.filter(is_staff=False).annotate(gift_count=Count('gifts_given')).order_by('-date_joined')
    
    # Search
    if query:
        users = users.filter(Q(full_name__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query))
    
    # Filters
    if status_filter == 'delivered':
        users = users.filter(received_gift_at__isnull=False)
    elif status_filter == 'not_received':
        users = users.filter(received_gift_at__isnull=True)
        
    if contrib_filter == 'contributed':
        users = users.filter(gift_count__gt=0)
    elif contrib_filter == 'not_contributed':
        users = users.filter(gift_count=0)

    return render(request, 'custom_admin/users.html', {
        'users': users,
        'search_query': query,
        'status_filter': status_filter,
        'contrib_filter': contrib_filter
    })

@user_passes_test(is_santa, login_url='admin_login')
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_gifts = Gift.objects.filter(user=user).order_by('-created_at')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'mark_delivered':
            user.received_gift_at = timezone.now()
            user.save()
            messages.success(request, f"Marked {user.full_name} as Delivered!")
            return redirect('admin_user_detail', user_id=user.id)
            
        elif action == 'mark_collected':
            gift_id = request.POST.get('gift_id')
            gift = get_object_or_404(Gift, id=gift_id, user=user)
            gift.collected_at = timezone.now()
            gift.save()
            messages.success(request, "Gift marked as collected.")
            return redirect('admin_user_detail', user_id=user.id)
            
        elif action == 'find_receiver':
            # Logic to find a random receiver
            # Exclude current user, admins, and those who already received
            candidates = User.objects.filter(
                is_staff=False, 
                received_gift_at__isnull=True
            ).exclude(id=user.id)
            
            if candidates.exists():
                selected = random.choice(list(candidates))
                messages.info(request, f"✨ Matched with: {selected.full_name} ({selected.city})")
                # We could redirect to the selected user or just show them. 
                # Prompt says 'Display selected user details'. 
                # Let's show it in context or redirect to their detail page? 
                # 'Display selected user's: Name, Address, Phone'.
                # Let's pass it to context.
                return render(request, 'custom_admin/user_detail.html', {
                    'user': user,
                    'user_gifts': user_gifts,
                    'matched_receiver': selected,
                    'show_match_modal': True
                })
            else:
                messages.warning(request, "No eligible receivers found.")

    return render(request, 'custom_admin/user_detail.html', {
        'user': user,
        'user_gifts': user_gifts
    })
