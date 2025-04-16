"""
Strategist agent for LlamaSearch ExperimentalAgents: Product Growth.

This module provides functionality for generating growth strategies based on
feedback analysis results using LLMs.
"""

import json
import logging
from typing import Dict, List, Optional, Any

from pydantic import ValidationError

from ..models.strategy import GrowthRecommendation, Priority, GTMStrategy
from ..core.llm import generate_strategies as llm_generate_strategies

logger = logging.getLogger(__name__)


def generate_growth_strategies(
    analysis_results: Dict[str, Any],
    max_strategies: int = 5,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None
) -> List[GrowthRecommendation]:
    """
    Generate growth strategies based on feedback analysis.
    
    Args:
        analysis_results: Results from feedback analysis
        max_strategies: Maximum number of strategies to generate
        provider: Optional LLM provider to use (openai, anthropic, local)
        model: Optional specific model to use
        api_key: Optional API key for the provider
        
    Returns:
        List of GrowthRecommendation objects
    """
    # Log the generation request
    logger.info(f"Generating up to {max_strategies} growth strategies")
    
    # Extract relevant information from analysis results
    clusters = analysis_results.get("num_clusters", 0)
    sentiments = analysis_results.get("cluster_sentiments", {})
    themes = analysis_results.get("cluster_themes", {})
    
    # Create a simplified analysis representation for the LLM
    simplified_analysis = {
        "clusters": clusters,
        "sentiments": sentiments,
        "themes": themes,
        "most_negative_clusters": _get_most_negative_clusters(sentiments, n=2),
        "most_positive_clusters": _get_most_positive_clusters(sentiments, n=2)
    }
    
    # Generate strategies with LLM
    try:
        if provider:
            # Use LLM-based generation with specified provider
            logger.info(f"Using LLM provider '{provider}' for strategy generation")
            
            # Generate strategies using our LLM module
            strategies_data = llm_generate_strategies(
                feedback_analysis=simplified_analysis,
                max_strategies=max_strategies,
                model=model,
                provider=provider
            )
            
            # Convert to GrowthRecommendation objects
            recommendations = _convert_to_recommendations(strategies_data)
            
            # Ensure we don't exceed max_strategies
            return recommendations[:max_strategies]
        else:
            # Use rule-based fallback
            logger.info("Using rule-based strategy generation")
            return _generate_rule_based(simplified_analysis, max_strategies)
    
    except Exception as e:
        logger.error(f"Error generating strategies: {str(e)}")
        logger.info("Falling back to rule-based generation")
        return _generate_rule_based(simplified_analysis, max_strategies)


def _convert_to_recommendations(strategies_data: List[Dict[str, Any]]) -> List[GrowthRecommendation]:
    """Convert raw strategy data to GrowthRecommendation objects."""
    recommendations = []
    
    for i, strategy in enumerate(strategies_data):
        try:
            # Map fields to GrowthRecommendation structure
            # Handle potential field name differences
            feature = strategy.get("feature") or strategy.get("name") or f"Strategy {i+1}"
            priority_str = strategy.get("priority", "medium").lower()
            
            # Map priority string to enum
            if priority_str == "high":
                priority = Priority.HIGH
            elif priority_str == "low":
                priority = Priority.LOW
            else:
                priority = Priority.MEDIUM
            
            # Get sentiment and impact scores
            sentiment_score = float(strategy.get("sentiment_score", 0))
            if sentiment_score > 1 or sentiment_score < -1:
                sentiment_score = max(-1, min(1, sentiment_score / 10))  # Scale if out of range
                
            impact_score = float(strategy.get("expected_impact", 0.5))
            if impact_score > 1 or impact_score < 0:
                impact_score = max(0, min(1, impact_score / 10))  # Scale if out of range
            
            # Get GTM strategies
            gtm_strategies = strategy.get("gtm_strategies", [])
            if not gtm_strategies and "gtm_strategy" in strategy:
                gtm_strategies = [strategy["gtm_strategy"]]
            
            if isinstance(gtm_strategies, str):
                gtm_strategies = [gtm_strategies]
                
            # Create the recommendation
            rec = GrowthRecommendation(
                feature=feature,
                priority=priority,
                sentiment_score=sentiment_score,
                expected_impact=impact_score,
                gtm_strategies=gtm_strategies,
                details=strategy.get("details") or strategy.get("description", "")
            )
            
            recommendations.append(rec)
        
        except ValidationError as e:
            logger.warning(f"Invalid strategy data: {str(e)}")
            continue
    
    return recommendations


def _get_most_negative_clusters(sentiments: Dict[str, float], n: int = 2) -> List[str]:
    """Get the IDs of the most negative sentiment clusters."""
    sorted_clusters = sorted(sentiments.items(), key=lambda x: x[1])
    return [cluster_id for cluster_id, _ in sorted_clusters[:n]]


def _get_most_positive_clusters(sentiments: Dict[str, float], n: int = 2) -> List[str]:
    """Get the IDs of the most positive sentiment clusters."""
    sorted_clusters = sorted(sentiments.items(), key=lambda x: x[1], reverse=True)
    return [cluster_id for cluster_id, _ in sorted_clusters[:n]]


def _generate_rule_based(analysis: Dict[str, Any], max_strategies: int) -> List[GrowthRecommendation]:
    """Generate strategies using rule-based approach (fallback)."""
    recommendations = []
    
    # Address negative sentiment clusters
    for cluster_id in analysis.get("most_negative_clusters", []):
        cluster_themes = analysis.get("themes", {}).get(cluster_id, [])
        if not cluster_themes:
            continue
        
        # Create a recommendation based on top theme
        theme = cluster_themes[0]
        recommendations.append(
            GrowthRecommendation(
                feature=f"Improve {theme}",
                priority=Priority.HIGH,
                sentiment_score=analysis.get("sentiments", {}).get(cluster_id, -0.5),
                expected_impact=0.8,
                gtm_strategies=[GTMStrategy.CUSTOMER_ADVOCACY, GTMStrategy.PRODUCT_LED_GROWTH],
                details=f"Address user concerns about {theme} based on negative feedback."
            )
        )
    
    # Leverage positive sentiment clusters
    for cluster_id in analysis.get("most_positive_clusters", []):
        cluster_themes = analysis.get("themes", {}).get(cluster_id, [])
        if not cluster_themes:
            continue
        
        # Create a recommendation based on top theme
        theme = cluster_themes[0]
        recommendations.append(
            GrowthRecommendation(
                feature=f"Expand {theme}",
                priority=Priority.MEDIUM,
                sentiment_score=analysis.get("sentiments", {}).get(cluster_id, 0.5),
                expected_impact=0.6,
                gtm_strategies=[GTMStrategy.CONTENT_MARKETING, GTMStrategy.VIRAL_LOOPS],
                details=f"Capitalize on positive sentiment around {theme} to drive growth."
            )
        )
    
    # Add a generic recommendation if we don't have enough
    if len(recommendations) < max_strategies:
        recommendations.append(
            GrowthRecommendation(
                feature="Customer Success Program",
                priority=Priority.MEDIUM,
                sentiment_score=0.0,
                expected_impact=0.7,
                gtm_strategies=[GTMStrategy.CUSTOMER_ADVOCACY, GTMStrategy.COMMUNITY_BUILDING],
                details="Establish a customer success program to improve overall sentiment and retention."
            )
        )
    
    # Ensure we don't exceed max_strategies
    return recommendations[:max_strategies] 