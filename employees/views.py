from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employee_list_create(request):
    if request.method == 'GET':
        # Filtering and Pagination
        department = request.query_params.get('department')
        role = request.query_params.get('role')
        employees = Employee.objects.all()

        if department:
            employees = employees.filter(department=department)
        if role:
            employees = employees.filter(role=role)

        paginator = Paginator(employees, 10)  # 10 employees per page
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)

        serializer = EmployeeSerializer(page_obj, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
