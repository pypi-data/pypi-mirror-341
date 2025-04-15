import logging

from bw_essentials.constants.services import Services
from bw_essentials.services.api_client import ApiClient

logger = logging.getLogger(__name__)


class ModelPortfolioReporting(ApiClient):

    def __init__(self,
                 service_user: str):
        logger.info(f"Initializing ModelPortfolioReporting client for user: {service_user}")
        super().__init__(user=service_user)
        self.object = None
        self.urls = {
            "portfolio": "portfolio"
        }
        self.name = Services.MODEL_PORTFOLIO.value
        self.base_url = self.get_base_url(Services.MODEL_PORTFOLIO.value)

    def get_active_rebalance(self, portfolio_id):
        logger.info(f"In - portfolios_by_id {portfolio_id =}")
        data = self._get(url=self.base_url,
                         endpoint=f'{self.urls.get("portfolio")}/{portfolio_id}/rebalance/active/')
        logger.info(f"{data =}")

        return data.get("data")

    def get_portfolio_performance_by_dates(self, portfolio_id, start_date, end_date):
        url = f"{self.base_url}/{self.urls['portfolio_performance'] % portfolio_id}"
        params = {"start_date": start_date, "end_date": end_date}
        performance = self._get(url=self.base_url,
                                endpoint=f"{self.urls['portfolio_performance'] % portfolio_id}",
                                params=params)
        return performance["data"]
