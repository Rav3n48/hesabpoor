from django.urls import path
from . import financial_target_page_view, panel_page_view, profile_page_view, reports_page_view, transaction_page_view, profile_picture, logout

urlpatterns = [
    path("", panel_page_view.panel_page, name="panel-page"),
    path("transaction/", transaction_page_view.transactions_page, name="transaction-page"),
    path("reports/", reports_page_view.reports_page, name="reports-page"),
    path("profile/", profile_page_view.profile_page, name="profile-page"),
    path("profile_picture/", profile_picture.profile_picture_display, name="profile-pic"),
    path("financial_target/", financial_target_page_view.financial_target_page, name="financial-target"),
    path("logout/", logout.logout, name="logout")
]
