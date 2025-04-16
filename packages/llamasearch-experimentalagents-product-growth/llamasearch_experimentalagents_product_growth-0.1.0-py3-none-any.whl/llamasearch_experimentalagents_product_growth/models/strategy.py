"""
Strategy data models for LlamaSearch ExperimentalAgents: Product Growth.

This module defines the data models for growth strategies, GTM approaches,
and strategic roadmaps using Pydantic.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field, field_validator


class Priority(str, Enum):
    """Priority levels for growth strategies."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class GTMStrategy(str, Enum):
    """Go-to-Market strategies for product features."""
    
    FREEMIUM = "freemium"
    LAND_AND_EXPAND = "land-and-expand"
    PRODUCT_LED_GROWTH = "product-led-growth"
    CUSTOMER_ADVOCACY = "customer-advocacy"
    ECOSYSTEM_PARTNERSHIPS = "ecosystem-partnerships"
    CONTENT_MARKETING = "content-marketing"
    COMMUNITY_BUILDING = "community-building"
    VIRAL_LOOPS = "viral-loops"
    VALUE_BASED_PRICING = "value-based-pricing"
    ACCOUNT_BASED_MARKETING = "account-based-marketing"


class GrowthRecommendation(BaseModel):
    """Model for a growth strategy recommendation."""
    
    feature: str = Field(..., description="Feature or improvement name")
    priority: Priority = Field(..., description="Priority level")
    sentiment_score: float = Field(
        ..., description="Sentiment score between -1 and 1", ge=-1, le=1
    )
    gtm_strategies: List[str] = Field(
        ..., description="Go-to-market strategies to apply"
    )
    expected_impact: float = Field(
        ..., description="Expected impact score between 0 and 1", ge=0, le=1
    )
    details: Optional[str] = Field(
        None, description="Detailed description and justification"
    )
    cluster_id: Optional[int] = Field(
        None, description="ID of the feedback cluster that generated this recommendation"
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="When the recommendation was created"
    )
    
    @field_validator("gtm_strategies")
    def validate_gtm_strategies(cls, v: List[str]) -> List[str]:
        """Validate GTM strategies."""
        # If the strategy is a valid enum value, normalize to the enum value
        valid_strategies = []
        for strategy in v:
            try:
                # Try to convert to enum value
                enum_value = GTMStrategy(strategy.lower())
                valid_strategies.append(enum_value.value)
            except ValueError:
                # If not a valid enum, keep as is (for flexibility)
                valid_strategies.append(strategy)
        
        return valid_strategies
    
    @property
    def impact_label(self) -> str:
        """Return a human-readable impact label."""
        if self.expected_impact > 0.7:
            return "high"
        elif self.expected_impact > 0.4:
            return "medium"
        else:
            return "low"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary suitable for JSON serialization."""
        return {
            "feature": self.feature,
            "priority": self.priority,
            "sentiment_score": self.sentiment_score,
            "gtm_strategies": self.gtm_strategies,
            "expected_impact": self.expected_impact,
            "impact_label": self.impact_label,
            "details": self.details,
            "cluster_id": self.cluster_id
        }


class StrategicRoadmap(BaseModel):
    """Model for a complete strategic roadmap."""
    
    recommendations: List[GrowthRecommendation] = Field(
        ..., description="List of growth recommendations"
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Timestamp when the roadmap was created"
    )
    version: str = Field("1.0", description="Roadmap version")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about the roadmap"
    )
    
    @property
    def high_priority_items(self) -> List[GrowthRecommendation]:
        """Return items with high priority."""
        return [r for r in self.recommendations if r.priority == Priority.HIGH]
    
    @property
    def medium_priority_items(self) -> List[GrowthRecommendation]:
        """Return items with medium priority."""
        return [r for r in self.recommendations if r.priority == Priority.MEDIUM]
    
    @property
    def low_priority_items(self) -> List[GrowthRecommendation]:
        """Return items with low priority."""
        return [r for r in self.recommendations if r.priority == Priority.LOW]
    
    @property
    def total_expected_impact(self) -> float:
        """Calculate the total expected impact of all recommendations."""
        # Simple sum (not perfect, but gives a relative measure)
        return sum(r.expected_impact for r in self.recommendations)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary suitable for JSON serialization."""
        return {
            "recommendations": [r.to_dict() for r in self.recommendations],
            "created_at": self.created_at.isoformat(),
            "version": self.version,
            "metadata": self.metadata,
            "high_priority_count": len(self.high_priority_items),
            "medium_priority_count": len(self.medium_priority_items),
            "low_priority_count": len(self.low_priority_items),
            "total_expected_impact": self.total_expected_impact
        } 