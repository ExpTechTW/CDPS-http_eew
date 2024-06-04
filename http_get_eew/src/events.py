from cdps.plugin.events import Event


class onEew(Event):
    """ 當 伺服器 啟動 """

    def __init__(self, data:list):
        self.eew = data #EEW資料
