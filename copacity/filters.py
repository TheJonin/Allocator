# Filtering for project list to be worked on latter



import django_filters
# from model import Product
# from django.db.models import Q
# import datetime


# class Filtered_Project_list(django_filters.FilterSet):
    
#     class Meta:
#         model = Product
#         fields = ['start_date','end_date']
            
#         now = datetime.datetime.now()        
#         def Active(self, value, queryset):
#             qs_Active = queryset.filter(Q(start_date__lte=now.date())|Q(end_date__gte=now.date())).order_by('-date')
#             return qs_Active
        
#         def Past(self):
#             qs_Past = queryset.filter(end_date__lte=now.date()).order_by('-date')
#             return qs_Past
            
        
#         def Future(self):
#             qs_future = queryset.filter(start_date__gte=now.date()).order_by('-date')
#             return qs_future
            
#         def All(self):
#             qs_All = queryset.order_by('-date') 
#             return qs_All


