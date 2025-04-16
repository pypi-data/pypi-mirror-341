"""Practitioner views."""

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import PractitionerFilter
from .models import (
    Practitioner,
    PractitionerRole,
    PractitionerRoleCode,
)
from .serializers import (
    PractitionerSerializer,
    PractitionerRoleCodeSerializer,
    PractitionerRoleSerializer,
    PractitionerRoleWithPractitionerIdSerializer,
)


class PractitionerListView(APIView):
    """Practitioner list view."""

    permission_classes = [AllowAny]

    @extend_schema(responses={200: PractitionerSerializer(many=True)})
    def get(self, request, pk=None):
        """Get practitioners."""
        queryset = Practitioner.objects.all()
        practitioners_filter = PractitionerFilter(request.GET, queryset=queryset)
        serializer = PractitionerSerializer(practitioners_filter.qs, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=PractitionerSerializer, responses={200: PractitionerSerializer}
    )
    def post(self, request):
        """Create a practitioner."""
        request_data = request.data
        request_data.pop("user", None)

        serializer = PractitionerSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PractitionerDetailView(APIView):
    """Practitioner detail view."""

    permission_classes = [AllowAny]

    def get_object(self, pk):
        """Get practitioner object."""
        try:
            return Practitioner.objects.get(pk=pk)
        except Practitioner.DoesNotExist as err:
            raise Http404 from err

    @extend_schema(responses={200: PractitionerSerializer})
    def get(self, request, pk=None):
        """Get a practitioner."""
        queryset = self.get_object(pk)
        serializer = PractitionerSerializer(queryset)
        return Response(serializer.data)

    @extend_schema(responses={200: PractitionerSerializer})
    def patch(self, request, pk=None):
        """Update a practitioner."""
        queryset = self.get_object(pk)
        serializer = PractitionerSerializer(
            queryset, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        """Delete a practitioner."""
        practitioner = self.get_object(pk)
        practitioner.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PractitionerRoleListView(APIView):
    """Practitioner role list view."""

    permission_classes = [AllowAny]

    @extend_schema(responses={200: PractitionerRoleWithPractitionerIdSerializer})
    def get(self, request, pk=None):
        """Get practitioner roles."""
        queryset = PractitionerRole.objects.all()
        serializer = PractitionerRoleSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=PractitionerRoleSerializer,
        responses={200: PractitionerRoleWithPractitionerIdSerializer},
    )
    def post(self, request):
        """Create a practitioner role."""
        request_data = request.data
        serializer = PractitionerRoleSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PractitionerRoleDetailView(APIView):
    """Practitioner role detail view."""

    def get_object(self, pk):
        """Get practitioner role object."""
        try:
            return PractitionerRole.objects.get(pk=pk)
        except PractitionerRole.DoesNotExist as err:
            raise Http404 from err

    @extend_schema(responses={200: PractitionerRoleWithPractitionerIdSerializer})
    def get(self, request, pk=None):
        """Get a practitioner role."""
        queryset = self.get_object(pk)
        serializer = PractitionerRoleSerializer(queryset)
        return Response(serializer.data)

    @extend_schema(responses={200: PractitionerRoleWithPractitionerIdSerializer})
    def patch(self, request, pk=None):
        """Update a practitioner role."""
        queryset = self.get_object(pk)
        serializer = PractitionerRoleSerializer(
            queryset, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        """Delete a practitioner role."""
        practitioner_role = self.get_object(pk)
        practitioner_role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PractitionerRoleCodeListView(APIView):
    """Practitioner role code list view."""

    permission_classes = [AllowAny]

    @extend_schema(responses={200: PractitionerRoleCodeSerializer})
    def get(self, request, pk=None):
        """Get practitioner role codes."""
        queryset = PractitionerRoleCode.objects.all()
        serializer = PractitionerRoleCodeSerializer(queryset, many=True)
        return Response(serializer.data)
