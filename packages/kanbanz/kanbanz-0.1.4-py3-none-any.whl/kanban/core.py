"""
kanban manager
"""
from enum import Enum
from .utils import read,write

class Pool(Enum):
    """
    预备池,就绪池,阻塞池,执行池,完成池,酱油池
    """
    预备池 ='预备池'
    就绪池 ='就绪池'
    阻塞池 ='阻塞池'
    执行池 ='执行池'
    完成池 ='完成池'
    酱油池 ='酱油池'


class Kanban():
    """
    看板管理工具
    """
    def __init__(self,kanban_path:str):
        """
        kanban_path 路径
        """
        self.kanban_path = kanban_path
        self.kanban_dict = {}

    def pull(self) -> None:
        """
        从文档拉取信息到 kanban_dict 属性。

        该方法打开指定的看板路径文件，读取其内容，并使用 _read 方法解析文本，
        将解析后的数据存储到 kanban_dict 属性中。
        """
        with open(self.kanban_path, 'r') as f:
            text = f.read()
        self.kanban_dict = read(text)

    def push(self) -> None:
        """
        将 kanban_dict 属性中的信息写入到文档。

        该方法使用 _write 方法将 kanban_dict 属性中的数据转换为文本格式，
        然后将该文本写入到指定的看板路径文件中。
        """
        text = write(self.kanban_dict)
        with open(self.kanban_path, 'w') as f:
            f.write(text)

    def insert(self, text: str, pool: Pool) -> None:
        """
        在指定的池中插入一条新的任务信息。

        Args:
            text (str): 任务的描述信息。
            pool (Pool): 要插入任务的池。

        Returns:
            None
        """
        self.kanban_dict[pool.value].append({'status': ' ', 'description': text, 'id': 12, 'level': 2})

    def pop(self, inputs: str, by: str, pool: Pool) -> None:
        """
        从指定的池中删除一条任务信息。

        Args:
            inputs (str): 用于匹配的任务信息，可以是描述或ID。
            by (str): 匹配的方式，'id' 或 'description'。
            pool (Pool): 要从中删除任务的池。

        Returns:
            None
        """
        def delete_by_description(data: list, description: str) -> list:
            for i, item in enumerate(data):
                if item.get('description') == description:
                    del data[i]
                    return data
            print(f"未找到描述为 '{description}' 的数据列")
            return data

        def delete_by_id(data: list, target_id: str) -> list:
            for i, item in enumerate(data):
                if item.get('id') == target_id:
                    del data[i]
                    return data
            print(f"未找到ID为 '{target_id}' 的数据列")
            return data

        data = self.kanban_dict[pool.value]
        if by == 'id':
            delete_by_id(data, inputs)
        elif by == 'description':
            delete_by_description(data, inputs)

    def select_by_pool(self, pool:Pool)->list[str]:
        """通过事件池进行选择

        Args:
            pool (Pool): 枚举的池类型

        Returns:
            list[str]: 返回对应的事件名称列表
        """

        pools = self.kanban_dict.get(pool.value)
        return [des.get("description") for des in pools]
        
    def select_by_tags(self, tags_name:str):
        pass

    def select_by_word(self,word:str)->list[str]:
        """通过关键字选择

        Args:
            word (str): 关键字

        Returns:
            list[str]: 返回的查询到的core内容
        """
        output = []
        for p,content in self.kanban_dict.items():
            for core in content:
                if word in core.get('description'):
                    output.append(core.get("description"))
        return output

    def select_by_word_and_pool(self,word:str,pool:Pool)->list[str]:
        """通过关键字选择

        Args:
            word (str): 关键字

        Returns:
            list[str]: 返回的查询到的core内容
        """
        output = []

        content = self.kanban_dict.get(pool.value)
        for core in content:
            if word in core.get('description'):
                output.append(core.get("description"))

        return output
