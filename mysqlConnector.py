from datetime import datetime
from typing import List, Any, Dict, Tuple, Callable

import pymysql


def execute_sql(
        database_config: Dict[str, Any],
        record_generators: Dict[str, Tuple[Callable, bool]],
        total_count: int,
        table_name: str,
        batch_size: int = 1000,
        start_index: int = 0
):
    """
    边生成数据边执行SQL，避免内存溢出
    :param record_generators: 字段生成器配置
    :param total_count: 总数据量
    :param table_name: 表名
    :param batch_size: 每批次大小
    :param start_index: 起始索引
    """
    connection = None
    success_count = 0
    failed_count = 0

    try:
        # 建立数据库连接
        connection = pymysql.connect(**database_config)
        cursor = connection.cursor()

        print(f"开始生成并插入 {total_count} 条数据...")
        print(f"批次大小: {batch_size}")
        print("-" * 50)

        # 计算总批次数
        total_batches = (total_count + batch_size - 1) // batch_size

        # 按批次处理
        for batch_num in range(total_batches):
            # 计算当前批次的数据量
            current_batch_size = min(batch_size, total_count - batch_num * batch_size)
            batch_data = []

            # 生成当前批次的数据
            for i in range(current_batch_size):
                record_data = {}
                current_index = start_index + batch_num * batch_size + i

                for key, (value_generator, is_unique) in record_generators.items():
                    if is_unique:
                        # 对于需要唯一性的字段，添加索引
                        record_data[key] = f"{value_generator()}_{current_index}"
                    else:
                        record_data[key] = value_generator()

                batch_data.append(record_data)

            # 生成并执行SQL
            batch_success = 0
            for row in batch_data:
                try:
                    # 构建SQL语句
                    columns = ', '.join(row.keys())
                    placeholders = ', '.join(['%s'] * len(row))
                    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                    # 准备值
                    values = []
                    for value in row.values():
                        if isinstance(value, datetime):
                            values.append(value.strftime('%Y-%m-%d %H:%M:%S'))
                        else:
                            values.append(value)

                    # 执行SQL
                    cursor.execute(sql, values)
                    batch_success += 1
                    success_count += 1

                except Exception as e:
                    failed_count += 1
                    # 可以记录错误日志
                    continue

            try:
                connection.commit()

                processed = (batch_num + 1) * batch_size
                if processed > total_count:
                    processed = total_count
                progress = (processed / total_count) * 100

                print(f"批次 {batch_num + 1}/{total_batches}: "
                      f"进度 {progress:.1f}% ({processed}/{total_count}) - "
                      f"本批次成功: {batch_success}/{current_batch_size}")

            except Exception as e:
                connection.rollback()
                print(f"批次 {batch_num + 1} 提交失败: {str(e)}")
                success_count -= batch_success
                failed_count += batch_success

        print("-" * 50)
        print(f"执行完成！成功: {success_count} 条, 失败: {failed_count} 条")

        return success_count, failed_count

    except Exception as e:
        print(f"数据库连接错误: {str(e)}")
        return 0, total_count

    finally:
        if connection:
            connection.close()
__all__ = ["execute_sql"]