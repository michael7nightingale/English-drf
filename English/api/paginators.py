from rest_framework.pagination import PageNumberPagination


class MessagesListPaginator(PageNumberPagination):
    page_size = 300
    page_size_query_param = "page_size"
    max_page_size = 10000
