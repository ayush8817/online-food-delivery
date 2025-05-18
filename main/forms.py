from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'address', 'phone_number', 'scheduled_time']
        widgets = {
            'scheduled_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'  # This ensures compatibility with HTML5 datetime-local
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheduled_time'].input_formats = ['%Y-%m-%dT%H:%M']
