# onsite-unstructured-lp

一个包含仿真模型的Python包，用于无结构环境下的自动驾驶仿真。

## 安装

```
pip install onsite-unstructured-lp
```

## 兼容性

本包已添加兼容层，支持从旧版包名导入：

```python
# 旧版导入方式，仍然有效
import importlib
scenarioOrganizer = importlib.import_module("onsite-unstructured.dynamic_scenes.scenarioOrganizer1")

# 新版导入方式
scenarioOrganizer = importlib.import_module("onsite-unstructured-lp.dynamic_scenes.scenarioOrganizer1")
```
