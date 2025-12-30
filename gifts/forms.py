from django import forms
from .models import Gift

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ['image', 'note']
        widgets = {
            'note': forms.Textarea(attrs={
                'class': 'w-full bg-black/20 border border-white/10 rounded-xl px-5 py-4 text-white placeholder-white/30 focus:outline-none focus:border-gold-accent/50 transition-colors',
                'rows': 4,
                'placeholder': 'A few kind words, if you wish…'
            }),
            'image': forms.FileInput(attrs={
                'class': 'hidden',
                'id': 'image-upload',
                'accept': 'image/*'
            })
        }
