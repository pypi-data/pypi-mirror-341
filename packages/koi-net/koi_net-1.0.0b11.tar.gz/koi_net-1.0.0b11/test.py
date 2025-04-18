from koi_net import NodeInterface
from koi_net.protocol.node import NodeProfile, NodeProvides, NodeType
from koi_net.processor.default_handlers import (
    basic_rid_handler,
    basic_manifest_handler,
    edge_negotiation_handler,
    basic_network_output_filter
)

node = NodeInterface(
    name="mypartialnode",
    profile=NodeProfile(
        node_type=NodeType.PARTIAL,
        provides=NodeProvides(
            event=[]
        )
    ),
    handlers=[
        basic_rid_handler,
        basic_manifest_handler,
        edge_negotiation_handler,
        basic_network_output_filter
        # include all or none of the default handlers imported above
    ]
)