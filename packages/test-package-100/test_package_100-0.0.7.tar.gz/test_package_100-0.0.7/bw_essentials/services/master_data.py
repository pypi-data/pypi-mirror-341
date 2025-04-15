"""
Module to make structured API calls to the Master Data Service.

This module extends the generic ApiClient to provide typed, reusable
endpoints for accessing Master Data APIs like holidays, security details,
broker configurations, and constants.
"""

import logging
from typing import Optional, List, Dict, Any

from bw_essentials.constants.services import Services
from bw_essentials.services.api_client import ApiClient

logger = logging.getLogger(__name__)


class MasterData(ApiClient):
    """
    API wrapper for Master Data Service.

    Inherits from ApiClient and provides domain-specific methods to fetch
    holidays, constants, company details, and broker configurations.

    Args:
        service_user (str): The user initiating the request (e.g., system/username).
    """

    def __init__(self, service_user: str):
        logger.info(f"Initializing MasterData client for user: {service_user}")
        super().__init__(user=service_user)
        self.base_url = self.get_base_url(Services.MASTER_DATA.value)
        self.name = Services.MASTER_DATA.value
        self.urls = {
            "holidays": "holidays",
            "securities": "securities",
            "details": "company/details",
            "constant": "constants",
            "broker_config": "broker/config/keys",
            "broker_details": "securities/{}/details",
            "isin_details": "company/details/isin"
        }

    def get_security_details(self, securities: List[str]) -> Optional[Dict[str, Any]]:
        """
        Fetches company security details by symbols.

        Args:
            securities (List[str]): List of security symbols.
        Returns:
            Optional[Dict[str, Any]]: Security detail data or None.
        """
        logger.info(f"Fetching security details for: {securities}")
        securities = ','.join(securities)
        response = self._get(url=self.base_url,
                             endpoint=self.urls["details"],
                             params={"symbols": securities})
        return response.get("data")

    def get_constants_data(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Fetches constants from master data using a key.

        Args:
            key (str): Constant key to query.

        Returns:
            Optional[Dict[str, Any]]: Constant values or None.
        """
        logger.info(f"Fetching constants data for key: {key}")
        response = self._get(url=self.base_url,
                             endpoint=self.urls["constant"],
                             params={"key": key})
        return response.get("data")

    def get_trading_holidays(self, year: int) -> Optional[List[Dict[str, Any]]]:
        """
        Gets trading holidays for a specific year.

        Args:
            year (int): Year for which holidays are to be fetched.
        Returns:
            Optional[List[Dict[str, Any]]]: List of holiday data.
        """
        logger.info(f"Fetching trading holidays for year: {year}")
        response = self._get(url=self.base_url,
                             endpoint=self.urls["holidays"],
                             params={"year": year})
        return response.get("data")

    def get_broker_config_keys(self, broker: str,
                               product_type: Optional[str] = None,
                               category: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieves broker configuration keys based on filters.

        Args:
            broker (str): Broker name.
            product_type (Optional[str]): Type of product (e.g., equity, MTF).
            category (Optional[str]): Optional configuration category.
        Returns:
            Optional[Dict[str, Any]]: Configuration key data or None.
        """
        logger.info(f"Fetching broker config keys for broker={broker}, product_type={product_type}, category={category}")
        params = {k: v for k, v in {'broker': broker, 'product': product_type, 'category': category}.items() if v}
        response = self._get(url=self.base_url,
                             endpoint=self.urls["broker_config"],
                             params=params)
        return response.get("data")

    def get_broker_security_details(self, securities: List[str], broker: str) -> Dict[str, Any]:
        """
        Retrieves broker-specific security details.

        Args:
            securities (List[str]): List of security symbols.
            broker (str): Broker name.

        Returns:
            Dict[str, Any]: Security detail data.
        """
        logger.info(f"Fetching broker security details for securities={securities}, broker={broker}")
        endpoint = self.urls["broker_details"].format(broker)
        params = {"symbols": securities}
        response = self._get(url=self.base_url,
                             endpoint=endpoint,
                             params=params)
        return response.get("data", {})

    def get_company_details(self, isin_data: List[str]) -> Dict[str, Any]:
        """
        Fetches company details using ISIN codes.

        Args:
            isin_data (List[str]): List of ISIN codes.

        Returns:
            Dict[str, Any]: Company detail data.
        """
        logger.info(f"Fetching company details for ISINs: {isin_data}")
        response = self._get(url=self.base_url,
                             endpoint=self.urls["isin_details"],
                             params={"isin": isin_data})
        return response.get("data", {})

    def get_active_securities(self) -> List[Dict[str, Any]]:
        """
        Retrieves all available active securities.

        Returns:
            List[Dict[str, Any]]: List of securities.
        """
        logger.info("Fetching list of all securities")
        response = self._get(url=self.base_url,
                             endpoint=self.urls["securities"])
        return response.get("data", [])
