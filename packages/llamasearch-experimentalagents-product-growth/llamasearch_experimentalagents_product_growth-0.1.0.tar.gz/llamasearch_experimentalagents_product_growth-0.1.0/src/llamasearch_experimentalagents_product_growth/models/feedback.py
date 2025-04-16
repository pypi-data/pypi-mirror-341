"""
Feedback data models for LlamaSearch ExperimentalAgents: Product Growth.

This module defines the data models for customer feedback, analysis results,
and cluster information using Pydantic.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union, Any

from pydantic import BaseModel, Field, validator


class FeedbackSource(str, Enum):
    """Source of customer feedback."""
    
    APP = "app"
    EMAIL = "email"
    SURVEY = "survey"
    INTERVIEW = "interview"
    SOCIAL = "social"
    SUPPORT = "support"
    OTHER = "other"


class UserType(str, Enum):
    """Types of users providing feedback."""
    
    NEW = "new"
    FREE = "free"
    PAID = "paid"
    CHURNED = "churned"
    UNKNOWN = "unknown"


class CustomerFeedback(BaseModel):
    """Model for customer feedback item."""
    
    feedback_id: Optional[str] = Field(None, description="Unique ID for the feedback")
    text: str = Field(..., description="The feedback text content")
    source: FeedbackSource = Field(FeedbackSource.OTHER, description="Source of the feedback")
    user_type: UserType = Field(UserType.UNKNOWN, description="Type of user providing feedback")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the feedback was received")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('feedback_id', pre=True, always=True)
    def set_id_if_none(cls, v):
        """Set a unique ID if none is provided."""
        from uuid import uuid4
        return v or str(uuid4())


class Cluster(BaseModel):
    """Model for a feedback cluster."""
    
    cluster_id: int = Field(..., description="Cluster identifier")
    size: int = Field(..., description="Number of feedback items in the cluster")
    sentiment_score: float = Field(..., description="Average sentiment score for the cluster", ge=-1.0, le=1.0)
    themes: List[str] = Field(..., description="Key themes identified in the cluster")
    representative_samples: List[str] = Field(
        ..., description="Representative feedback samples from this cluster"
    )
    
    @property
    def sentiment_label(self) -> str:
        """Return a human-readable sentiment label."""
        if self.sentiment_score > 0.3:
            return "positive"
        elif self.sentiment_score < -0.3:
            return "negative"
        else:
            return "neutral"


class AnalysisResults(BaseModel):
    """Model for the complete feedback analysis results."""
    
    num_feedback_items: int = Field(..., description="Total number of feedback items analyzed")
    num_clusters: int = Field(..., description="Number of clusters identified")
    cluster_sizes: Dict[str, int] = Field(..., description="Sizes of each cluster")
    cluster_themes: Dict[str, List[str]] = Field(..., description="Themes identified in each cluster")
    cluster_sentiments: Dict[str, float] = Field(..., description="Sentiment scores for each cluster")
    sample_feedback: Dict[str, List[str]] = Field(..., description="Sample feedback from each cluster")
    backend_used: str = Field(..., description="NLP backend used for analysis")
    execution_time_ms: Optional[float] = Field(None, description="Execution time in milliseconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the analysis was performed")
    
    def to_clusters(self) -> List[Cluster]:
        """Convert the analysis results to a list of Cluster objects."""
        clusters = []
        
        for cluster_id in range(self.num_clusters):
            cluster_str = str(cluster_id)
            
            # Skip if no data for this cluster
            if cluster_str not in self.cluster_sizes:
                continue
                
            clusters.append(
                Cluster(
                    cluster_id=cluster_id,
                    size=self.cluster_sizes.get(cluster_str, 0),
                    sentiment_score=self.cluster_sentiments.get(cluster_str, 0.0),
                    themes=self.cluster_themes.get(cluster_str, []),
                    representative_samples=self.sample_feedback.get(cluster_str, [])
                )
            )
            
        return clusters
    
    @property
    def most_positive_cluster(self) -> Optional[Cluster]:
        """Return the cluster with the most positive sentiment."""
        clusters = self.to_clusters()
        if not clusters:
            return None
        return max(clusters, key=lambda c: c.sentiment_score)
    
    @property
    def most_negative_cluster(self) -> Optional[Cluster]:
        """Return the cluster with the most negative sentiment."""
        clusters = self.to_clusters()
        if not clusters:
            return None
        return min(clusters, key=lambda c: c.sentiment_score)
    
    @property
    def largest_cluster(self) -> Optional[Cluster]:
        """Return the largest cluster."""
        clusters = self.to_clusters()
        if not clusters:
            return None
        return max(clusters, key=lambda c: c.size) 