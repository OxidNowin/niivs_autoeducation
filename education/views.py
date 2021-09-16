from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib import messages

from .models import UserCard, FirstEducation, PeriodEducation, Subdivision
from .forms import *

from quiz.models import *

import xlsxwriter


class SubdivisionName:
    """Вывод queryset подразделения"""

    def get_subdivisions(self):
        return Subdivision.objects.all()


class UserListView(SubdivisionName, View):
    """Список сотрудников"""

    def get(self, request):
        model = UserCard.objects.all()
        form = UserCardForm()
        context = {
            "model": model,
            "form": form,
            "sub": super().get_subdivisions()}
        return render(request, "education/usercard_list.html", context)

    def post(self, request):
        form = UserCardForm(request.POST)
        if form.is_valid():
            form.save()
            employee_name = form.cleaned_data['name']
            messages.success(request, f'Сотрудник {employee_name} успешно добавлен!')
        else:
            messages.error(request, 'Что-то пошло не так...')
        return redirect('usercard_list')


class UserDetailView(View):
    """Карточка сотрудника"""

    def get(self, request, pk, slug):
        context = {}
        try:
            model = UserCard.objects.get(id=pk)
            context.update({'model': model})
        except:
            messages.error(request, 'Сотрудник не найден')
        return render(request, "education/usercard_detail.html", context)

    def post(self, request, pk, slug):
        try:
            user_id = list(request.POST.values())[1]
            employee_name = UserCard.objects.get(id=user_id).name 
            UserCard.objects.get(id=user_id).delete()
        except UserCard.DoesNotExist:
            messages.error(request, 'Что-то пошло не так..')
        else:
            messages.success(request, f'Сотрудник {employee_name} удален')
        return redirect('usercard_list')


class FilterUserCardView(SubdivisionName, View):
    """Фильтр по подразделениям"""

    def get(self, request):
        model = UserCard.objects.filter(subdivision__in=self.request.GET.getlist('subdivision_name'))
        form = UserCardForm()
        context = {
            'model': model,
            'form': form,
            'sub': super().get_subdivisions()}
        return render(request, "education/usercard_list.html", context)


class FEducationView(SubdivisionName, View):
    """Список первичного обучения"""

    def get(self, request):
        model = FirstEducation.objects.all()
        form = FirstEducationForm()
        context = {
            'model': model,
            'form': form,
            "sub": super().get_subdivisions()}
        return render(request, "education/feducation.html", context)

    """Создание записи первичного обучения"""

    def post(self, request):
        form = FirstEducationForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = form.cleaned_data['user_name']
            employee_name = UserCard.objects.get(id=user_id.id)
            if FirstEducation.objects.filter(user_name_id=user_id).exists():
                messages.error(request, f'{employee_name} уже в списке первичного обучения')
            else:
                form.save()
                messages.success(request, f'Создано первичное обучение для {employee_name}')
        else:
            messages.error(request, 'Что-то пошло не так...')
        return redirect('feducation_view')


    def get_fedu_xl(self):
        """Формирование экселя по первичному обучению"""
        
        """Формирование словаря из бд"""
        users_data = UserCard.objects.all()
        fedu_dict = list(FirstEducation.objects.values())
        fedu_arr = []
        for dictionary in fedu_dict:
            fedu_arr.append([])
            u = users_data[dictionary['user_name_id']]
            fedu_arr[-1].append(u.name)
            fedu_arr[-1].append(u.subdivision.subdivision_name)
            fedu_arr[-1].append(u.receipt)
            fedu_arr[-1].append(dictionary['date'])

            if dictionary['estimate'] is True:
                estimate = "Сдал"
            else:
                estimate = "Не сдал"
            fedu_arr[-1].append(estimate)

            if not dictionary['fe_file']:
                has_file = "Нет"
            else:
                has_file = "Есть"
            fedu_arr[-1].append(has_file)

        """Создание эксель-респонса"""
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Otchet_o_pervichnom_obuchenii.xlsx"'
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet('Список сотрудников')
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 25)
        worksheet.set_column('F:F', 25)
        worksheet.set_column('G:G', 30)
        worksheet.set_row(0, 50)

        """Заголовки"""
        header_cells_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'align': 'vcenter',
            'valign': 'center',
            'border': 1,
            'color': '#000000',
            'fg_color': 'D0D0D0',
            'font_name': 'TimesNewRoman',
            'font_size': 16,
        })

        header_titles = [
            "№ п/п",
            "ФИО",
            "Подразделение",
            "Дата приема",
            "Дата сдачи первичного плана",
            "Отметка о сдаче первичного обучения",
            "Подтверждение о сдаче первичного обучения"
        ]

        value_cells_format = workbook.add_format({
            'border': 1,
            'font_name': 'TimesNewRoman',
            'font_size': 14,
        })

        date_format = workbook.add_format({
            'border': 1,
            'font_name': 'TimesNewRoman',
            'font_size': 14,
            'num_format': 'dd.mm.yyyy'
        })

        for col_num, data in enumerate(header_titles):
            worksheet.write(0, col_num, data, header_cells_format)

        for row_num, row_data in enumerate(fedu_arr):
            worksheet.write(row_num + 1, 0, row_num + 1, value_cells_format)
            for col_num, col_data in enumerate(row_data):
                if col_num == 3 or col_num == 2:
                    worksheet.write(row_num + 1, col_num + 1, col_data, date_format)
                else:
                    worksheet.write(row_num + 1, col_num + 1, col_data, value_cells_format)

        workbook.close()
        return response


