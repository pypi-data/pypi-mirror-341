from typing import Dict, Any
from kirara_ai.plugin_manager.plugin import Plugin
from kirara_ai.logger import get_logger
from kirara_ai.workflow.core.block import BlockRegistry
from kirara_ai.ioc.inject import Inject
from kirara_ai.ioc.container import DependencyContainer
from kirara_ai.workflow.core.workflow.builder import WorkflowBuilder
from kirara_ai.workflow.core.workflow.registry import WorkflowRegistry
from .blocks import QQEmailBlock, QQEmailFetchBlock
import json
import os
from pathlib import Path

logger = get_logger("QQEmail")

class EmailPlugin(Plugin):
    def __init__(self, block_registry: BlockRegistry, container: DependencyContainer):
        super().__init__()
        self.block_registry = block_registry
        self.workflow_registry = container.resolve(WorkflowRegistry)
        self.container = container
        self.config_path = Path(__file__).parent / 'config.json'

    def on_load(self):
        logger.info("QQEmailPlugin loading")

        # Register Block
        try:
            self.block_registry.register("send_qq_email", "email", QQEmailBlock)
            self.block_registry.register("find_qq_emails", "email", QQEmailFetchBlock)
        except Exception as e:
            logger.warning(f"QQEmailPlugin registration failed: {e}")

        try:
            current_file = os.path.abspath(__file__)
            parent_dir = os.path.dirname(current_file)
            example_dir = os.path.join(parent_dir, 'example')
            yaml_files = [f for f in os.listdir(example_dir) if f.endswith('.yaml') or f.endswith('.yml')]

            for yaml in yaml_files:
                logger.info(os.path.join(example_dir, yaml))
                self.workflow_registry.register_preset_workflow("email", yaml.stem, WorkflowBuilder.load_from_yaml(os.path.join(example_dir, yaml), self.container))
        except Exception as e:
            logger.warning(f"workflow_registry failed: {e}")
        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def on_start(self):
        logger.info("QQEmailPlugin started")

    def on_stop(self):
        logger.info("QQEmailPlugin stopped")

    def save_token(self, token_info: Dict[str, Any]):
        """Save OAuth token to local storage"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(token_info, f)
            return True
        except Exception as e:
            logger.error(f"Failed to save token: {e}")
            return False

    def load_token(self) -> Dict[str, Any]:
        """Load OAuth token from local storage"""
        try:
            if not self.config_path.exists():
                return {}
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load token: {e}")
            return {}
