# sql_generator (English Version)

Python script for quickly generating database test data (currently supports MySQL)

## Required Libraries

- **Faker**: For generating various types of mock data (names, addresses, emails, etc.)
- **PyMySQL**: MySQL database connection and operations
- **random**: Python standard library for generating random numbers
- **datetime**: Python standard library for handling date and time
- **typing**: Python standard library for type annotations

## Usage Instructions

### 1. Install Dependencies

```bash
pip install faker pymysql
```

### 2. Configure Database Connection

Modify the database configuration in `__init__.py`:

```python
database_config = {
    'host': 'localhost',
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database_schema',
    'charset': 'utf8mb4',
    'autocommit': False
}
```

### 3. Define Data Generation Rules

Use the `record_generators` dictionary to define generation rules for each field:

```python
record_generators = {
    "name": (lambda: gen.generate_name(), True),  # Second parameter True means uniqueness is required
    "age": (lambda: gen.generate_number(18, 65), False),
    "city": (lambda: gen.generate_city(), False),
    "salary": (lambda: gen.generate_float(3000.00, 50000.00, 2), False),
    "department": (lambda: gen.generate_enum_value(departments), False),
    "create_time": (lambda: gen.generate_datetime(), False),
}
```

Test Database DDL:
```mysql
    create table users
    (
        id          int auto_increment
            primary key,
        name        varchar(50)    not null,
        age         int            null,
        city        varchar(30)    null,
        salary      decimal(10, 2) null,
        department  varchar(30)    null,
        create_time datetime       null
    );
```

### 4. Execute Data Generation

Call the `execute_sql` function to generate and insert data:

```python
success, failed = execute_sql(
    database_config=database_config,
    record_generators=record_generators,
    total_count=100,        # Total amount of data
    table_name='users_copy', # Target table name
    batch_size=10,          # Records per batch
    start_index=0           # Starting index
)
```

### 5. Run the Script

```bash
python __init__.py
```

## Important Notes

### 1. Memory Optimization
- The script uses a generate-and-insert approach to avoid memory overflow from generating large amounts of data at once
- Control the amount of data processed per batch with the `batch_size` parameter

### 2. Uniqueness Handling
- For fields requiring unique values, set the second parameter to `True` in the generator configuration
- The system automatically appends an index to generated values to ensure uniqueness

### 3. Performance Optimization
- Batch insertion: Data is processed in batches with unified commits
- Progress display: Real-time processing progress for easy monitoring
- Error handling: Single record insertion failures don't affect overall execution

### 4. Supported Data Types
- Strings: Names, cities, addresses, emails, etc.
- Numbers: Integers, floats (with precision control)
- Date/time: Supports custom time ranges
- Enum values: Random selection from predefined sets
- Boolean values: Random True/False

### 5. Custom Extensions
- Add new generation methods in `generatorUtil.py`
- Support custom lambda expressions to generate data in specific formats
- Generate test data in different languages by modifying the locale parameter (e.g., 'en_US' for English data)


# sql_generator(中文版本)

快速生成数据库测试数据的Python脚本(目前适配mysql)

## 使用的库

- **Faker**: 用于生成各种类型的模拟数据（姓名、地址、邮箱等）
- **PyMySQL**: MySQL数据库连接和操作
- **random**: Python标准库，用于生成随机数
- **datetime**: Python标准库，用于处理日期时间
- **typing**: Python标准库，用于类型注解

## 使用说明

### 1. 安装依赖

```bash
pip install faker pymysql
```

### 2. 配置数据库连接

在 `__init__.py` 中修改数据库配置：

```python
database_config = {
    'host': 'localhost',
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database_schema',
    'charset': 'utf8mb4',
    'autocommit': False
}
```

### 3. 定义数据生成规则

使用 `record_generators` 字典定义每个字段的生成规则：

```python
record_generators = {
    "name": (lambda: gen.generate_name(), True),  # 第二个参数True表示需要唯一性
    "age": (lambda: gen.generate_number(18, 65), False),
    "city": (lambda: gen.generate_city(), False),
    "salary": (lambda: gen.generate_float(3000.00, 50000.00, 2), False),
    "department": (lambda: gen.generate_enum_value(departments), False),
    "create_time": (lambda: gen.generate_datetime(), False),
}
```

测试数据库DDL:
```mysql
    create table users
    (
        id          int auto_increment
            primary key,
        name        varchar(50)    not null,
        age         int            null,
        city        varchar(30)    null,
        salary      decimal(10, 2) null,
        department  varchar(30)    null,
        create_time datetime       null
    );
```

### 4. 执行数据生成

调用 `execute_sql` 函数生成并插入数据：

```python
success, failed = execute_sql(
    database_config=database_config,
    record_generators=record_generators,
    total_count=100,        # 总数据量
    table_name='users_copy', # 目标表名
    batch_size=10,          # 每批次数量
    start_index=0           # 起始索引
)
```

### 5. 运行脚本

```bash
python __init__.py
```

## 注意点

### 1. 内存优化
- 脚本采用边生成边插入的方式，避免一次性生成大量数据导致内存溢出
- 通过 `batch_size` 参数控制每批次处理的数据量

### 2. 唯一性处理
- 对于需要唯一值的字段，在生成器配置中设置第二个参数为 `True`
- 系统会自动在生成的值后添加索引确保唯一性

### 3. 性能优化
- 批量插入：数据按批次处理，每批次统一提交
- 进度提示：实时显示处理进度，便于监控
- 错误处理：单条数据插入失败不影响整体执行

### 4. 数据类型支持
- 字符串：姓名、城市、地址、邮箱等
- 数字：整数、浮点数（支持精度控制）
- 日期时间：支持自定义时间范围
- 枚举值：从预定义集合中随机选择
- 布尔值：随机True/False

### 5. 自定义扩展
- 可以在 `generatorUtil.py` 中添加新的生成方法
- 支持自定义lambda表达式生成特定格式的数据
- 可以通过修改locale参数生成不同语言的测试数据（如 'en_US' 生成英文数据）

---


