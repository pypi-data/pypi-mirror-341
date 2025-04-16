"""diagnostic report models."""

from django.db import models

from dfhir.base.models import (
    Annotation,
    Attachment,
    BaseReference,
    CodeableConcept,
    CodeableReference,
    Identifier,
    Period,
    TimeStampedModel,
)
from dfhir.encounters.models import EncounterReference
from dfhir.medicationrequests.models import MedicationRequest
from dfhir.observations.models import Observation
from dfhir.patients.models import Patient
from dfhir.practitioners.models import Practitioner
from dfhir.servicerequests.models import ServiceRequest

from .choices import DiagnosticReportStatus


class DiagnosticReportCode(TimeStampedModel):
    """diagnostic report code model."""

    display = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True)


class DiagnosticCategory(TimeStampedModel):
    """diagnostic report category model."""

    display = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class ConclusionCode(TimeStampedModel):
    """diagnostic report conclusion code model."""

    display = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True)


class ObservationReference(BaseReference):
    """Observation Reference model."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="observation_reference_identifier",
    )

    observation = models.ForeignKey(
        "observations.Observation",
        on_delete=models.DO_NOTHING,
        related_name="observation_reference",
        null=True,
    )


class DiagnosticReportBasedOnReference(BaseReference):
    """diagnostic report based on model."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="diagnostic_report_based_on_identifier",
    )

    # TODO: careplan = models.ForeignKey(
    #     "careplans.CarePlan",
    #     on_delete=models.DO_NOTHING,
    #     null=True,
    #     related_name="diagnostic_report_based_on_careplan",
    # )
    # TODO: ImmunizationRecommendation = models.ForeignKey(
    #     "ImmunizationRecommendation", on_delete=models.DO_NOTHING, null=True
    # )
    medication_request = models.ForeignKey(
        MedicationRequest,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="diagnostic_report_based_on_medication_request",
    )
    # TODO: nutrition_order = models.ForeignKey("NutritionOrder", on_delete=models.DO_NOTHING)
    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="diagnostic_report_based_on_service_request",
    )


class DiagnosticReportSubjectReference(BaseReference):
    """diagnostic report subject model."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="diagnostic_report_subject_identifier",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="diagnostic_report_subject_patient",
    )
    location = models.ForeignKey(
        "locations.Location", on_delete=models.DO_NOTHING, null=True
    )
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.DO_NOTHING, null=True
    )
    healthcare_service = models.ForeignKey(
        "healthcareservices.HealthcareService", on_delete=models.DO_NOTHING, null=True
    )
    practitioner = models.ForeignKey(
        "practitioners.Practitioner", on_delete=models.DO_NOTHING, null=True
    )
    medication = models.ForeignKey(
        "medications.Medication",
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="diagnostic_report_subject_medication",
    )
    # TODO: group = models.ForeignKey("Group", on_delete=models.DO_NOTHING, null=True)
    device = models.ForeignKey("devices.Device", on_delete=models.DO_NOTHING, null=True)
    # TODO: substance = models.ForeignKey("Substance", on_delete=models.DO_NOTHING, null=True)
    # TODO: biologically_derived_product = models.ForeignKey("BiologicallyDerivedProduct", on_delete=models.DO_NOTHING, null=True)


class DiagnosticReportEffective(TimeStampedModel):
    """diagnostic report effective model."""

    effective_date_time = models.DateTimeField(null=True)
    period = models.ForeignKey(Period, null=True, on_delete=models.DO_NOTHING)


class DiagnosticReportPerformerReference(BaseReference):
    """performer reference."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="performer_identifier",
    )
    practitioner = models.ForeignKey(
        Practitioner,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="performer_practitioner",
    )
    practitioner_role = models.ForeignKey(
        "practitioners.PractitionerRole",
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="performer_practitioner_role",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="performer_organization",
    )
    # TODO: care_plan = models.ForeignKey(
    #     "careplans.CarePlan",
    #     on_delete=models.DO_NOTHING,
    #     null=True,
    #     related_name="performer_care_plan",
    # )


