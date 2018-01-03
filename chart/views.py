from django.shortcuts import render

from .chart import TimeSeriesChart


def some_view(request):
    return render(request, 'template.html', {
        'line_chart': TimeSeriesChart(),
    })
