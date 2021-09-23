from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib import messages

from account.admin import UserCreationForm

from .models import User, Subdivision
from .admin import UserChangeForm


class SubdivisionName:
    """Вывод queryset подразделения"""

    def get_subdivisions(self):
        return Subdivision.objects.all()


class UserListView(SubdivisionName, View):
    """Список сотрудников"""

    def get(self, request):
        model = User.objects.all()
        form = UserCreationForm()
        context = {
            "model": model,
            "form": form,
            "sub": super().get_subdivisions()}
        return render(request, "account/usercard_list.html", context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            employee_name = form.cleaned_data['name']
            messages.success(request, f'Сотрудник {employee_name} успешно добавлен!')
        else:
            messages.error(request, 'Что-то пошло не так...')
        return redirect('user_list')


class UserDetailView(View):
    """Карточка сотрудника"""

    def get(self, request, pk, slug):
        context = {}
        try:
            user = User.objects.get(id=pk)
            form = UserChangeForm(initial={
                'email': user.email,
                'name': user.name,
                'subdivision': user.subdivision,
                'education': user.education,
                'education_profile': user.education_profile,
                'receipt': user.receipt,
                })
            context.update({
                'form': form,
                })
        except:
            messages.error(request, 'Сотрудник не найден')
        return render(request, "account/usercard_detail.html", context)

    def post(self, request, pk, slug):
        if 'delete_user' in request.POST:
            try:
                user = User.objects.get(id=pk)
                user.delete()
            except User.DoesNotExist:
                messages.error(request, 'Что-то пошло не так..')
                return redirect('user_detail', pk=pk, slug=slug)
            else:
                messages.success(request, f'Сотрудник {user.name} удален')
            return redirect('user_list')


class FilterUserView(SubdivisionName, View):
    """Фильтр по подразделениям"""

    def get(self, request):
        model = User.objects.filter(subdivision__in=self.request.GET.getlist('subdivision_name'))
        form = UserCreationForm()
        context = {
            'model': model,
            'form': form,
            'sub': super().get_subdivisions()}
        return render(request, "account/usercard_list.html", context)


class LoginView(View):
    """Страница входа"""
    def get(self, request):
        return render(request, 'registration/login.html')