class FilterFEducationView(SubdivisionName, View):
    """Фильтр по подразделениям"""

    def get(self, request):
        model = FirstEducation.objects.filter(
            user_name__subdivision__in=self.request.GET.getlist('subdivision_name')
        )
        form = FirstEducationForm()
        context = {
            'model': model,
            'form': form,
            'sub': super().get_subdivisions()
        }
        return render(request, "education/feducation.html", context)


class FEducationDetailView(View):
    """Первичное обучение сотрудника"""

    def get(self, request, pk):
        context = {}
        try:
            model = FirstEducation.objects.get(id=pk)
            #a_model = Answer.objects.filter(question_id__poll_id=model.test.id)
            #Инфа о сданном тесте
            context.update({
                'model': model,
                #'a_model': a_model,
            })
        except:
            messages.error(request, 'Первичное обучение не найдено')
        return render(request, "education/feducation_detail.html", context)

    """Удаление записи первичного обучения"""

    def post(self, request, pk):
        try:
            fedu_id = list(request.POST.values())[1]
            employee_name = FirstEducation.objects.get(id=fedu_id).user_name
            FirstEducation.objects.get(id=fedu_id).delete()
        except FirstEducation.DoesNotExist:
            messages.error(request, 'Что-то пошло не так...')
        else:
            messages.success(request, f'{employee_name} удален(а) из записей первичного обучения')
        return redirect("feducation_view")


class PEducationView(SubdivisionName, View):
    """Список периодического обучения"""

    def get(self, request):
        model = PeriodEducation.objects.all()
        form = PeriodEducationForm()
        context = {
            'model': model,
            'form': form,
            'sub': super().get_subdivisions()
        }
        return render(request, "education/peducation.html", context)

    """Создание записи периодического обучения"""

    def post(self, request):
        form = PeriodEducationForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = form.cleaned_data['user_name'].id
            employee_name = UserCard.objects.get(id=user_id)
            form.save()
            messages.success(request, f'Создано периодическое обучения для {employee_name}')
        else:
            messages.error(request, 'Что-то пошло не так..')
        return redirect('peducation_view')


class PEducationDetailView(View):
    """Периодическое обучение сотрудника"""

    def get(self, request, pk):
        context = {}
        try:
            model = PeriodEducation.objects.get(id=pk)
            context.update({'model':model})
        except:
            messages.error(request, 'Периодическое обуение не найдено')
        return render(request, "education/peducation_detail.html", context)

    """Удаление записи периодического обучения"""

    def post(self, request, pk):
        try:
            pedu_id = list(request.POST.values())[1]
            employee_name = PeriodEducation.objects.get(id=pedu_id).user_name
            PeriodEducation.objects.get(id=pedu_id).delete()
        except PeriodEducation.DoesNotExist:
            messages.error(request, 'Что-то пошло не так...')
        else:
            messages.success(request, f'{employee_name} удален(а) из записей периодического обучения')
        return redirect("peducation_view")


class FilterPEducationView(SubdivisionName, View):
    """Фильтр по подразделениям"""

    def get(self, request):
        model = PeriodEducation.objects.filter(
            user_name__subdivision__in=self.request.GET.getlist('subdivision_name')
        )
        form = PeriodEducationForm()
        context = {
            'model': model,
            'form': form,
            'sub': super().get_subdivisions()
        }
        return render(request, "education/peducation.html", context)

