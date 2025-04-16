"""Network profile models for AgentDock.

This module defines the data models for network profiles, which describe
the characteristics and capabilities of AgentDock networks.
"""

from typing import List, Optional, Dict, Any, Literal
import uuid
from pydantic import BaseModel, Field, validator
from packaging import version

class NetworkAuthentication(BaseModel):
    """Authentication configuration for a network."""
    
    type: Literal["none", "basic", "oauth2", "api_key"] = Field(
        default="none",
        description="The type of authentication required by the network"
    )
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional configuration for the authentication method"
    )


class NetworkProfile(BaseModel):
    """Profile information for an AgentDock network.
    
    This model defines the public-facing information and capabilities
    of an AgentDock network, including its name, description, capacity,
    and authentication requirements.
    """
    
    discoverable: bool = Field(
        default=False,
        description="Whether the network should be discoverable in network directories"
    )

    network_discovery_server: Optional[str] = Field(
        default="https://discovery.agentdock.org",
        description="The URL of the network discovery server"
    )

    network_id: str = Field(
        default_factory=lambda: f"network-{uuid.uuid4().hex[:8]}",
        description="The unique identifier for the network"
    )
    
    management_code: Optional[str] = Field(
        default=None,
        description="Optional management code for re-publishing a network with the same ID"
    )
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The human-readable name of the network"
    )
    
    description: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="A description of the network's purpose and capabilities"
    )
    
    icon: Optional[str] = Field(
        None,
        description="URL to the network's icon image"
    )
    
    website: Optional[str] = Field(
        None,
        description="URL to the network's website"
    )
    
    tags: List[str] = Field(
        default_factory=list,
        description="Tags describing the network's features and focus areas"
    )
    
    categories: List[str] = Field(
        default_factory=list,
        description="Categories that the network belongs to"
    )
    
    country: str = Field(
        default="Worldwide",
        description="The country or region where the network operates"
    )
    
    required_agentdock_version: str = Field(
        ...,
        description="The minimum version of AgentDock required to connect to this network"
    )
    
    capacity: Optional[int] = Field(
        default=None,
        description="The maximum number of agents that can connect to the network simultaneously"
    )
    
    authentication: NetworkAuthentication = Field(
        default_factory=NetworkAuthentication,
        description="Authentication configuration for the network"
    )
    
    host: str = Field(
        default="localhost",
        description="The host address of the network"
    )
    
    port: int = Field(
        default=8765,
        ge=1,
        le=65535,
        description="The port number of the network"
    )
    
    @validator('required_agentdock_version')
    def validate_version(cls, v):
        """Validate that the version string is in the correct format."""
        try:
            version.parse(v)
            return v
        except version.InvalidVersion:
            raise ValueError(f"Invalid version format: {v}")
    
    