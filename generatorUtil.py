from faker import Faker
from datetime import datetime, timedelta
import random
from typing import Optional, List, Dict, Any, Callable, Tuple, Union


class DataGenerator:

    def __init__(self, locale: str = 'zh_CN'):
        """
        初始化数据生成器
        :param locale: 语言环境，默认为中文
        zh_CN 中文  en_US 英文
        """
        self.fake = Faker(locale)
        Faker.seed(None)  # 每次运行生成不同的数据
    
    def set_seed(self, seed: int):
        """设置随机种子以获得可重复的结果"""
        Faker.seed(seed)
        random.seed(seed)
    
    # 姓名相关
    def generate_name(self) -> str:
        """生成完整姓名"""
        return self.fake.name()
    
    def generate_first_name(self) -> str:
        """生成名"""
        return self.fake.first_name()
    
    def generate_last_name(self) -> str:
        """生成姓"""
        return self.fake.last_name()
    
    # 地址相关
    def generate_address(self) -> str:
        """生成完整地址"""
        return self.fake.address()
    
    def generate_city(self) -> str:
        """生成城市名"""
        return self.fake.city()
    
    def generate_province(self) -> str:
        """生成省份"""
        return self.fake.province()
    
    def generate_postcode(self) -> str:
        """生成邮政编码"""
        return self.fake.postcode()
    
    def generate_street_address(self) -> str:
        """生成街道地址"""
        return self.fake.street_address()
    
    # 时间相关
    def generate_datetime(self, start_date: Optional[datetime] = None, 
                         end_date: Optional[datetime] = None) -> datetime:
        """
        生成指定范围内的随机时间
        :param start_date: 起始时间
        :param end_date: 结束时间
        :return: 随机时间
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
        
        return self.fake.date_time_between(start_date=start_date, end_date=end_date)
    
    def generate_date(self, start_date: Optional[str] = '-1y', 
                      end_date: Optional[str] = 'today') -> str:
        """
        生成日期字符串
        :param start_date: 起始日期，支持 '-30d', '-1y' 等格式
        :param end_date: 结束日期
        :return: YYYY-MM-DD 格式的日期
        """
        return str(self.fake.date_between(start_date=start_date, end_date=end_date))
    
    def generate_time(self) -> str:
        """生成时间字符串 HH:MM:SS"""
        return self.fake.time()

    
    def generate_timestamp(self) -> int:
        """生成Unix时间戳"""
        return self.fake.unix_time()
    
    # 联系方式相关
    def generate_phone_number(self) -> str:
        """生成手机号码"""
        return self.fake.phone_number()
    
    def generate_email(self) -> str:
        """生成邮箱地址"""
        return self.fake.email()

    
    # 公司相关
    def generate_company_name(self) -> str:
        """生成公司名称"""
        return self.fake.company()
    
    def generate_job(self) -> str:
        """生成职位名称"""
        return self.fake.job()
    
    # 互联网相关
    def generate_username(self) -> str:
        """生成用户名"""
        return self.fake.user_name()
    
    def generate_password(self, length: int = 10, special_chars: bool = True) -> str:
        """生成密码"""
        return self.fake.password(length=length, special_chars=special_chars)
    
    def generate_url(self) -> str:
        """生成URL"""
        return self.fake.url()
    
    def generate_ipv4(self) -> str:
        """生成IPv4地址"""
        return self.fake.ipv4()
    
    def generate_mac_address(self) -> str:
        """生成MAC地址"""
        return self.fake.mac_address()
    
    # 文本相关
    def generate_text(self, max_chars: int = 200) -> str:
        """生成随机文本"""
        return self.fake.text(max_nb_chars=max_chars)
    
    def generate_sentence(self, nb_words: int = 10) -> str:
        """生成句子"""
        return self.fake.sentence(nb_words=nb_words)
    
    def generate_paragraph(self, nb_sentences: int = 5) -> str:
        """生成段落"""
        return self.fake.paragraph(nb_sentences=nb_sentences)
    
    # 数字相关
    def generate_number(self, min_value: int = 0, max_value: int = 9999) -> int:
        """生成指定范围内的随机整数"""
        return self.fake.random_int(min=min_value, max=max_value)
    
    def generate_float(self, min_value: float = 0.0, max_value: float = 1000.0, 
                      decimals: int = 2) -> float:
        """生成指定范围内的随机浮点数"""
        return round(random.uniform(min_value, max_value), decimals)
    
    def generate_boolean(self) -> bool:
        """生成随机布尔值"""
        return self.fake.boolean()
    
    # 身份相关
    def generate_ssn(self) -> str:
        """生成身份证号码（18位）"""
        return self.fake.ssn()
    
    def generate_license_plate(self) -> str:
        """生成车牌号"""
        return self.fake.license_plate()
    
    # 金融相关
    def generate_credit_card_number(self) -> str:
        """生成信用卡号"""
        return self.fake.credit_card_number()
    
    def generate_bank_account(self, length: int = 16) -> str:
        """生成银行账号"""
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    def generate_currency_code(self) -> str:
        """生成货币代码"""
        return self.fake.currency_code()

    def generate_enum_value(self, choices: set) -> Any:
        """
        从给定的集合中随机选择一个值
        :param choices: 可选值的集合
        :return: 随机选中的值
        """
        if not choices:
            raise ValueError("集合不能为空")
        return random.choice(list(choices))

def generate_batch_data(record: Dict[str, Tuple[Callable, bool]], batch_size: int,start_index:int=0) -> List[Dict[str, Any]]:
    """
    批量生成数据
    :param record: 字段生成器配置 {字段名: (生成函数, 是否唯一)}
    :param batch_size: 生成数量
    :param start_index: 唯一值的起始索引
    :return: 数据列表
    """
    batch_data = []
    
    # 计算5%的间隔
    progress_interval = max(1, batch_size // 20)  # 每5%的数据量
    
    print(f"开始生成 {batch_size} 条数据...")
    
    for i in range(batch_size):
        record_data = {}
        for key, (value_generator, uniq) in record.items():
            if uniq:
                record_data[key] = value_generator() + str(start_index)
                start_index += 1
            else:
                record_data[key] = value_generator()
        batch_data.append(record_data)
        
        # 每5%进度提示一次
        if (i + 1) % progress_interval == 0:
            progress = ((i + 1) / batch_size) * 100
            print(f"数据生成进度: {progress:.1f}% ({i + 1}/{batch_size})")
    
    print(f"数据生成完成！共 {batch_size} 条")
    return batch_data




def create_generator(locale: str = 'zh_CN') -> DataGenerator:
    return DataGenerator(locale)


