from Controller import ElectronicLoadController


class LoadControllerModel:
    def __init__(self, port):
        self.controller = ElectronicLoadController(port)

    def configure_parameters(self, params):
        """配置硬件参数（不包含开关状态）"""
        try:
            self.controller.set_current(current=params['set_current'])
            self.controller.set_stop_voltage(voltage=params['stop_voltage'])
            self.controller.set_timer(seconds=params['timer'])
            return True
        except Exception as e:
            print(f"参数配置错误: {str(e)}")
            return False

    def enable_load_switch(self):
        """单独启用负载开关"""
        try:
            self.controller.set_load_switch(on=True)
            return True
        except Exception as e:
            print(f"开关启用失败: {str(e)}")
            return False