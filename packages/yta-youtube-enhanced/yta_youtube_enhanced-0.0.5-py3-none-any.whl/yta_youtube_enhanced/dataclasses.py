from yta_general_utils.programming.regular_expressions import RegularExpression
from dataclasses import dataclass


@dataclass
class DescriptionParameter:
    """
    @dataclass
    Class that represents a parameter that is written
    in the video description, that is detected because
    its format is a specific one defined by us.

    This is the format of a description parameter that
    our system will detect: @parameter:value@
    """

    name: str
    """
    The name of the parameter.
    """
    value: any
    """
    The value of the parameter.
    """

    def __init__(
        self,
        name: str,
        value: any
    ):
        self.name = name
        self.value = value

    @staticmethod
    def detect_parameters(
        description: str
    ) -> list['DescriptionParameter']:
        """
        Detect the parameters available in the youtube
        video 'description' provided as a parameter.
        """
        # TODO: I don't like having this declaration here
        class MyRegExp(RegularExpression):
            DESCRIPTION_PARAMETER = r'@([^:]+):([^@]+)@'

        return [
            DescriptionParameter(
                hit[0],
                hit[1]
            ) for hit in MyRegExp.DESCRIPTION_PARAMETER.find(description)
        ]