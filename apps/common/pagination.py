from rest_framework.pagination import PageNumberPagination as DRFPageNumberPagination
from rest_framework.response import Response

class PageNumberPagination(DRFPageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'total_pages': {
                    'type': 'integer',
                    'example': 10
                },
                'results': schema
            }
        }

class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
