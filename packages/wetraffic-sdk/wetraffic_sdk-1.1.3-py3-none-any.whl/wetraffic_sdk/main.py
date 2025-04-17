from .api_client import ApiClient
from .lights import Lights


class WetrafficSdk:
    """
    Main SDK that composes all functionalities for the Wetraffic system.

    This class provides the main interface for interacting with the Wetraffic system.
    It manages traffic lights and other related functionalities.

    Args:
        area (str): The area code to initialize the SDK with.

    Attributes:
        lights (Lights): Interface for managing traffic lights.

    Example:
        >>> from wetraffic_sdk import WetrafficSdk
        >>> sdk = WetrafficSdk(area="AREA01")
        >>> sdk.lights.get_status()
    """

    def __init__(self, area: str):
        """
        Initialize the WetrafficSdk.

        Args:
            area (str): The area code to initialize the SDK with.
        """
        self._client = ApiClient(area=area)
        self.lights = Lights(client=self._client, area=area)

    def get_area(self) -> str:
        """
        Get the current area code.

        Returns:
            str: The current area code.
        """
        return self._client.area
