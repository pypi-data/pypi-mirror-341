from datetime import datetime

from .api_client import ApiClient


class Lights:
    """
    Interface for managing traffic lights.

    This class provides methods to interact with traffic lights data and status.

    Args:
        client (ApiClient): The API client instance.
        area (str): The area code for the traffic lights.

    Example:
        >>> from wetraffic_sdk import WetrafficSdk
        >>> sdk = WetrafficSdk(area="AREA01")
        >>> sdk.lights.get_data(start_date=datetime.now(), end_date=datetime.now())
    """

    def __init__(self, *, client: ApiClient, area: str):
        """
        Initialize the Lights interface.

        Args:
            client (ApiClient): The API client instance.
            area (str): The area code for the traffic lights.
        """
        self._client = client

    def get_data(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> None:
        """
        Get traffic data for a specific time period.

        Args:
            start_date (datetime): The start date for the data retrieval.
            end_date (datetime): The end date for the data retrieval.

        Returns:
            None: Currently returns None as placeholder.
        """
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        print(params)
        return None
