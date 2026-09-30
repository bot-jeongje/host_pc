import rclpy
from rclpy.node import Node
from shared_data import shared_memory

class RobotController(Node):
    def __init__(self, burger1_node, burger2_node): # 이거 말고 밑에꺼 써야함
    # def __init__(self, burger1_node, burger2_node, waffle_node, arm1_node, arm2_node, arm3_node):
        super().__init__('control')
        self.old_start_flag = False
        
        # Robot
        self.burger1 = burger1_node
        self.burger2 = burger2_node
        # self.waffle = waffle_node

        # # Arm
        # self.arm1 = arm1_node
        # self.arm2 = arm2_node
        # self.arm3 = arm3_node

        self.timer = self.create_timer(1.0, self.controlRobot) # print 문 빼고 나중에 0.1초로 바꾸자
        self.get_logger().info('RobotController 노드가 시작되었습니다.')

    def controlRobot(self):
        
        if  self.old_start_flag == shared_memory.start_flag:
            # no operate
            self.get_logger().info("정상 종료 : 이전 상태와 동일한 상태 입력 / 현 동작 유지")
        else:
            self.old_start_flag = shared_memory.start_flag

            if  self.old_start_flag == True:
                # 동작 내용
                self.burger1.send_goal("move_to_warehouse", 1.5)
                self.burger2.send_goal("move_to_warehouse", 5)
                self.get_logger().info("로봇 동작 시작")
            else:
                self.get_logger().info("로봇 정지")

            