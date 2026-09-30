import rclpy

from rclpy.action import ActionClient
from rclpy.node import Node
from host_pkg.action import Burger

from shared_data import shared_memory

class Burger2ActionClient(Node):
    def __init__(self):
        # 네임스페이스 'host' 지정 및 노드 이름 설정
        super().__init__('data', namespace='burger2') # 발행을 /burger2/host_data 로 할꺼임
        self._client = ActionClient(self, Burger, '/burger2/data') # 수신을 /host_server/robot_data 로 할꺼임

    def send_goal(self, command, speed):

        self.get_logger().info('Waiting for action server at /host/burger2...')
        self._client.wait_for_server()

        goal_msg = Burger.Goal()
        goal_msg.command = command
        goal_msg.cmd_val = speed

        self.get_logger().info(f"Goal msg CMD = {command}, Speed = {speed}")

        self._send_goal_future = self._client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_data):
        shared_memory.key = shared_memory.get_key()
        if shared_memory.key == False:
            return "ERROR 발생 : burger2_node"
        else:
            shared_memory.burger2_x_axis = feedback_data.feedback.robot_x
            shared_memory.burger2_y_axis = feedback_data.feedback.robot_y
            shared_memory.burger2_theta = feedback_data.feedback.robot_theta # string Data
            shared_memory.key = False
            
        self.get_logger().info(f"x_axis = {shared_memory.burger2_x_axis}, y_axis = {shared_memory.burger2_y_axis}, theta = {shared_memory.burger2_theta}")


    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("burger2 fail")
            # rclpy.shutdown() # 프로그램 자체를 꺼버리는 거
            return

        self.get_logger().info("burger2 success")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
        
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result received: success={result.success}, message="{result.message}"')
        # rclpy.shutdown() # 프로그램 자체를 꺼버리는 거
