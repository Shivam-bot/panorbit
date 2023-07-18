# To define customize Validations functions to validate various fields


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomValidations:

    @staticmethod
    def validate_mobile_number(value: int):
        mobile_number = str(value)
        if len(mobile_number) < 10 or len(mobile_number)>10:
            raise ValidationError(
                _("%(value)s should be of length 10"),
                params={"value": value}
            )

    @staticmethod
    def validate_name(value: str):
        if value.__contains__(' '):
            raise ValidationError([
                ValidationError(_(f"{value} should not contain space"),
                params={"value": value})]
            )


