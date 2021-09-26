from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, Subdivision
from .forms import UserCreationForm, UserChangeForm


class SubdivisionName:
    """Вывод queryset подразделения"""

    def get_subdivisions(self):
        return Subdivision.objects.all()


class UserListView(SubdivisionName, View):
    """Список сотрудников"""
    #login_url = 'user_list'
    #redirect_field_name = 'login_view'

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
    """Логин пользователя""" 
 
    def get(self, request):
        """Предоставить страницу входа пользователя"""
        return render(request, 'registration/login.html')
 
    def post(self, request):
        """Реализовать логику входа пользователя"""
                 # Параметры приема
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return render (request, 'login.html', {'account_errmsg': 'Ошибка аккаунта или пароля'})
            # Государственный замок
        login(request, user)
        if remembered != 'on':
            # Не забыл войти в систему: состояние остается разрушенным после завершения сеанса браузера
            request.session.set_expiry(0) # Единица измерения - секунды
        else:
            # Не забудьте войти в систему: срок хранения состояния составляет две недели (по умолчанию - две недели)
            request.session.set_expiry(3600)

         # Результат ответа
         # Сначала достать следующий
        next = request.GET.get('next')
        if next:
                         # Перенаправить на следующий
            response = redirect(next)
        else:
                         # Перенаправить на домашнюю страницу
            response = redirect(reverse('contents:index'))
 
                 # Чтобы отображать информацию об имени пользователя в правом верхнем углу домашней страницы, нам нужно кэшировать имя пользователя в cookie
        # response.set_cookie('key', 'value', 'expiry')
        response.set_cookie('username', user.username, max_age=3600)
                 # Результат ответа: перенаправление на домашнюю страницу
        return response