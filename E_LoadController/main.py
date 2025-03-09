import time
import os
from Controller import ElectronicLoadController
from model import LoadControllerModel
from storage import DataLogger


def select_com_port():
    ports = ElectronicLoadController.scan_ch340_ports()
    if not ports:
        print("未找到CH340设备")
        exit()

    print("\n可用的COM端口:")
    for i, port in enumerate(ports):
        print(f"{i + 1}. {port}")

    while True:
        try:
            choice = int(input("请选择COM端口序号: ")) - 1
            return ports[choice]
        except (ValueError, IndexError):
            print("输入无效，请重新选择")


def get_hardware_params():
    """获取硬件参数（不包含开关状态）"""
    print("\n=== 请输入设备参数 ===")
    params = {
        'set_current': float(input("设定恒流值(A): ")),
        'stop_voltage': float(input("设定停止电压(V): ")),
        'timer': int(input("设定放电时间(秒): "))
    }
    return params


def get_switch_decision():
    """单独获取开关决策"""
    return input("\n是否现在开启负载开关？(y/n): ").lower() == 'y'


def main():
    # 选择COM端口
    selected_port = select_com_port()

    # 初始化模型和日志
    model = LoadControllerModel(selected_port)
    logger = DataLogger()

    try:
        # 步骤1：获取硬件参数
        hw_params = get_hardware_params()

        # 步骤2：配置硬件参数
        if not model.configure_parameters(hw_params):
            print("硬件参数配置失败！")
            return

        # 步骤3：确认开关状态
        if not get_switch_decision():
            print("未启用负载开关，程序退出")
            return

        # 步骤4：开启负载开关
        if not model.enable_load_switch():
            print("无法启用负载开关！")
            return

        # 步骤5：开始监测
        print("\n=== 放电已启动 ===")
        print("实时监测中（按Ctrl+C停止）...")
        logger.start_logging()
        last_status = True  # 初始状态为开启

        while True:
            data = model.controller.query()
            current_status = data['switch_status']['value']

            # 状态变化检测
            if current_status != last_status:
                if not current_status:  # 状态从开变关
                    print("\n检测到负载关闭，停止记录...")
                    break

            # 持续记录数据
            logger.log_data(data)
            last_status = current_status
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n用户手动终止操作")
    finally:
        # 停止记录并保存
        logger.stop_logging()
        save = input("\n是否保存采集数据？(y/n): ").lower() == 'y'
        final_filename = logger.filename if save else None

        if save:
            print(f"数据已保存至: {os.path.abspath(final_filename)}")
        else:
            if os.path.exists(final_filename):
                os.remove(final_filename)
            print("数据已丢弃")


if __name__ == "__main__":
    main()