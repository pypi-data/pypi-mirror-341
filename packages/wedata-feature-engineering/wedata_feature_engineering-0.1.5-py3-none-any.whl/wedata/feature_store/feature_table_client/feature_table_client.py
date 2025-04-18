"""
特征表操作相关工具方法
"""

from typing import Union, List, Dict, Optional, Sequence, Any
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import StructType
import os

from feature_store.constants.constants import APPEND, DEFAULT_WRITE_STREAM_TRIGGER


class FeatureTableClient:
    """特征表操作类"""

    def __init__(
            self,
            spark: SparkSession
    ):
        self._spark = spark

    @staticmethod
    def _normalize_params(
            param: Optional[Union[str, Sequence[str]]],
            default_type: type = list
    ) -> list:
        """统一处理参数标准化"""
        if param is None:
            return default_type()
        return list(param) if isinstance(param, Sequence) else [param]

    @staticmethod
    def _validate_schema(df: DataFrame, schema: StructType):
        """校验DataFrame和schema的有效性和一致性"""
        # 检查是否同时为空
        if df is None and schema is None:
            raise ValueError("必须提供DataFrame或schema其中之一")

        # 检查schema匹配
        if df is not None and schema is not None:
            df_schema = df.schema
            if df_schema != schema:
                diff_fields = set(df_schema.fieldNames()).symmetric_difference(set(schema.fieldNames()))
                raise ValueError(
                    f"DataFrame与schema不匹配。差异字段: {diff_fields if diff_fields else '字段类型不一致'}"
                )

    @staticmethod
    def _validate_table_name(name: str):
        """验证特征表命名规范"""
        if name.count('.') < 2:
            raise ValueError("特征表名称需符合<catalog>.<schema>.<table>格式")

    @staticmethod
    def _validate_key_conflicts(primary_keys: List[str], timestamp_keys: List[str]):
        """校验主键与时间戳键是否冲突"""
        conflict_keys = set(timestamp_keys) & set(primary_keys)
        if conflict_keys:
            raise ValueError(f"时间戳键与主键冲突: {conflict_keys}")

    @staticmethod
    def _escape_sql_value(value: str) -> str:
        """转义SQL值中的特殊字符"""
        return value.replace("'", "''")

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
        # 参数标准化
        primary_keys = self._normalize_params(primary_keys)
        timestamp_keys = self._normalize_params(timestamp_keys)
        partition_columns = self._normalize_params(partition_columns)

        # 元数据校验
        self._validate_schema(df, schema)
        #self._validate_table_name(name)
        self._validate_key_conflicts(primary_keys, timestamp_keys)

        # 表名 格式：<catalog>.<schema>.<table>  catalog默认值：DataLakeCatalog，schema默认值：feature_store
        table_name = f'DataLakeCatalog.feature_store.{name}'

        # 检查表是否存在
        try:
            if self._spark.catalog.tableExists(table_name):
                raise ValueError(
                    f"表 '{table_name}' 已存在\n"
                    "解决方案：\n"
                    "1. 使用不同的表名\n"
                    "2. 删除现有表: spark.sql(f'DROP TABLE {name}')\n"
                )
        except Exception as e:
            raise ValueError(f"检查表存在性时出错: {str(e)}") from e

        # 推断表schema
        table_schema = schema or df.schema

        # 构建时间戳键属性
        timestamp_keys_ddl = []
        for timestamp_key in timestamp_keys:
            if timestamp_key not in primary_keys:
                raise ValueError(f"时间戳键 '{timestamp_key}' 必须是主键")
            timestamp_keys_ddl.append(f"`{timestamp_key}` TIMESTAMP")

        #从环境变量获取额外标签
        env_tags = {
            "project_id": os.getenv("WEDATA_PROJECT_ID", ""),  # wedata项目ID
            "engine_name": os.getenv("WEDATA_NOTEBOOK_ENGINE", ""),  # wedata引擎名称
            "user_uin": os.getenv("WEDATA_USER_UIN", "")  # wedata用户UIN
        }

        # 构建表属性（通过TBLPROPERTIES）
        tbl_properties = {
            "feature_table": "TRUE",
            "primaryKeys": ",".join(primary_keys),
            "comment": description or "",
            **{f"{k}": v for k, v in (tags or {}).items()},
            **{f"feature_{k}": v for k, v in (env_tags or {}).items()}
        }

        # 构建列定义
        columns_ddl = []
        for field in table_schema.fields:
            data_type = field.dataType.simpleString().upper()
            col_def = f"`{field.name}` {data_type}"
            if not field.nullable:
                col_def += " NOT NULL"
            # 添加字段注释(如果metadata中有comment)
            if field.metadata and "comment" in field.metadata:
                comment = self._escape_sql_value(field.metadata["comment"])
                col_def += f" COMMENT '{comment}'"
            columns_ddl.append(col_def)

        # 构建分区表达式
        partition_expr = (
            f"PARTITIONED BY ({', '.join([f'`{c}`' for c in partition_columns])})"
            if partition_columns else ""
        )

        # 核心建表语句
        ddl = f"""
        CREATE TABLE {table_name} (
            {', '.join(columns_ddl)}
        )
        USING PARQUET
        {partition_expr}
        TBLPROPERTIES (
            {', '.join(f"'{k}'='{self._escape_sql_value(v)}'" for k, v in tbl_properties.items())}
        )
        """

        # 打印sql
        print(f"create table ddl: {ddl}")

        # 执行DDL
        try:
            self._spark.sql(ddl)
            if df is not None:
                df.write.insertInto(table_name)
        except Exception as e:
            raise ValueError(f"建表失败: {str(e)}") from e

    def write_table(
            self,
            name: str,
            df: DataFrame,
            mode: str = APPEND,
            checkpoint_location: Optional[str] = None,
            trigger: Optional[Dict[str, Any]] = DEFAULT_WRITE_STREAM_TRIGGER
    ) -> Optional[StreamingQuery]:
        """
        写入特征表数据（支持批处理和流式写入）

        Args:
            name: 特征表名称（格式：<table>）
            df: 要写入的数据（DataFrame）
            mode: 写入模式（append/overwrite）
            checkpoint_location: 流式写入的检查点位置（仅流式写入需要）
            trigger: 流式写入触发条件（仅流式写入需要）

        Returns:
            如果是流式写入返回StreamingQuery对象，否则返回None

        Raises:
            ValueError: 当参数不合法时抛出
        """

        # 验证写入模式
        valid_modes = ["append", "overwrite"]
        if mode not in valid_modes:
            raise ValueError(f"无效的写入模式 '{mode}'，可选值: {valid_modes}")

        # 完整表名格式：<catalog>.<schema>.<table>
        table_name = f'DataLakeCatalog.feature_store.{name}'

        # 判断是否是流式DataFrame
        is_streaming = df.isStreaming

        try:
            if is_streaming:
                # 流式写入
                if not checkpoint_location:
                    raise ValueError("流式写入必须提供checkpoint_location参数")

                writer = df.writeStream \
                    .format("parquet") \
                    .outputMode(mode) \
                    .option("checkpointLocation", checkpoint_location)

                if trigger:
                    writer = writer.trigger(**trigger)

                return writer.toTable(table_name)
            else:
                # 批处理写入
                df.write \
                    .mode(mode) \
                    .insertInto(table_name)
                return None

        except Exception as e:
            raise ValueError(f"写入表'{table_name}'失败: {str(e)}") from e

    def read_table(
            self,
            name: str
    ) -> DataFrame:
        """
        从特征表中读取数据

        Args:
            name: 特征表名称（格式：<table>）

        Returns:
            包含表数据的DataFrame

        Raises:
            ValueError: 当表不存在或读取失败时抛出
        """
        # 构建完整表名
        table_name = f'DataLakeCatalog.feature_store.{name}'

        try:
            # 检查表是否存在
            if not self._spark.catalog.tableExists(table_name):
                raise ValueError(f"表 '{table_name}' 不存在")

            # 读取表数据
            return self._spark.read.table(table_name)

        except Exception as e:
            raise ValueError(f"读取表 '{table_name}' 失败: {str(e)}") from e

    def drop_table(
            self,
            name: str
    ) -> None:
        """
        删除特征表（表不存在时抛出异常）

        Args:
            name: 特征表名称（格式：<table>）

        Raises:
            ValueError: 当表不存在时抛出
            RuntimeError: 当删除操作失败时抛出

        示例:
            # 基本删除
            drop_table("user_features")
        """
        # 构建完整表名
        table_name = f'DataLakeCatalog.feature_store.{name}'

        try:
            # 检查表是否存在
            if not self._spark.catalog.tableExists(table_name):
                raise ValueError(f"表 '{table_name}' 不存在")

            # 执行删除
            self._spark.sql(f"DROP TABLE {table_name}")

        except ValueError as e:
            raise  # 直接抛出已知的ValueError
        except Exception as e:
            raise RuntimeError(f"删除表 '{table_name}' 失败: {str(e)}") from e
