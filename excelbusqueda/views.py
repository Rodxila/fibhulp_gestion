from django.shortcuts import render
from .forms import ExcelSearchForm
import pandas as pd
from django.http import HttpResponse

def buscar_en_excel(request):
    resultados = []
    form = ExcelSearchForm()


    headers = []

    if request.method == 'POST':
        form = ExcelSearchForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            texto = form.cleaned_data['texto'].lower()

            try:
                df = pd.read_excel(archivo)
                headers = df.columns.tolist()  # <- extrae los nombres de columnas
                if df.shape[1] >= 3:
                    col_c = df.iloc[1:, 2].astype(str).str.lower()
                    resultados_df = df.iloc[1:][col_c.str.contains(texto, na=False)]
                    resultados = resultados_df.values.tolist()
                    request.session['resultados'] = resultados
                    request.session['headers'] = headers
            except Exception as e:
                form.add_error('archivo', f"Error al procesar el archivo: {e}")


    return render(request, 'excelbusqueda/buscar_excel.html', {
    'form': form,
    'resultados': resultados,
    'headers': headers,
})


def exportar_excel(request):
    from django.http import HttpResponse
    import pandas as pd

    resultados = request.session.get('resultados')
    headers = request.session.get('headers')

    if not resultados or not headers:
        return HttpResponse("No hay resultados para exportar", status=400)

    try:
        df_export = pd.DataFrame(resultados, columns=headers)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="resultados_filtrados.xlsx"'

        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df_export.to_excel(writer, index=False)

        request.session.pop('resultados', None)
        request.session.pop('headers', None)

        return response

    except Exception as e:
        return HttpResponse(f"Error al generar el archivo: {e}", status=500)
