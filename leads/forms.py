from django import forms 
from leads.models import Agent, Lead
from django.contrib.auth.forms import UserCreationForm
from leads.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from leads.models import BackGround

User = get_user_model()

class LeadModelForm(forms.ModelForm):

    class Meta:
        model = Lead 
        fields = (
            '__all__'
        )

class LeadForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)

class CustomeUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}

class AssignAgentForm(forms.Form):

    """agent = forms.ChoiceField(choices=(
        ("Agent 1", "Agent 1 Full name"),
        ("Agent 2", "Agent 2 Full name")
    ))"""
    agent = forms.ModelChoiceField(
        queryset=Agent.objects.none()
    )

    def __init__(self, *args, **kwargs):

        request = kwargs.pop("request")
        #print(request.user)
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        #self.fields["agent"].queryset = agents
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents
    
class LeadCategoryUpdateForm(forms.ModelForm):

    class Meta:
        model = Lead 
        fields = (
            'category',
        )
    
class BackGroundForm(forms.ModelForm):

    class Meta:

        model = BackGround
        fields = (
            'image',
        )