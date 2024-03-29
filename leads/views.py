from unicodedata import category
from django.shortcuts import render
from django.http import HttpResponse
from leads.models import Agent, Category, Lead, UserProfile
from leads.forms import LeadForm, LeadModelForm
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from leads.forms import CustomeUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
from django.views.generic import FormView
from leads.forms import AssignAgentForm
from leads.forms import LeadCategoryUpdateForm
from leads.forms import BackGroundForm
from leads.models import BackGround
#CRUD + L - Create, Retrieve, Update and Delete + List


class SignUpView(CreateView):

    template_name = 'registration/signup.html'
    form_class = CustomeUserCreationForm

    def get_success_url(self):
        return reverse('login')


class LandingPageView(TemplateView):

    template_name = 'landing.html'


"""def landing_page(request):

    return render(request, 'landing.html')"""

class LeadListView(LoginRequiredMixin,ListView):

    template_name = 'leads/lead_list.html'
    #queryset = Lead.objects.all()
    context_object_name = 'leads'
    
    def get_queryset(self):

        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
                agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):

        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context

"""def lead_list(request):
    #return HttpResponse('Hello!')
    leads = Lead.objects.all()
    #context = { 
    #    "name": "Mason",
    #    "age" : 32,
    #}
    context = {
        "leads": leads
    }
    return render(request, 'leads/lead_list.html', context )"""

class LeadDetailView(LoginRequiredMixin, DetailView):

    template_name = 'leads/lead_detail.html'
    #queryset = Lead.objects.all()
    context_object_name = 'lead'

    def get_queryset(self):

        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset


"""def lead_detail(request, pk):

    lead = Lead.objects.get(id=pk)
    context = {
        'lead' : lead
    }
    #return HttpResponse("Here is the detail view")
    return render(request, 'leads/lead_detail.html', context)"""

class LeadCreateView(OrganisorAndLoginRequiredMixin, CreateView):

    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):

        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        #Todo send email
        send_mail(
            subject="A lead has been created",
            message="Go to the site",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

"""def lead_create(request):

    #print(request.POST)
    form = LeadModelForm()
    if request.method == "POST":
        print("Receiving post request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form": form
    }
    return render(request, 'leads/lead_create.html', context)"""

class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):

    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm
    #queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def get_queryset(self):
        
        #Initial queryset of leads for the entire organisation
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

"""def lead_update(request, pk):

    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        print("Receiving post request")
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, 'leads/lead_update.html', context)"""

class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):

    template_name = "leads/lead_delete.html"
    #queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def get_queryset(self):
        
        #Initial queryset of leads for the entire organisation
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
        

"""def lead_delete(request, pk):

    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')
"""

class AssignAgentView(OrganisorAndLoginRequiredMixin, FormView):

    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        """return {
            "request": self.request
        }
        """
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):

        #print(form.cleaned_data["agent"])
        #print(form.data)
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent 
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, ListView):

    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):

        context = super(CategoryListView, self).get_context_data(**kwargs)
        
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
                )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):

        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile, 
                )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation, 
                )
        return queryset

class CategoryDetailView(LoginRequiredMixin, DetailView):

    template_name = "leads/category_detail.html"
    context_object_name = "category"

    """def get_context_data(self, **kwargs):

        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        leads = self.get_object().leads.all()
        context.update({
            "leads": leads
        })
        return context"""

    def get_queryset(self):

        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile, 
                )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation, 
                )
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm
    #queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-detail', kwargs={"pk":self.get_object().id})
    
    def get_queryset(self):

        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

def BackGroundView(request):

    if request.method == 'POST':  
        form = BackGroundForm(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
  
            # Getting the current instance object to display in the template  
            img_object = form.instance  
              
            return render(request, 'image_form.html', {'img_obj': img_object})  
    else:  
        form = BackGroundForm()  
  
    return render(request, 'image_form.html', {'form': form})  

"""def lead_update(request, pk):

    lead = Lead.objects.get(id=pk)
    form = LeadForm()
    if request.method == "POST":
        print("Receiving post request")
        form = LeadForm(request.POST)
        if form.is_valid():
            print('The form is valid')
            print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            lead.first_name = first_name
            lead.last_name = last_name
            lead.age = age
            lead.save()
            print("The Lead has been created")
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, 'leads/lead_update.html', context)
"""
"""def lead_create(request):

    #print(request.POST)
    form = LeadForm()
    if request.method == "POST":
        print("Receiving post request")
        form = LeadForm(request.POST)
        if form.is_valid():
            print('The form is valid')
            print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = Agent.objects.first()
            Lead.objects.create(
                first_name = first_name,
                last_name = last_name,
                age = age,
                agent = agent
            )
            print("The Lead has been created")
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, 'leads/lead_create.html', context)"""

# CTRL + k CTRL + 0