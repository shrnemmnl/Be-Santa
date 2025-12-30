from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GiftForm

@login_required
def be_santa_view(request):
    if request.method == 'POST':
        form = GiftForm(request.POST, request.FILES)
        if form.is_valid():
            gift = form.save(commit=False)
            gift.user = request.user
            gift.save()
            return redirect('gifts:gift_success')
    else:
        form = GiftForm()
    return render(request, 'gifts/be_santa.html', {'form': form})

@login_required
def gift_success_view(request):
    return render(request, 'gifts/success.html')
