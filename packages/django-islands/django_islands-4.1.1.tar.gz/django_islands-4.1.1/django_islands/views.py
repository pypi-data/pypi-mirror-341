# pylint: disable=unused-import
import django_islands.django_mt_environment
from django_islands.utils import set_current_tenant
from django_islands.models import TenantModel
from rest_framework import viewsets
from abc import abstractmethod


@abstractmethod
def get_tenant(request) -> TenantModel:
    pass


class TenantModelViewSet(viewsets.ModelViewSet):
    model_class = TenantModel

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return self.model_class.objects.none()
        tenant = get_tenant(self.request)
        set_current_tenant(tenant)
        list3 = self.model_class.objects.all()
        return list3
