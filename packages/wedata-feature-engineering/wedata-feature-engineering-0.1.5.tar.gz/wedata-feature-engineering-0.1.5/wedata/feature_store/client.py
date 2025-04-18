"""
Wedata FeatureStoreClient Python实现
"""

from __future__ import annotations
from typing import Union, List, Dict, Optional, Any
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import StructType

from feature_store.constants.constants import APPEND, DEFAULT_WRITE_STREAM_TRIGGER
from feature_store.entities.feature_function import FeatureFunction
from feature_store.entities.feature_lookup import FeatureLookup
from feature_store.entities.training_set import TrainingSet
from feature_store.feature_table_client.feature_table_client import FeatureTableClient
from feature_store.spark_client.spark_client import SparkClient
from feature_store.training_set_client.training_set_client import TrainingSetClient
from feature_store.utils.feature_utils import format_feature_lookups_and_functions


class FeatureStoreClient:
    """特征存储统一客户端，提供特征全生命周期管理能力"""

    def __init__(self, spark: SparkSession):
        """
        :param spark: 已初始化的SparkSession对象
        """
        self._spark = spark
        self._spark_client = SparkClient(spark)
        self._feature_table_client = FeatureTableClient(spark)

    def create_table(
            self,
            name: str,
            primary_keys: Union[str, List[str]],
            df: Optional[DataFrame] = None,
            *,
            timestamp_keys: Union[str, List[str], None] = None,
            partition_columns: Union[str, List[str], None] = None,
            schema: Optional[StructType] = None,
            description: Optional[str] = None,
            tags: Optional[Dict[str, str]] = None
    ):
        """
        创建特征表（支持批流数据写入）

        Args:
            name: 特征表全称（格式：<table>）
            primary_keys: 主键列名（支持复合主键）
            df: 初始数据（可选，用于推断schema）
            timestamp_keys: 时间戳键（用于时态特征）
            partition_columns: 分区列（优化存储查询）
            description: 业务描述
            tags: 业务标签

        Returns:
            FeatureTable实例

        Raises:
            ValueError: 当schema与数据不匹配时
        """

        return self._feature_table_client.create_table(
            name=name,
            primary_keys=primary_keys,
            df=df,
            timestamp_keys=timestamp_keys,
            partition_columns=partition_columns,
            schema=schema,
            description=description,
            tags=tags
        )


    def read_table(self, name: str) -> DataFrame:
        """
        读取特征表数据

        Args:
            name: 特征表名称

        Returns:
            DataFrame: 包含特征表数据的DataFrame对象
        """
        return self._feature_table_client.read_table(name)


    def drop_table(self, name: str) -> None:
        """
        删除特征表

        Args:
            name: 要删除的特征表名称

        Returns:
            None
        """
        return self._feature_table_client.drop_table(name)


    def create_training_set(
            self,
            df: DataFrame,
            feature_lookups: List[Union[FeatureLookup, FeatureFunction]],
            label: Union[str, List[str], None],
            exclude_columns: Optional[List[str]] = None,
            **kwargs,
    ) -> TrainingSet:

        """
        创建训练集

        Args:
            df: 基础数据
            feature_lookups: 特征查询列表
            label: 标签列名
            exclude_columns: 排除列名

        Returns:
            TrainingSet实例
        """

        if exclude_columns is None:
            exclude_columns = []

        features = feature_lookups
        del feature_lookups

        features = format_feature_lookups_and_functions(self._spark_client, features)
        # 创建TrainingSetClient实例
        training_set_client = TrainingSetClient(self._spark_client)
        return training_set_client.create_training_set_from_feature_lookups(
            df=df,
            feature_lookups=features,
            label=label,
            exclude_columns=exclude_columns,
            **kwargs
        )

    def write_table(
            self,
            name: str,
            df: DataFrame,
            mode: str = APPEND,
            checkpoint_location: Optional[str] = None,
            trigger: Dict[str, Any] = DEFAULT_WRITE_STREAM_TRIGGER,
    ) -> Optional[StreamingQuery]:

        """
        写入数据到特征表（支持批处理和流式处理）

        Args:
            name: 特征表名称
            df: 要写入的数据DataFrame
            mode: 写入模式（默认追加）
            checkpoint_location: 流式处理的检查点位置（可选）
            trigger: 流式处理触发器配置（默认使用系统预设）

        Returns:
            如果是流式写入返回StreamingQuery对象，否则返回None
        """

        return self._feature_table_client.write_table(
            name=name,
            df=df,
            mode=mode,
            checkpoint_location=checkpoint_location,
            trigger=trigger,
        )