from mysqlConnector import execute_sql
import generatorUtil


def main():
    gen = generatorUtil.create_generator()

    print("开始生成测试数据...")

    # 部门选择集合
    departments = {'技术部', '销售部', '市场部', '人事部', '财务部', '运营部'}

    database_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'test',
            'database': 'test',
            'charset': 'utf8mb4',
            'autocommit': False
    }



    # 定义生成器函数（使用lambda包装）
    # 格式：(生成函数, 是否需要唯一性)
    record_generators = {
        "name": (lambda: gen.generate_name(), True),  # varchar(50) not null
        "age": (lambda: gen.generate_number(18, 65), False),  # int null
        "city": (lambda: gen.generate_city(), False),  # varchar(30) null
        "salary": (lambda: gen.generate_float(3000.00, 50000.00, 2), False),  # decimal(10,2) null
        "department": (lambda: gen.generate_enum_value(departments), False),  # varchar(30) null
        "create_time": (lambda: gen.generate_datetime(), False),  # datetime
    }


    success, failed = execute_sql(
        database_config=database_config,
        record_generators=record_generators,
        total_count=100,  # 总数据量
        table_name='users_copy',
        batch_size=10,  # 每批1万条
        start_index=0  # 起始索引
    )


if __name__ == "__main__":
    main()
