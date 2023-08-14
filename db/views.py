from django.shortcuts import render
from django.db.models import Sum
import matplotlib
from rest_framework import status
from .models import Electrify
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
import io
import plotly.graph_objs as go
import matplotlib.pyplot as plt
matplotlib.use('agg')  # Use the 'agg' backend (non-GUI)
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
# Create your views here.
from django.utils import timezone
class TotalUnit(viewsets.ViewSet):
    def list(self, request):
        today = timezone.now()
        two_months_ago = today - timedelta(days=60)

        total_units = Electrify.objects.filter(date__gte=two_months_ago).aggregate(total_units=Sum('units'))['total_units']
        total_cost = Electrify.objects.filter(date__gte=two_months_ago).aggregate(total_cost=Sum('cost'))['total_cost']

        return Response({'total_units': total_units, 'total_cost': total_cost})

class Last24HoursData(viewsets.ViewSet):
    def list(self, request):
        now = timezone.now()
        last_24_hours = now - timedelta(hours=24)

        total_units = Electrify.objects.filter(date__gte=last_24_hours).aggregate(total_units=Sum('units'))['total_units']
        total_cost = Electrify.objects.filter(date__gte=last_24_hours).aggregate(total_cost=Sum('cost'))['total_cost']

        return Response({'total_units_last_24_hours': total_units, 'total_cost_last_24_hours': total_cost})

    
class InsertData(viewsets.ViewSet):
    def create(self, request):
        try:
            date = request.data.get('date')
            today_units = request.data.get('today')
            user = "admin"
            f = 1
            # Find the latest record for the user
            try:
                latest_record = Electrify.objects.filter(user=user).latest('id')
                prev_units = latest_record.units
            except Electrify.DoesNotExist:
                f = 0
                prev_units = 0
                cost = 0
                units=0

            if f == 1:
                units = today_units - prev_units
                if units <= 200:
                    if units <= 50:
                        cost = units * 3.15
                    elif units <= 100:
                        cost = units * 3.95
                    elif units <= 150:
                        cost = units * 5
                    else:
                        cost = units * 6.8
                else:
                    if units <= 250:
                        cost = units * 8
                    elif units <= 300:
                        cost = units * 6.2
                    elif units <= 400:
                        cost = units * 7.0
                    elif units <= 500:
                        cost = units * 7.6
                    else:
                        cost = units * 8.5

            record = Electrify(user=user, date=date, units=today_units,unit=units, cost=cost)
            record.save()

            return Response({"message": "Data Inserted"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class FetchAllData(viewsets.ViewSet):
    def list(self, request):
        try:
            data = Electrify.objects.all()
            return Response({'data': data.values()}, status=200)  # 200 OK
        except Exception as e:
            return Response({'error': str(e)}, status=400)  # 400 Bad Request
        
class DataGraphPlotter(viewsets.ViewSet):
    def create(self, request):
        pass

    def get(self, request):
        data = Electrify.objects.all()
        units = [entry.unit for entry in data]
        cost = [entry.cost for entry in data]
        dates = [entry.date for entry in data]

        fig = go.Figure()

        # Get the current month
        current_month = datetime.now().month

        # Filter the dates and units for the current month
        current_month_data = [(date, unit) for date, unit in zip(dates, units) if date.month == current_month]
        costs = [(date, c) for date, c in zip(dates, cost) if date.month == current_month]
        unit_values = [unit for _, unit in costs]
        print(unit_values)
        # Extract days and units of the current month for x-axis and y-axis
        x_ticks = [date.day for date, _ in current_month_data]
        y_units = [unit for _, unit in current_month_data]

        # Create a line plot for the current month's data
        line_trace = go.Scatter(
            x=x_ticks,
            y=y_units,
            mode='lines+markers',
            name='Units',
            text=[f'Day {day}: {unit}' for day, unit in zip(x_ticks, y_units)],
            hoverinfo='text+y',
            marker=dict(
                size=10,
                color=unit_values,
                colorbar=dict(title='Cost'),
                colorscale='bluered',
                showscale=True
            )
        )
        fig.add_trace(line_trace)

        # Update layout
        fig.update_layout(
            title='Data Plot',
            xaxis_title='Day',
            yaxis_title='Units',
            hovermode='closest',
            xaxis=dict(
                tickmode='linear',  # Set tick mode to linear
                tickvals=x_ticks,   # Set tick values to the days
                ticktext=[f'Day {day}' for day in x_ticks],  # Display tick labels as Day X
            ),
            yaxis=dict(type='linear', range=[0, max(y_units) + 1]),  # Scaled y-axis range
        )
        # Create a BytesIO buffer to save the plot
        buffer = io.BytesIO()
        fig.write_image(buffer, format='png')
        buffer.seek(0)

        # Create a Django HttpResponse with the image data
        response = HttpResponse(buffer, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="data_plot.png"'

        return response
class DataFilterGraphPlotter(viewsets.ViewSet):
    def create(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        data = Electrify.objects.filter(date__range=(start_date, end_date))  # Fetch all rows from the database
        units = [entry.units for entry in data]
        cost = [entry.cost for entry in data]

        fig, ax = plt.subplots()

        ax.set_xlabel('Cost')
        ax.set_ylabel('Unit', color='tab:blue')
        
        # Plot "Units" as blue dots and lines
        ax.plot(cost, units, color='tab:blue', marker='o', label='Units')
        ax.tick_params(axis='y', labelcolor='tab:blue')

        fig.tight_layout()

        # Save the plot as an image in memory
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close(fig)

        # Create a Django HttpResponse with the image data
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="data_plot.png"'

        return response


















