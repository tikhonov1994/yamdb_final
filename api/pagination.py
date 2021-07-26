from rest_framework import pagination
from rest_framework.response import Response


class CursorPagination(pagination.CursorPagination):
    ordering = '-id'

    def get_paginated_response(self, data):
        return Response({
            'count': len(data),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
