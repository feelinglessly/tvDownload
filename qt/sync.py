from qt.widgets import TextEdit
from stores.stores import get_store


class SyncTextEdit(TextEdit):
    def __init__(self, readonly=False):
        """
        :param readonly:
        """
        super().__init__(readonly)
        store = get_store()
        store.to_connect(self.sync)

    def sync(self):
        store = get_store()
        text = store.list()
        self.set_markdown(self.format_text(text))

    def format_text(self, text):
        title = """
| 平台 | 网址 | 名称 | 自动下一集 | 存放位置 | 状态 | 当前剧级 |
|------|------|------|------|------|------|------|
"""
        contents = []
        for i in text:
            contents.append(
                f"| {i.platform} | {i.url_line} | {i.host_line} "
                f"| {i.auto_next} | {i.file_dir} | {i.status} | {i.nid} |"
            )

        return title + "\n".join(contents)


#         """| 状态 | 描述 | 进度 |
# |------|------|------|
# | ✅ 完成 | **重要任务** | 100% |
# | ⚠️ 进行中 | *普通任务* | 75% |
# | ❌ 未开始 | ~~取消的任务~~ | 0% |"""



