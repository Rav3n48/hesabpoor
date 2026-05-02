from django.urls import path
from . import views

urlpatterns = [
    path("", views.PanelView.as_view(), name="panel"),
    path("transaction/", views.TransactionView.as_view(), name="transaction"),
    path("reports/", views.ReportsView.as_view(), name="reports"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile_picture/", views.ProfilePictureView.as_view(), name="profile_picture"),
    path("financial_target/add/", views.FinancialTargetAddView.as_view(), name="financial_target_add"),
    path("financial_target/done/<int:pk>", views.FinancialTargetDoneView.as_view(), name="financial_target_done"),
    path("financial_target/remove/<int:pk>", views.FinancialTargetRemoveView.as_view(), name="financial_target_remove"),
]
