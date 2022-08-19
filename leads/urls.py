from django.urls import path 
#from leads.views import lead_list
#from leads.views import lead_detail
#from leads.views import lead_create
#from leads.views import lead_update
#from leads.views import lead_delete
from leads.views import LeadListView
from leads.views import LeadDetailView
from leads.views import LeadCreateView
from leads.views import LeadUpdateView
from leads.views import LeadDeleteView
from leads.views import AssignAgentView
from leads.views import CategoryListView
from leads.views import CategoryDetailView
from leads.views import LeadCategoryUpdateView

app_name = 'leads'

urlpatterns = [

    #path('', lead_list, name='lead-list'),
    path('', LeadListView.as_view(), name='lead-list'),
    #path('<int:pk>/', lead_detail, name='lead-detail'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    #path('<int:pk>/update/', lead_update, name='lead-update'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    #path('<int:pk>/delete/', lead_delete, name='lead-delete'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    #path('create/', lead_create, name='lead-create')
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]

"""
    path('<pk>/', lead_detail),
    path('create/', lead_create)

    pk с create могут появится ошибка. чтобы избежать
    делаем int:pk
"""

"""
    Вместо этого, 
    <a href="/leads/{{lead.pk}}/update/">Update</a>
    напишем вот это!
    <a href="{% url 'leads:update' %}">Update</a>
"""

"""
    <a href="/leads/{{lead.pk}}/"></a>
    <a href="{% url 'leads:lead-detail' lead.pk %}"></a>
"""