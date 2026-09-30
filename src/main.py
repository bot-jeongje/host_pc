import rclpy
import threading
from rclpy.executors import MultiThreadedExecutor
from burger1_node import Burger1ActionClient
from burger2_node import Burger2ActionClient
from web_node import WebDataPase

from control import RobotController

def main(args=None):
    rclpy.init(args=args)

    WebDataPaser = WebDataPase()

    Burger1Act = Burger1ActionClient()
    Burger2Act = Burger2ActionClient()

    Controller = RobotController(Burger1Act, Burger2Act)

    # Burger1Act.send_goal(command="move_forward", speed=1.5)

    executor = MultiThreadedExecutor()
    executor.add_node(WebDataPaser)
    executor.add_node(Burger1Act)
    executor.add_node(Burger2Act)
    executor.add_node(Controller)
    # 핵심 수정: send_goal을 별도 스레드에서 실행하여 main이 멈추지 않고 즉시 executor.spin()으로 진입하게 함

    try:
        executor.spin()

    except KeyboardInterrupt:
        Burger1Act.destroy_node()
        Burger2Act.destroy_node()
        WebDataPaser.destroy_node()
        Controller.destroy_node()
        rclpy.shutdown()
        pass

if __name__ == '__main__':
    main()