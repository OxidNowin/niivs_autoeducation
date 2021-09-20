from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib import messages

from account.admin import UserCreationForm

from .models import User, Subdivision


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
            model = User.objects.get(id=pk)
            context.update({'model': model})
        except:
            messages.error(request, 'Сотрудник не найден')
        return render(request, "account/usercard_detail.html", context)

    def post(self, request, pk, slug):
        try:
            user_id = list(request.POST.values())[1]
            employee_name = User.objects.get(id=user_id).name 
            User.objects.get(id=user_id).delete()
        except User.DoesNotExist:
            messages.error(request, 'Что-то пошло не так..')
        else:
            messages.success(request, f'Сотрудник {employee_name} удален')
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
