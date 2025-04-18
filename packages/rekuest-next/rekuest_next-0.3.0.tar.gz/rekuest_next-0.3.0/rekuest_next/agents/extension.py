from typing import List, runtime_checkable, Protocol, Optional
from rekuest_next.api.schema import Template
from rekuest_next.actors.base import Actor, Passport, ActorTransport
from typing import TYPE_CHECKING
from rekuest_next.definition.registry import DefinitionRegistry
from rekuest_next.collection.collector import Collector
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from rekuest_next.agents.base import BaseAgent
    from rekuest_next.api.schema import TemplateInput


@runtime_checkable
class AgentExtension(Protocol):
    cleanup: bool = False

    async def astart(self):
        """This should be called when the agent starts"""
        ...


    def get_name(self) -> str:
        """This should return the name of the extension"""
        ...
    
    def get_definition_registry(self) -> DefinitionRegistry:
        """This should register the definitions for the agent.

        This is called when the agent is started, for each extensions. Extensions
        should register their definitions here and merge them with the agent's
        definition registry.
        
        Dynamic 
        """
        ...

    async def aspawn_actor_from_template(
        self,
        agent: "BaseAgent",
        interface: str,
    ) -> Optional[Actor]:
        """This should create an actor from a template and return it.

        The actor should not be started!

        TODO: This should be asserted

        """
        ...

    async def aget_templates(
        self, 
    ) -> List["TemplateInput"]:
        """This should register the definitions for the agent.

        This is called when the agent is started, for each extensions. Extensions
        should register their definitions here and merge them with the agent's
        definition registry.


        Basic usage:

        ```python

        definition, actorBuilder = reactify(...)

        definition_registry.register_at_interface(
            "deploy_graph",
            definition=definition,
            structure_registry=self.structure_registry,
            actorBuilder=actorBuilder,
        )

        ```

        Merge Usage:

        ```python

        self.definition_registry = DefinitionRegistry()

        agent_definition_registry.merge_with(self.definition_registry)



        """
        ...

    async def atear_down(self):
        """This should be called when the agent is torn down"""
        ...


class BaseAgentExtension(ABC):
    cleanup: bool = False

    @abstractmethod
    async def astart(self):
        """This should be called when the agent starts"""
        ...

    @abstractmethod
    def get_name(self) -> str:
        """This should return the name of the extension"""
        raise NotImplementedError("Implement this method")

    @abstractmethod
    async def aspawn_actor_for_interface(
        self,
        agent: "BaseAgent",
        interface: str,
    ) -> Optional[Actor]:
        """This should create an actor from a template and return it.

        The actor should not be started!
        """
        ...

    @abstractmethod
    async def aget_templates(self) -> List["TemplateInput"]:
        """This should register the definitions for the agent.

        This is called when the agent is started, for each extensions. Extensions
        should register their definitions here and merge them with the agent's
        definition registry.
        """
        ...

    @abstractmethod
    async def atear_down(self):
        """
        This should be called when the agent is torn down
        """