class SupportingInfoReference(BaseReference):
    """supporting info reference model."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="supporting_info_reference_identifier",
    )
    # TODO: imaging_study = models.ForeignKey(
    #     "ImagingStudy", on_delete=models.DO_NOTHING, null=True
    # )
    # TODO: procedure = models.ForeignKey("Procedure", on_delete=models.DO_NOTHING, null=True)
    observation = models.ForeignKey(
        Observation,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="supporting_info_observation",
    )
    diagnostic_report = models.ForeignKey(
        "DiagnosticReport",
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="supporting_info_diagnostic_report",
    )
    # TODO: citation = models.ForeignKey("Citation", on_delete=models.DO_NOTHING, null=True)
    # TODO: family_member_history = models.ForeignKey(
    #     "FamilyMemberHistory", on_delete=models.DO_NOTHING, null=True
    # )
    # TODO: allergy_intolerance = models.ForeignKey("AllergyIntolerance", on_delete=models.DO_NOTHING, null=True)
    # TODO: device_usage = models.ForeignKey("DeviceUsage", on_delete=models.DO_NOTHING, null=True)


class SupportingInfo(TimeStampedModel):
    """diagnostic report supporting info model."""

    type = models.ForeignKey(
        CodeableConcept,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="supporting_info_type",
    )
    reference = models.ForeignKey(
        SupportingInfoReference,
        null=True,
        on_delete=models.SET_NULL,
        related_name="supporting_info_reference",
    )


class ConclusionCodeReference(BaseReference):
    """conclusion code reference model."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="conclusion_code_reference_identifier",
    )
    observation = models.ForeignKey(
        "observations.Observation",
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="conclusion_code_observation",
    )
    condition = models.ForeignKey(
        "conditions.Condition",
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="conclusion_code_condition",
    )


class ConclusionCodeCodeableReference(TimeStampedModel):
    """conclusion code codeable reference model."""

    concept = models.ForeignKey(
        CodeableConcept,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="conclusion_code_codeable_reference_concept",
    )
    reference = models.ForeignKey(
        ConclusionCodeReference,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="conclusion_code_codeable_reference_codeable",
    )


class DiagnosticReportMedia(TimeStampedModel):
    """media model."""

    comment = models.TextField(blank=True)
    # TODO: link = models.ForeignKey(
    #     "DocumentReference",
    #     on_delete=models.DO_NOTHING,
    #     null=True,
    #     related_name="media_link",
    # )


class DiagnosticReport(TimeStampedModel):
    """diagnostic report model."""

    identifier = models.ManyToManyField(
        Identifier,
        blank=True,
        related_name="diagnostic_report_identifier",
    )
    based_on = models.ManyToManyField(
        DiagnosticReportBasedOnReference,
        blank=True,
        related_name="diagnostic_report_based_on",
    )
    status = models.CharField(
        max_length=255, choices=DiagnosticReportStatus.choices, null=True
    )
    category = models.ManyToManyField(
        CodeableConcept, blank=True, related_name="diagnostics_report_category"
    )
    code = models.ForeignKey(
        CodeableConcept,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="diagnostics_report_code",
    )
    subject = models.ForeignKey(
        DiagnosticReportSubjectReference, on_delete=models.DO_NOTHING, null=True
    )
    encounter = models.ForeignKey(
        EncounterReference,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="diagnostic_encounter",
    )
    effective_date_time = models.DateTimeField(null=True)
    effective_period = models.ForeignKey(
        Period,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="diagnostic_report_effective_period",
    )
    issued = models.DateTimeField(null=True)
    performer = models.ManyToManyField(
        DiagnosticReportPerformerReference,
        blank=True,
        related_name="diagnostic_report_performer",
    )
    results_interpretation = models.ManyToManyField(
        DiagnosticReportPerformerReference,
        blank=True,
        related_name="diagnostic_results_interpretation",
    )

    # TODO: specimen models.ManyToMany(|"specimens.Specimen", on_delete=models.DO_NOTHING, null=True)
    result = models.ManyToManyField(
        ObservationReference, blank=True, related_name="diagnostic_result"
    )
    note = models.ManyToManyField(
        Annotation, blank=True, related_name="diagnostic_report_note"
    )
    # TODO: study = models.ManyToManyField(GenomicImagingReference, blank=True)
    supporting_info = models.ManyToManyField(
        SupportingInfo, blank=True, related_name="diagnostic_report_supporting_info"
    )
    media = models.ManyToManyField(DiagnosticReportMedia, blank=True)
    # TODO: composition = models.ForeignKey(
    #     "Composition",
    #     on_delete=models.DO_NOTHING,
    #     null=True,
    #     related_name="diagnostic_report_composition",
    # )
    conclusion = models.TextField(null=True)
    conclusion_code = models.ManyToManyField(
        ConclusionCodeCodeableReference,
        blank=True,
        related_name="diagnostic_report_conclusion_code",
    )
    recommendation = models.ManyToManyField(CodeableReference, blank=True)
    presented_form = models.ManyToManyField(Attachment, blank=True)
    communication = models.ManyToManyField(
        "communications.CommunicationReference",
        blank=True,
        related_name="diagnostic_report_communication",
    )


class DiagnosticReportDocumentReferenceReference(BaseReference):
    """document reference reference model."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="document_reference_reference_identifier",
    )
    # TODO: fix!
    # document_reference = models.ForeignKey(
    #     "documentreferences.DocumentReference",
    #     on_delete=models.DO_NOTHING,
    #     null=True,
    #     related_name="document_reference_reference_document_reference",
    # )
    diagnostic_report = models.ForeignKey(
        DiagnosticReport,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="document_reference_reference_diagnostic_report",
    )
