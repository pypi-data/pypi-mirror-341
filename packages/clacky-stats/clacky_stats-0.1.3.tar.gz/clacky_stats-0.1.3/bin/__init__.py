__version__ = "0.1.3"

"""
Clacky AI 代码贡献统计工具

这个包提供了一组工具来分析和统计代码仓库中的贡献情况，
特别关注 ClackyAI 与人类开发者之间的协作。

主要功能：
- 按时间段统计代码贡献
- 按版本标签统计代码贡献
- 支持周报和月报统计
"""

from bin.blame import BlameAnalyzer
from bin.cli import main

__all__ = ['BlameAnalyzer', 'main'] 