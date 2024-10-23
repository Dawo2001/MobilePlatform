class PID:
    def __init__(self):
        self.kp = 0.5
        self.ki = 0.5
        self.kd = 0.5
        self.dt = 1  
        self.setpoint = (0, 0)
        self.prev_error_x = 0.0
        self.integral_x = 0.0

        self.prev_error_y = 0.0
        self.integral_y = 0.0


    def compute(self, current_position):
        error_x = self.setpoint[0] - current_position[0]
        error_y = self.setpoint[1] - current_position[1]

        self.integral_x += error_x * self.dt
        self.integral_y += error_y * self.dt

        derivative_x = (error_x - self.prev_error_x) / self.dt
        derivative_y = (error_y - self.prev_error_y) / self.dt

        output_x = (self.kp * error_x) + (self.ki * self.integral_x) + (self.kd * derivative_x)
        output_y = (self.kp * error_y) + (self.ki * self.integral_y) + (self.kd * derivative_y)

        self.prev_error_x = error_x
        self.prev_error_y = error_y

        return output_x, output_y
