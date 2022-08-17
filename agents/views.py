from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.shortcuts import reverse
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth.models import User
from random import randint
from web.encrypt_util import *

#from .mixins import OrganisorAndLoginRequiredMixin - Создай свой миксин. Если пользватель не супер админ

class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):

    template_name = 'agents/agent_list.html'
    
    def get_queryset(self):
        
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):

    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm  

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def form_valid(self, form):

        """agent = form.save(commit=False)
        agent.organisation = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)"""

        user = form.save(commit=False)
        user.is_agent = True 
        user.is_organisor = False
        user.set_password(str(randint(0,10000000)))
        user.save()
        Agent.objects.create(
            user = user,
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on Militech CRM. Please come login to start working.",
            from_email="atabekdemurtaza@gmail.com",
            recipient_list=[user.email]
        )
        encryptpass= encrypt(self.request.user.password)
        #print(encryptpass)
        decryptpass= decrypt(encryptpass)
        #print(decryptpass)
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):

    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):

    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):

    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    





 