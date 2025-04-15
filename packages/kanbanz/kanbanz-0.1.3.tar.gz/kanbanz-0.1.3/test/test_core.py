import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import re
import pytest


from kanban import Kanban,Pool




@pytest.fixture
def kanb():
    Kanban()



def test_pull(text:str,work:str):

    kanban_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作/实验室/ceshi.md"
    cm = Kanban(kanban_path)
    cm.pull()
    print(cm.kanban_dict,'canvs')
