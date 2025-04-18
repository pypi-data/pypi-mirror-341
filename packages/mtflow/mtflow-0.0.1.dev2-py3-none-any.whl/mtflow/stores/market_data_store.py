from __future__ import annotations
from typing import TYPE_CHECKING, TypeAlias
if TYPE_CHECKING:
    import datetime
    from pfeed.typing import tDATA_SOURCE, GenericFrame
    from pfeed.enums import DataStorage
    from pfeed.feeds.market_feed import MarketFeed
    from pfeed.data_models.market_data_model import MarketDataModel
    from pfund.typing import ComponentName
    from pfund.datas.resolution import Resolution
    from pfund.products.product_base import BaseProduct

from dataclasses import dataclass, field

import polars as pl

from pfeed.enums import DataSource
from mtflow.stores.base_data_store import BaseDataStore


MarketDataKey: TypeAlias = str
ProductName: TypeAlias = str
ResolutionRepr: TypeAlias = str


@dataclass
class MarketDataMetadata:
    data_source: DataSource
    data_origin: str
    product: BaseProduct
    resolution: Resolution
    start_date: datetime.date
    end_date: datetime.date
    consumers: list[ComponentName] = field(default_factory=list)


class MarketDataStore(BaseDataStore):
    _registry: dict[MarketDataKey, MarketDataMetadata]
    _datas: dict[MarketDataKey, GenericFrame]
    
    @staticmethod
    def _generate_data_key(
        data_source: DataSource,
        data_origin: str,
        product: BaseProduct,
        resolution: Resolution,
    ) -> MarketDataKey:
        return f"{data_source}:{data_origin}:{product.name}:{repr(resolution)}"
    
    def _register_data(
        self,
        consumer: ComponentName,
        data_source: tDATA_SOURCE,
        data_origin: str,
        product: BaseProduct,
        resolution: Resolution,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> MarketDataKey:
        data_source = DataSource[data_source.upper()]
        data_origin = data_origin or data_source.value
        data_key = self._generate_data_key(
            data_source=data_source,
            data_origin=data_origin,
            product=product,
            resolution=resolution,
        )
        if data_key not in self._registry:
            self._registry[data_key] = MarketDataMetadata(
                data_source=data_source,
                data_origin=data_origin,
                product=product,
                resolution=resolution,
                start_date=start_date,
                end_date=end_date,
                consumers=[consumer],
            )
        else:
            if consumer not in self._registry[data_key].consumers:
                self._registry[data_key].consumers.append(consumer)

    def _materialize(self):
        '''Loads data from pfeed's data lakehouse into the store'''
        dfs = []
        for metadata in self._registry.values():
            data_source: DataSource = metadata['data_source']
            self._add_feed(data_source)
            data_origin = metadata['data_origin']
            product: BaseProduct = metadata['product']
            resolution: Resolution = metadata['resolution']
            data_key = self._generate_data_key(
                data_source=data_source,
                data_origin=data_origin,
                product=product.name,
                resolution=repr(resolution),
            )
            df = self._get_historical_data(
                data_source=data_source,
                data_origin=data_origin,
                product=product,
                resolution=resolution,
                start_date=metadata['start_date'],
                end_date=metadata['end_date'],
                storage=self._storage,
                storage_options=self._storage_options,
            )
            assert df is not None, f'No data found for {data_key}'
            dfs.append(df)
            # TODO: add data_source as new column? need to differentiate historical data from live data
        self._set_data(pl.concat(dfs))
    
    def _get_historical_data(
        self,
        data_source: DataSource,
        data_origin: str,
        product: BaseProduct,
        resolution: Resolution,
        start_date: datetime.date,
        end_date: datetime.date,
        storage: DataStorage,
        storage_options: dict,
    ) -> GenericFrame:
        from pfeed import get_market_feed
        feed = get_market_feed(
            data_source=data_source.value,
            data_tool=self._data_tool.value,
            use_ray=False,  # FIXME
            use_deltalake=True,
        )
        lf: pl.LazyFrame = feed.retrieve(
            auto_transform=False,
        )
        df = lf.head(1).collect()
        # TODO
        retrieved_resolution = ...
        is_resample_required = ...
        
        df = feed.get_historical_data(
            product=product.basis, 
            symbol=product.symbol,
            resolution=resolution,
            start_date=start_date, 
            end_date=end_date,
            data_origin=data_origin,
            from_storage=storage.value,
            storage_options=storage_options,
            retrieve_per_date=is_resample_required,
            **product.specs
        )
        # TEMP
        print('***got historical data:\n', df)
