"""
模块配置加载器
按模块加载 YAML 配置文件（定位器、测试数据）
期望值按语言拆分到独立文件：config/{module}/{lang}.yaml
如：config/login/zh_CN.yaml, config/login/en_US.yaml
"""

import yaml
import os

# 配置缓存
_config_cache = {}
_expectations_cache = {}

# 支持的语言列表
SUPPORTED_LANGUAGES = [
    "zh_CN", "en_US", "fr_FR", "ru_RU",
    "it_IT", "es_ES", "ko_KR", "ar_EG", "th_TH"
]


def load_module_config(module_name: str) -> dict:
    """
    加载模块配置（定位器 + 测试数据，不含期望值）

    Args:
        module_name: 模块名，如 'login'

    Returns:
        配置字典，包含 locators, test_data
    """
    config_path = f"config/{module_name}/{module_name}_config.yaml"

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_module_config(module_name: str, reload: bool = False) -> dict:
    """
    获取模块配置（带缓存）

    Args:
        module_name: 模块名，如 'login'
        reload: 是否强制重新加载

    Returns:
        配置字典
    """
    global _config_cache

    if reload or module_name not in _config_cache:
        _config_cache[module_name] = load_module_config(module_name)

    return _config_cache[module_name]


def load_expectations(module_name: str, language: str) -> dict:
    """
    加载指定语言的期望值文件

    Args:
        module_name: 模块名，如 'login'
        language: 语言代码，如 'zh_CN', 'en_US'

    Returns:
        期望值字典
    """
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"不支持的语言 '{language}'，可用: {SUPPORTED_LANGUAGES}")

    file_path = f"config/{module_name}/{language}.yaml"

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"期望值文件不存在: {file_path}\n"
            f"请创建 {file_path}，参考 config/{module_name}/zh_CN.yaml"
        )

    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_expectations(module_name: str, language: str = "zh_CN") -> dict:
    """
    获取断言期望值（指定语言）

    Args:
        module_name: 模块名，如 'login'
        language: 语言代码，如 'zh_CN', 'en_US'

    Returns:
        期望值字典
    """
    global _expectations_cache

    cache_key = f"{module_name}:{language}"

    if cache_key not in _expectations_cache:
        _expectations_cache[cache_key] = load_expectations(module_name, language)

    return _expectations_cache[cache_key]


def get_expectation(module_name: str, expectation_name: str, language: str = "zh_CN") -> str:
    """
    获取单个断言期望值

    Args:
        module_name: 模块名
        expectation_name: 期望值名
        language: 语言代码

    Returns:
        期望值字符串
    """
    expectations = get_expectations(module_name, language)
    return expectations[expectation_name]


def get_locators(module_name: str) -> dict:
    """获取定位器配置"""
    config = get_module_config(module_name)
    return config["locators"]


def get_locator(module_name: str, locator_name: str) -> str:
    """获取单个定位器"""
    locators = get_locators(module_name)
    return locators[locator_name]


def get_test_data(module_name: str, data_key: str) -> dict:
    """
    获取测试数据

    Args:
        module_name: 模块名
        data_key: 数据键，如 'valid' 或 'invalid'

    Returns:
        测试数据字典
    """
    config = get_module_config(module_name)
    return config["test_data"][data_key]


def get_available_languages(module_name: str) -> list:
    """
    获取模块已有期望值文件的语言列表

    Args:
        module_name: 模块名

    Returns:
        语言代码列表
    """
    config_dir = f"config/{module_name}"
    languages = []
    if os.path.isdir(config_dir):
        for f in os.listdir(config_dir):
            if f.endswith(".yaml") and f != f"{module_name}_config.yaml":
                languages.append(f.replace(".yaml", ""))
    return languages
