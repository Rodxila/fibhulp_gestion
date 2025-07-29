from django.shortcuts import render, redirect
from .models import DatosEnsayo
from .forms import DatosEnsayoForm
import json

def index(request):
    if request.method == 'POST':
        form = DatosEnsayoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DatosEnsayoForm()

    datos = DatosEnsayo.objects.all()
    chart_data = {
        'labels': [d.mes for d in datos],
        'ensayos': [d.ensayos for d in datos],
        'observacionales': [d.observacionales for d in datos],
        'adendas': [d.adendas for d in datos],
    }

    return render(request, 'index.html', {
        'form': form,
        'chart_data': json.dumps(chart_data)
    })
