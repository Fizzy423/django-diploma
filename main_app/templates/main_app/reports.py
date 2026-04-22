# main_app/reports.py
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from xhtml2pdf import pisa
import pandas as pd
from io import BytesIO
from .models import Abiturient, Dogovor

def render_to_pdf(template_src, context_dict):
    """Конвертация HTML в PDF"""
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def abiturient_report_pdf(request):
    """Отчет по абитуриентам в PDF"""
    abiturients = Abiturient.objects.select_related('specialnost').all()
    context = {
        'abiturients': abiturients,
        'total_count': abiturients.count(),
        'by_class': {
            '9': abiturients.filter(class_of_entry='9').count(),
            '11': abiturients.filter(class_of_entry='11').count(),
        },
        'generated_date': timezone.now(),
    }
    return render_to_pdf('main_app/reports/abiturient_report.html', context)

def dogovor_report_excel(request):
    """Отчет по договорам в Excel"""
    dogovors = Dogovor.objects.select_related('abiturient', 'roditel_zakazchik').all()
    
    data = []
    for d in dogovors:
        data.append({
            'Номер договора': d.number,
            'Дата заключения': d.date_of_conclusion,
            'Абитуриент': d.abiturient.fio if d.abiturient else '',
            'Форма оплаты': d.get_payment_form_display(),
            'Материнский капитал': 'Да' if d.maternity_capital else 'Нет',
            'Кредит': 'Да' if d.credit else 'Нет',
            'Родитель-заказчик': d.roditel_zakazchik.fio if d.roditel_zakazchik else '',
        })
    
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="dogovors_report.xlsx"'
    df.to_excel(response, index=False, sheet_name='Договоры')
    return response

def dashboard_report(request):
    """Сводный отчет по дашборду"""
    context = {
        'total_abiturients': Abiturient.objects.count(),
        'total_students': Abiturient.objects.filter(status='student').count(),
        'total_dogovors': Dogovor.objects.count(),
        'by_specialnost': Abiturient.objects.values('specialnost__name').annotate(count=models.Count('id')),
        'by_payment_form': Dogovor.objects.values('payment_form').annotate(count=models.Count('id')),
        'monthly_stats': Dogovor.objects.filter(
            date_of_conclusion__year=timezone.now().year
        ).values('date_of_conclusion__month').annotate(count=models.Count('id')),
    }
    return render(request, 'main_app/reports/dashboard_report.html', context)