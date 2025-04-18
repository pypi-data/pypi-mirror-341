__version__ = '0.1.0-b1'

from ._internal.managers import project_manager, registry_manager
from ._internal.mcp import (
    MCPResolver,
    MCPStrategy,
    add_to_fastmcp,
    create_resource_info,
    create_tool_info,
    mount_to_fastmcp,
)
from ._internal.project import Project
from ._internal.registry import Registry

__all__ = (
    'MCPResolver',
    'MCPStrategy',
    'Project',
    'Registry',
    'add_to_fastmcp',
    'create_resource_info',
    'create_tool_info',
    'mount_to_fastmcp',
    'project_manager',
    'registry_manager',
)
