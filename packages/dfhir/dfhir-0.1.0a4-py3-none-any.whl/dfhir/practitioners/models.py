"""Practitioner models."""
from django.db import models

from dfhir.base import choices as base_choices
from dfhir.base.models import (
    Address,
    Attachment,
    Availability,
    BaseReference,
    CodeableConcept,
    Communication,
    ContactPoint,
    ExtendedContactDetail,
    HumanName,
    Identifier,
    OrganizationReference,
    Period,
    Qualification,
    TimeStampedModel,
)
from dfhir.endpoints.models import EndpointReference
from dfhir.healthcareservices.models import (
    HealthCareServiceReference,
)
from dfhir.locations.models import LocationReference
from dfhir.organizations.models import Organization


class PractitionerReference(BaseReference):
    """Practitioner reference model."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.CASCADE,
        related_name="practitioner_reference_identifier",
        null=True,
    )
    practitioner = models.ForeignKey(
        "Practitioner",
        on_delete=models.CASCADE,
        related_name="practitioner_reference_practitioner",
        null=True,
    )


class PractitionerRoleCode(TimeStampedModel):
    """Practitioner Role Code model."""

    display = models.CharField(max_length=255)
    definition = models.TextField(null=True)


class Practitioner(TimeStampedModel):
    """Practitioner model."""

    identifier = models.ManyToManyField(
        Identifier, related_name="practitioner_identifier", blank=True
    )
    active = models.BooleanField(default=True)
    name = models.ManyToManyField(
        HumanName, related_name="practitioner_name", blank=True
    )
    telecom = models.ManyToManyField(
        ContactPoint, related_name="practitioner_telecom", blank=True
    )
    gender = models.CharField(
        max_length=20, choices=base_choices.GenderChoices.choices, null=True, blank=True
    )
    birth_date = models.DateField(null=True, blank=True)
    deceased_boolean = models.BooleanField(default=True)
    deceased_date_time = models.DateTimeField(null=True, blank=True)
    address = models.ManyToManyField(
        Address, related_name="practitioner_address", blank=True
    )
    photo = models.ManyToManyField(
        Attachment, related_name="practitioner_photo", blank=True
    )
    qualification = models.ManyToManyField(
        Qualification, related_name="practitioner_qualification", blank=True
    )
    communication = models.ManyToManyField(
        Communication, related_name="practitioner_communication", blank=True
    )


# Practitioner Role
class PractitionerRole(TimeStampedModel):
    """Practitioner Role model."""

    identifier = models.ManyToManyField(
        Identifier, related_name="practitioner_role_identifier", blank=True
    )
    active = models.BooleanField(default=True)
    period = models.ForeignKey(
        Period, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    practitioner = models.ForeignKey(
        PractitionerReference,
        on_delete=models.CASCADE,
        related_name="practitioner_role_practitioner",
    )
    organization = models.ForeignKey(
        OrganizationReference,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="practitioner_role_organization",
    )
    network = models.ManyToManyField(
        OrganizationReference, related_name="practitioner_role_network", blank=True
    )
    code = models.ManyToManyField(
        CodeableConcept, related_name="practitioner_role_code", blank=True
    )
    display = models.TextField(null=True)
    specialty = models.ManyToManyField(
        CodeableConcept, related_name="practitioner_role_specialty", blank=True
    )
    location = models.ManyToManyField(
        LocationReference, related_name="practitioner_role_location", blank=True
    )
    healthcare_service = models.ManyToManyField(
        HealthCareServiceReference, related_name="practitioner_role_healthcareservice"
    )
    contact = models.ManyToManyField(
        ExtendedContactDetail, related_name="practitioner_role_contact", blank=True
    )
    characteristic = models.ManyToManyField(
        CodeableConcept, related_name="practitioner_role_characteristic", blank=True
    )
    communication = models.ManyToManyField(
        CodeableConcept, related_name="practitioner_role_communication", blank=True
    )
    availability = models.ForeignKey(
        Availability,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="practitioner_role_availability",
    )
    endpoint = models.ManyToManyField(
        EndpointReference, related_name="practitioner_role_endpoint", blank=True
    )


class PractitionerOrganizationPractitionerRoleReference(models.Model):
    """General Practitioner Reference model."""

    practitioner = models.ForeignKey(
        Practitioner,
        on_delete=models.CASCADE,
        related_name="general_practitioner",
        null=True,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="general_practitioner_organization",
        null=True,
    )
    practitioner_role = models.ForeignKey(
        PractitionerRole, on_delete=models.CASCADE, null=True
    )


class PractitionerPractitionerRoleReference(BaseReference):
    """practitioner practitioner role reference model."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.CASCADE,
        related_name="practitioner_practitioner_role_reference_identifier",
        null=True,
    )
    practitioner = models.ForeignKey(
        Practitioner,
        on_delete=models.CASCADE,
        related_name="practitioner_practitioner_role_reference_practitioner",
        null=True,
    )
    practitioner_role = models.ForeignKey(
        PractitionerRole,
        on_delete=models.CASCADE,
        related_name="practitioner_practitioner_role_reference_practitioner_role",
        null=True,
    )


class PractitionerRoleReference(BaseReference):
    """Practitioner Role Reference model."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.CASCADE,
        related_name="practitioner_role_reference_identifier",
    )
    practitioner_role = models.ForeignKey(
        PractitionerRole,
        on_delete=models.CASCADE,
        related_name="practitioner_role_reference_practitioner_role",
    )
