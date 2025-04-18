from reaktion_next.actor import FlowActor
from rekuest_next.agents.base import BaseAgent
from rekuest_next.actors.reactive.api import useInstanceID
import logging
from rekuest_next.register import register_func
from rekuest_next.actors.base import Actor
from rekuest_next.actors.types import Passport
from fluss_next.api.schema import RekuestNodeBase, aget_flow
from rekuest_next.api.schema import NodeKind

from typing import Optional
from rekuest_next.api.schema import (
    PortInput,
    DependencyInput,
    DefinitionInput,
    Template,
    NodeKind,
    acreate_template,
    afind,
    TemplateInput,
)
from fakts_next.fakts import Fakts
from fluss_next.api.schema import (
    Flow,
)
from reaktion_next.utils import infer_kind_from_graph
from rekuest_next.widgets import StringWidget
from rekuest_next.structures.default import get_default_structure_registry
from rekuest_next.structures.registry import StructureRegistry
from pydantic import BaseModel, Field
from .utils import convert_flow_to_definition
from rekuest_next.agents.extension import AgentExtension

logger = logging.getLogger(__name__)
from rekuest_next.definition.registry import DefinitionRegistry
from rekuest_next.actors.actify import reactify
from rekuest_next.actors.base import ActorTransport
from rekuest_next.collection.collector import Collector


class ReaktionExtension(BaseModel):
    extension_name: str = "reaktion"
    cleanup: bool = False

    async def astart(self, instance_id):
        pass
    
    def get_name(self):
        return self.extension_name

    def should_cleanup_on_init(self):
        return False

    async def aspawn_actor_for_interface(
        self,
        agent: "BaseAgent",
        interface: str,
    ) -> Optional[Actor]:
        
        t = await aget_flow(id=interface)

        return FlowActor(
            flow=t,
            agent=agent,
        )

    async def aget_templates(
        self,
    ) -> list[TemplateInput]:
        templates = []
        return templates

    async def atear_down(self):
        pass
