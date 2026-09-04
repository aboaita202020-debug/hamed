"""Safe business-service engines used by Hamed AI."""
from .platform import (
    CRM, EducationCouncil, OpportunityEngine, PackageEngine, OfferEngine,
    NegotiationEngine, RestaurantGrowthEngine, ReputationEngine, SalesMessageEngine,
    ServiceCatalog, WebsiteAnalyzer, StoreAnalyzer, QRMenu, KnowledgeBase,
)
from .social_growth import SocialGrowthEngine, SocialGrowthPlan
from .supplier_database import SupplierDatabase, SupplierRecord
from .digital_delivery import DigitalDeliveryEngine

__all__ = [
    "CRM", "EducationCouncil", "OpportunityEngine", "PackageEngine", "OfferEngine",
    "NegotiationEngine", "RestaurantGrowthEngine", "ReputationEngine",
    "SalesMessageEngine", "ServiceCatalog", "WebsiteAnalyzer", "StoreAnalyzer",
    "QRMenu", "KnowledgeBase", "SocialGrowthEngine", "SocialGrowthPlan",
    "SupplierDatabase", "SupplierRecord", "DigitalDeliveryEngine",
]
