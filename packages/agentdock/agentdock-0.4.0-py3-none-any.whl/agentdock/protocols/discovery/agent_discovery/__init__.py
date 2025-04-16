"""
Agent Discovery Protocol for AgentDock.

This protocol allows agents to announce their capabilities to the network
and for other agents to discover agents with specific capabilities.
Key features:
- Capability announcement
- Capability discovery
- Capability matching
"""

from src.agentdock.protocols.discovery.agent_discovery.adapter import AgentDiscoveryAdapter
from src.agentdock.protocols.discovery.agent_discovery.protocol import AgentDiscoveryProtocol

__all__ = ["AgentDiscoveryAdapter", "AgentDiscoveryProtocol"]
