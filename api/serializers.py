import os
from rest_framework import serializers

from .maskers import mask_common, mask_email, mask_phone_number
from .models import Employee, FileUpload


class EmployeeListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        level = dict(Employee.LEVEL_CHOICES).get(obj.level)
        type = dict(Employee.TYPE_CHOICES).get(obj.type)
        return level + " " + type

    class Meta:
        model = Employee
        fields = "__all__"


# class WorkInformationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WorkInformation
#         fields = "__all__"


# class PersonalInformationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PersonalInformation
#         fields = "__all__"


class EmployeeDetailSerializer(serializers.ModelSerializer):
    # work_information = WorkInformationSerializer()
    # personal_information = PersonalInformationSerializer()
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        level = dict(Employee.LEVEL_CHOICES).get(obj.level)
        type = dict(Employee.TYPE_CHOICES).get(obj.type)
        return level + " " + type

    class Meta:
        model = Employee
        fields = "__all__"


# class MaskedWorkInformationSerializer(WorkInformationSerializer):
#     tax_code = serializers.SerializerMethodField()
#     social_insurance_code = serializers.SerializerMethodField()

#     def get_tax_code(self, obj):
#         return mask_common(obj.tax_code)

#     def get_social_insurance_code(self, obj):
#         return mask_common(obj.social_insurance_code)

#     class Meta:
#         model = WorkInformation
#         fields = "__all__"


# class MaskedPersonalInformationSerializer(PersonalInformationSerializer):
#     phone_number = serializers.SerializerMethodField()
#     citizen_identification_code = serializers.SerializerMethodField()
#     personal_email = serializers.SerializerMethodField()
#     birthplace = serializers.SerializerMethodField()
#     current_address = serializers.SerializerMethodField()
#     permanent_address = serializers.SerializerMethodField()
#     bank_account_number = serializers.SerializerMethodField()

#     def get_phone_number(self, obj):
#         return mask_phone_number(obj.phone_number)

#     def get_citizen_identification_code(self, obj):
#         return mask_common(obj.citizen_identification_code)

#     def get_personal_email(self, obj):
#         return mask_email(obj.personal_email)

#     def get_birthplace(self, obj):
#         return mask_common(obj.birthplace)

#     def get_current_address(self, obj):
#         return mask_common(obj.current_address)

#     def get_permanent_address(self, obj):
#         return mask_common(obj.permanent_address)

#     def get_bank_account_number(self, obj):
#         return mask_common(obj.bank_account_number)

#     class Meta:
#         model = PersonalInformation
#         fields = "__all__"


class MaskedEmployeeDetailSerializer(serializers.ModelSerializer):
    # work_information = MaskedWorkInformationSerializer()
    # personal_information = MaskedPersonalInformationSerializer()
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        level = dict(Employee.LEVEL_CHOICES).get(obj.level)
        type = dict(Employee.TYPE_CHOICES).get(obj.type)
        return level + " " + type

    #work
    tax_code = serializers.SerializerMethodField()
    social_insurance_code = serializers.SerializerMethodField()

    def get_tax_code(self, obj):
        return mask_common(obj.tax_code)

    def get_social_insurance_code(self, obj):
        return mask_common(obj.social_insurance_code)
    
    #personal
    phone_number = serializers.SerializerMethodField()
    citizen_identification_code = serializers.SerializerMethodField()
    personal_email = serializers.SerializerMethodField()
    birthplace = serializers.SerializerMethodField()
    current_address = serializers.SerializerMethodField()
    permanent_address = serializers.SerializerMethodField()
    bank_account_number = serializers.SerializerMethodField()
    # date_of_birth = serializers.SerializerMethodField()

    def get_phone_number(self, obj):
        return mask_phone_number(obj.phone_number)

    def get_citizen_identification_code(self, obj):
        return mask_common(obj.citizen_identification_code)

    def get_personal_email(self, obj):
        return mask_email(obj.personal_email)

    def get_birthplace(self, obj):
        return mask_common(obj.birthplace)

    def get_current_address(self, obj):
        return mask_common(obj.current_address)

    def get_permanent_address(self, obj):
        return mask_common(obj.permanent_address)

    def get_bank_account_number(self, obj):
        return mask_common(obj.bank_account_number)
    
    # def get_date_of_birth(self, obj):
    #     return mask_date_of_birth(obj.date_of_birth)

    class Meta:
        model = Employee
        fields = "__all__"


class TypeCountSerializer(serializers.Serializer):
    type_display = serializers.CharField()
    count = serializers.IntegerField()

    class Meta:
        fields = ["type_display", "count"]


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ["id", "employee", "file", "is_encrypted"]


class FileUploadListSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.file.url

    def get_name(self, obj):
        return os.path.basename(obj.file.name)

    class Meta:
        model = FileUpload
        fields = ["id", "name", "url", "is_encrypted", "created_at"]
