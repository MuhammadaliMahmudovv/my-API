from rest_framework.pagination import PageNumberPagination


class PostPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page-size"
    max_page_size = 20
