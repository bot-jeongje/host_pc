import time

MAXIMUM_KEY_ERROR = 10

class SharedState:
    def __init__(self):
        self.key = False
        self.get_key_error_cnt = 0


        self.start_flag = False
        self.quantity = 0
        self.product = ""

        #Robot - burger1
        self.burger1_x_axis = 0.0
        self.burger1_y_axis = 0.0
        self.burger1_theta = ""

        #Robot - burger2
        self.burger2_x_axis = 0.0
        self.burger2_y_axis = 0.0
        self.burger2_theta = ""

        #Robot - waffle
        self.waffle_x_axis = 0.0
        self.waffle_y_axis = 0.0
        self.waffle_theta = ""

    def get_key(self):
        while self.key == True:
            time.sleep(0.001) # wait 1ms

        if self.key == False:
            return True
        
        else:
            if  self.get_key_error_cnt >= MAXIMUM_KEY_ERROR:
                self.get_key_error_cnt = 0
                return False
            else:
                self.get_key_error_cnt += 1
                self.get_key()
              
# 전역에서 쓸 수 있는 단일 공유 객체 생성
shared_memory = SharedState()