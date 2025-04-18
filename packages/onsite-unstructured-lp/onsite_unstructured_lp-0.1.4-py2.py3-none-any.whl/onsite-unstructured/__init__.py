"""
兼容层，将对 onsite-unstructured 的导入重定向到 onsite-unstructured-lp
"""

import sys
import importlib.util
import importlib

# 由于包名中含有连字符，不能直接使用 import 语句
# 使用 importlib 动态导入

def _import_from_lp():
    """导入 onsite-unstructured-lp 包的内容"""
    try:
        # 尝试使用 importlib 导入带连字符的包
        lp_module = importlib.import_module("onsite-unstructured-lp")
        
        # 将其所有内容复制到当前模块
        for attr_name in dir(lp_module):
            if not attr_name.startswith('_'):
                globals()[attr_name] = getattr(lp_module, attr_name)
    except ImportError:
        pass

# 执行导入
_import_from_lp()

# 处理子模块的导入
class _ModuleFinder:
    def find_module(self, fullname, path=None):
        if fullname.startswith('onsite-unstructured.'):
            return self
        return None
        
    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
            
        # 直接使用带连字符的包名
        new_name = fullname.replace('onsite-unstructured', 'onsite-unstructured-lp')
        
        # 导入新模块
        try:
            module = importlib.import_module(new_name)
            
            # 注册到 sys.modules 中，使用旧名称
            sys.modules[fullname] = module
            return module
        except ImportError as e:
            raise e

# 安装导入钩子
sys.meta_path.insert(0, _ModuleFinder()) 