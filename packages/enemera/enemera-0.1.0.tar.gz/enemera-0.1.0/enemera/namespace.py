"""
Namespace structure for organizing API endpoints.
"""

from typing import Any




class ItalyNamespace:
    """
    Namespace for Italian energy market endpoints.
    """

    def __init__(self, client: Any):
        """
        Initialize the Italy namespace.

        Args:
            client: Enemera API client instance
        """
        # Import here to avoid circular imports
        from .api.prices import ItalyPricesAPI
        from .api.exchange_volumes import ItalyExchangeVolumesAPI
        from .api.commercial_flows import ItalyCommercialFlowsAPI
        from .api.ancillary_services import ItalyAncillaryServicesAPI
        from enemera.api.ipex_demand_act import ItalyIpexDemandActAPI
        from enemera.api.ipex_demand_fcs import ItalyIpexDemandFcsAPI

        self.prices = ItalyPricesAPI(client)
        self.exchange_volumes = ItalyExchangeVolumesAPI(client)
        self.commercial_flows = ItalyCommercialFlowsAPI(client)
        self.ancillary_services = ItalyAncillaryServicesAPI(client)
        self.ipex_demand_fcs = ItalyIpexDemandFcsAPI(client)
        self.ipex_demand_act = ItalyIpexDemandActAPI(client)