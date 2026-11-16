# analyzerapp/forms.py

from django import forms
from .models import Candidate

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['resume_file']


from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
    class Meta:
        model = Candidate
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            
        
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = self.cleaned_data['password']  # ✅ save password to model
        if commit:
            instance.save()
        return instance
        
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')