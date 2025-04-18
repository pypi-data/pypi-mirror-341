from pathlib import Path
from typing import Any
from typing import cast

from dipdup.codegen import CodeGenerator
from dipdup.config import HandlerConfig
from dipdup.config.starknet import StarknetContractConfig
from dipdup.config.starknet_events import StarknetEventsHandlerConfig
from dipdup.config.starknet_events import StarknetEventsIndexConfig
from dipdup.config.starknet_node import StarknetNodeDatasourceConfig
from dipdup.datasources import AbiDatasource
from dipdup.exceptions import ConfigurationError
from dipdup.utils import json_dumps
from dipdup.utils import snake_to_pascal
from dipdup.utils import touch


class StarknetCodeGenerator(CodeGenerator):
    kind = 'starknet'

    async def generate_abis(self) -> None:
        for index_config in self._config.indexes.values():
            if isinstance(index_config, StarknetEventsIndexConfig):
                await self._fetch_abi(index_config)

    async def _fetch_abi(self, index_config: StarknetEventsIndexConfig) -> None:
        contracts: list[StarknetContractConfig] = [
            handler_config.contract
            for handler_config in index_config.handlers
            if isinstance(handler_config, StarknetEventsHandlerConfig)
        ]

        if not contracts:
            self._logger.debug('No contract specified. No ABI to fetch.')
            return

        # deduplicated (by name) Datasource list
        datasources: list[AbiDatasource[Any]] = list(
            {
                datasource_config.name: cast('AbiDatasource[Any]', self._datasources[datasource_config.name])
                for datasource_config in index_config.datasources
                if isinstance(datasource_config, StarknetNodeDatasourceConfig)
            }.values()
        )

        if not datasources:
            raise ConfigurationError('No Starknet ABI datasources found')

        async for contract, abi_json in AbiDatasource.lookup_abi_for(contracts, using=datasources, logger=self._logger):
            abi_path = self._package.abi / contract.module_name / 'cairo_abi.json'

            if abi_path.exists():
                continue

            touch(abi_path)
            abi_path.write_bytes(json_dumps(abi_json))

    async def generate_schemas(self) -> None:
        from dipdup.abi.cairo import abi_to_jsonschemas

        self._cleanup_schemas()

        handler_config: HandlerConfig
        events: set[str] = set()

        for index_config in self._config.indexes.values():
            if isinstance(index_config, StarknetEventsIndexConfig):
                for handler_config in index_config.handlers:
                    events.add(handler_config.name)

        abi_to_jsonschemas(self._package, events)

    async def generate_hooks(self) -> None:
        pass

    async def generate_system_hooks(self) -> None:
        pass

    async def generate_handlers(self) -> None:
        pass

    def get_typeclass_name(self, schema_path: Path) -> str:
        module_name = schema_path.stem
        if schema_path.parent.name == 'starknet_events':
            class_name = f'{module_name}_payload'
        else:
            class_name = module_name
        return snake_to_pascal(class_name)

    async def _generate_type(self, schema_path: Path, force: bool) -> None:
        markers = {
            'starknet_events',
        }
        if not set(schema_path.parts).intersection(markers):
            return
        await super()._generate_type(schema_path, force)
