from rest_framework.pagination import PaginationSerializer
from rest_framework import serializers


class PaginationSerializerWithPageNo(PaginationSerializer):
    page_no = serializers.Field(source='number')
    page_size = serializers.Field(source='paginator.per_page')
