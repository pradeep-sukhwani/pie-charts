from django.urls import reverse
from django.views.generic import TemplateView


class StatisticsTemplateView(TemplateView):
    template_name = 'statistical-data.html'

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        allowed_search_text = ['class', 'student', 'year']
        search_text = self.kwargs.get('search_text')
        if search_text in allowed_search_text and self.request.user.is_authenticated:
            if search_text == 'class':
                context.update({'query_from': 'Class wise', 'placeholder': 'Enter Class/Standard Name'})
            elif search_text == 'student':
                context.update({'query_from': 'Student wise', 'placeholder': 'Enter Student Name/ID'})
            elif search_text == 'year':
                context.update({'query_from': 'Yearly', 'placeholder': "Enter Student's passing Year"})
        else:
            self.template_name = '404.html'
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )


class HomeTemplateView(TemplateView):
    template_name = 'home.html'
