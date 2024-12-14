from django import forms
from .models import Expense, Category

class ExpenseForm(forms.ModelForm):

    try:
        default_categories = Category.objects.all()
    except:
        default_categories = None

    category = forms.ModelChoiceField(
        queryset= default_categories,
        empty_label="Select a category",
        required=False,
    )

    new_category = forms.CharField(
        max_length=100, 
        required=False, 
        label="Or create a new category"
    )

    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'enter a note'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Get default and user-specific categories
        if user:
            default_categories = Category.objects.filter(is_default=True)
            user_categories = Category.objects.filter(user=user)
            self.fields['category'].queryset = default_categories | user_categories

    def save(self, commit=True):
        # Check if a new category was added
        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            category, created = Category.objects.get_or_create(
                name=new_category_name,
                user=self.instance.user if self.instance.user_id else None
            )
            self.cleaned_data['category'] = category

        return super().save(commit)