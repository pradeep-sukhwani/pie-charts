from django.http import HttpResponseBadRequest
from rest_auth.views import LoginView
from rest_framework.generics import ListAPIView
from datetime import datetime

from rest_framework.response import Response

from api.serializers import ReportSerializer
from core.models import Login, Report


class LoginAPIView(LoginView):
    """
        ** Login API View **

            ** Override the Login View for ip address verification **

            ** returns: **

            * Auth Token:

            ** Required Fields: **
            * username: <string>
            * password: <string>
    """

    def post(self, request, *args, **kwargs):
        reponse_data = {}
        self.serializer = self.get_serializer(data=request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        ip_address = request.META.get('REMOTE_ADDR')
        login_queryset = Login.objects.filter(user__username=username)
        if login_queryset and ip_address != login_queryset.first().allowed_ip:
            reponse_data.update({'username': username,
                                 'error': 'User: {username} is not allowed to login from ip address: {ip_address}'.format(
                                     username=username, ip_address=ip_address)})
            return Response(reponse_data, status=HttpResponseBadRequest.status_code)
        self.login()
        return self.get_response()


class ClassAPIView(ListAPIView):
    """
            **Class API View**

                This api is for the reports based on the class

                ** returns: **

                * List of report objects categorised as total_students, fail_students, pass_students: *
                * students:
                    * name: <string>
                    * id: <int>
                *std: <string>
                *year: <int>
                *sci: <float>
                *math: <float>
                *language: <float>
                *social: <float>
                *total: <float>
                *grade: <string>
                *pass_fail: <boolean>

                ** Required Fields: **
                * data: <string>
        """
    serializer_class = ReportSerializer
    queryset = Report.objects.filter(year__gte=int(datetime.today().year) - 5)

    def get_queryset(self):
        return self.queryset.filter(std=self.request.GET.get('data'))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        total_students_serializer = self.get_serializer(queryset, many=True)
        fail_students_serializer = self.get_serializer(queryset.filter(pass_fail=False), many=True)
        pass_students_serializer = self.get_serializer(queryset.filter(pass_fail=True), many=True)
        data = {
            'total_students': total_students_serializer.data, 'fail_students': fail_students_serializer.data,
            'pass_students': pass_students_serializer.data}
        return Response(data)


class StudentAPIView(ListAPIView):
    """
                **Student API View**

                    This api is for the particular student based on the name/id

                    ** returns: **

                    * Report object: *
                    * students:
                        * name: <string>
                        * id: <int>
                    *std: <string>
                    *year: <int>
                    *sci: <float>
                    *math: <float>
                    *language: <float>
                    *social: <float>
                    *total: <float>
                    *grade: <string>
                    *pass_fail: <boolean>

                    ** Required Fields: **
                    * data: <string> - for name/<int> - for id
            """
    serializer_class = ReportSerializer
    queryset = Report.objects.filter(year__gte=int(datetime.today().year) - 5)

    def get_queryset(self):
        student_name_or_id = self.request.GET.get('data')
        if student_name_or_id:
            try:
                return self.queryset.filter(students__id=int(student_name_or_id))
            except ValueError:
                return self.queryset.filter(students__name__icontains=student_name_or_id)
        else:
            return []


class YearAPIView(ListAPIView):
    """
                **Year API View**

                    This api is based on the year

                    ** returns: **

                    * List of Report objects passed in that year: *
                    * students:
                        * name: <string>
                        * id: <int>
                    *std: <string>
                    *year: <int>
                    *sci: <float>
                    *math: <float>
                    *language: <float>
                    *social: <float>
                    *total: <float>
                    *grade: <string>
                    *pass_fail: <boolean>

                    ** Required Fields: **
                    * data: <int>
            """
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def get_queryset(self):
        try:
            int(self.request.GET.get('data'))
            return self.queryset.filter(year=self.request.GET.get('data'))
        except (ValueError, TypeError):
            return []
