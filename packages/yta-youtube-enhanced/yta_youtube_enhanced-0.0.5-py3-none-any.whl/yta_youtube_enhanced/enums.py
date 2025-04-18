from yta_general_utils.programming.enum import YTAEnum as Enum


class DescriptionParameter(Enum):
    """
    Enum class to contain the description parameters
    that we can expect in our videos.
    """

    KEY_MOMENT = 'key_moment'
    """
    The time moment in which the video is more 
    interesting and/or the most important part is
    taking place.
    """