import rclpy
import json

from rclpy.node import Node
from std_msgs.msg import String

from shared_data import shared_memory
from control import RobotController

class WebDataPase(Node):
    def __init__(self):
        super().__init__('web_data_receiver')
        self.subscription = self.create_subscription(
            String,
            '/web_to_ros',
            self.listener_callback,
            10
        )

        # 2. ROS에서 웹으로 데이터를 보내는 발행자 (Publisher)
        self.publisher = self.create_publisher(
            String,
            '/ros_to_web',
            10
        )

        # 3. 주기적으로(예: 0.2초마다) 웹으로 로봇/공정 상태를 전송하는 타이머 설정
        self.timer = self.create_timer(0.2, self.send_status_to_web)

        self.get_logger().info('웹 데이터 노드가 시작되었습니다.')

    def listener_callback(self, msg):
        try:
            # 웹에서 JSON 문자열로 보낸 데이터를 딕셔너리로 변환
            data = json.loads(msg.data)

            shared_memory.key = shared_memory.get_key()
            if shared_memory.key == False:
                self.get_logger().info("ERROR 발생 : WebData Parsing 중 key 수신 불가")
            # 파이썬에서 변수와 상수값 추출
            
            shared_memory.product = data.get('product')
            shared_memory.quantity = data.get('quantity')
            shared_memory.start_flag = data.get('playing')

            # 터미널에 예쁘게 출력
            self.get_logger().info(f"[수신 성공] 시작 여부 : {shared_memory.start_flag} 수량 : {shared_memory.quantity} 제품 : {shared_memory.product}")

            shared_memory.key = False
            
        except json.JSONDecodeError:
            # JSON 형태가 아닐 경우 일반 문자열로 처리
            self.get_logger().info(f"Jason 이 아닌 데이터 수신 : {msg.data}")

    def send_status_to_web(self):
        """ROS 2에서 처리된 최신 상태를 웹으로 송신하는 함수"""
        status_data = {
            "burger1_x_axis" : shared_memory.burger1_x_axis,
            "burger1_y_axis" : shared_memory.burger1_y_axis,
            "burger1_theta" : shared_memory.burger1_theta,

            "burger2_x_axis" : shared_memory.burger2_x_axis,
            "burger2_y_axis" : shared_memory.burger2_y_axis,
            "burger2_theta" : shared_memory.burger2_theta,

            "message": "ROS 2 test 공정 입니다."
        }
        
        msg = String()
        msg.data = json.dumps(status_data)
        self.publisher.publish(msg)
        # self.get_logger().info('웹으로 상태 데이터 전송 완료')