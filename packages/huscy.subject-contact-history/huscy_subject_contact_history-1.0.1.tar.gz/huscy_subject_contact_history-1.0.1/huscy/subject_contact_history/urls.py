from huscy.subject_contact_history import views
from huscy.subjects.urls import subject_router


subject_router.register('contacthistory', views.ContactHistoryViewSet, basename='contacthistory')

urlpatterns = subject_router.urls
