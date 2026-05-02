from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from datetime import timedelta

from . import forms
from . import models


class PanelView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile

        range_type = request.GET.get('range', 'all')
        today = timezone.now().date()

        if range_type == 'this-week':
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            transactions = profile.transactions.filter(
                date__range=(start_week, end_week)
            )

        elif range_type == 'this-month':
            transactions = profile.transactions.filter(
                date__year=today.year,
                date__month=today.month
            )

        elif range_type == 'last-month':
            last_month = today.replace(day=1) - timedelta(days=1)
            transactions = profile.transactions.filter(
                date__year=last_month.year,
                date__month=last_month.month
            )

        elif range_type == 'this-year':
            transactions = profile.transactions.filter(
                date__year=today.year
            )

        else:
            transactions = profile.transactions.all()

        financial_targets = profile.financial_targets.all()
        return render(request, 'panel/index.html', {
            'profile': profile,
            'transactions': transactions,
            'range_type': range_type,
            'financial_targets': financial_targets,
        })


class TransactionView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.TransactionForm()
        return render(request, 'panel/transaction.html', {'form': form})

    def post(self, request):
        form = forms.TransactionForm(request.POST)
        user = request.user.profile
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = user
            transaction.save()
            return redirect('panel')

        return render(request, 'panel/transaction.html', {
            'form': form
        })


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile_form = forms.EditProfileForm(
            initial={'first_name': user.first_name, 'last_name': user.last_name}
        )
        avatar_form = forms.EditAvatarForm()
        password_edit_form = forms.EditPasswordForm(user=user)
        return render(request, 'panel/profile.html', {
            'avatar_form': avatar_form,
            'profile_form': profile_form,
            'password_form': password_edit_form,
        })

    def post(self, request):
        user = request.user
        form_type = request.POST.get('form_type')

        if form_type == 'avatar':
            avatar_form = forms.EditAvatarForm(
                request.POST, request.FILES, instance=user.profile
            )
            if avatar_form.is_valid():
                avatar_form.save()

                return redirect('profile')
            else:
                profile_form = forms.EditProfileForm(
                    initial={'first_name': user.first_name, 'last_name': user.last_name}
                )
                password_edit_form = forms.EditPasswordForm(user=user)
                return render(request, 'panel/profile.html', {
                    'avatar_form': avatar_form,
                    'profile_form': profile_form,
                    'password_form': password_edit_form,
                })

        elif form_type == 'profile':
            profile_form = forms.EditProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
            else:
                avatar_form = forms.EditAvatarForm()
                password_edit_form = forms.EditPasswordForm(user=user)
                return render(request, 'panel/profile.html', {
                    'avatar_form': avatar_form,
                    'profile_form': profile_form,
                    'password_form': password_edit_form,
                })

        elif form_type == 'password':
            password_edit_form = forms.EditPasswordForm(
                user=user, data=request.POST
            )
            if password_edit_form.is_valid():
                password_edit_form.save()
                return redirect('profile')
            else:
                profile_form = forms.EditProfileForm(
                    initial={'first_name': user.first_name, 'last_name': user.last_name}
                )
                avatar_form = forms.EditAvatarForm()
                return render(request, 'panel/profile.html', {
                    'avatar_form': avatar_form,
                    'profile_form': profile_form,
                    'password_form': password_edit_form,
                })

        return HttpResponseBadRequest('مشکلی پیش آمده است.')


class ReportsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.profile

        category = request.GET.get('type')

        categories = ['salary', 'food', 'clothes', 'transportation',
                      'hobby', 'health', 'investment', 'loan', 'rent', 'bill']

        if category in categories and category != 'all':
            transaction = user.transactions.filter(
                category=category
            ).order_by('-date')[:50]

        else:
            transaction = user.transactions.order_by('-date')[:50]

        return render(request, 'panel/reports.html', {
            'transactions': transaction,
            'category': category
        })


class FinancialTargetAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.FinancialTargetForm()
        return render(request, 'panel/financial_target.html', {'form': form})

    def post(self, request):
        form = forms.FinancialTargetForm(request.POST)
        if form.is_valid():
            target = form.save(commit=False)
            target.user = request.user.profile
            target.save()
            return redirect('panel')
        return render(request, 'panel/financial_target.html', {'form': form})


class FinancialTargetDoneView(LoginRequiredMixin, View):
    def get(self, request, pk):
        models.FinancialTarget.objects.filter(pk=pk, user=request.user.profile).update(is_done=True)
        return redirect('panel')


class FinancialTargetRemoveView(LoginRequiredMixin, View):
    def get(self, request, pk):
        models.FinancialTarget.objects.filter(pk=pk, user=request.user.profile).delete()
        return redirect('panel')


class ProfilePictureView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        path = user.profile.profile_picture.path

        if not path:
            return None

        return FileResponse(open(path, 'rb'))
