import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from host_pkg.action import Burger1

class Burger1ActionServer(Node):
    def __init__(self):
        super().__init__('data', namespace='burger1')
        self._action_server = ActionServer(
        self,
        Burger1,
        '/burger1/data',
        self.execute_callback
        )
        self.get_logger().info('Host Burger1 Action Server is ready under namespace "/burger1".')


    def execute_callback(self, goal_handle):
        self.get_logger().info(f"Receive Goal Data : CMD = {goal_handle.request.command} Speed = {goal_handle.request.cmd_val}")
    
        feedback_msg = Burger1.Feedback()

        for i in range(0,10):
            # 실제 로봇 x,y축 및 바라보는 방향으로 수정 필요
            feedback_msg.robot_x = float(i)
            feedback_msg.robot_y = float(i)

            if i < 5:
                feedback_msg.robot_theta = "front"
            else:
                feedback_msg.robot_theta = "back"
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1.0)
            
        if i == 9:
            goal_handle.succeed()
        else:
            goal_handle.abort()

        result = Burger1.Result()
        result.success = True
        result.message = "Burger1 arrived _Dest_"
        self.get_logger().info('Goal succeeded!')
        return result
        
def main(args=None):
    rclpy.init(args=args)
    server = Burger1ActionServer()
    try:
        rclpy.spin(server)
    except KeyboardInterrupt:
        pass
    finally:
        server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

