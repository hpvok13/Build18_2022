import RPi.GPIO as GPIO
import time
from threading import Thread


cur_pos = 0

in1 = 24
in2 = 23
en1 = 25
temp1=1

in3 = 5
in4 = 6
en2 = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en1,1000)
p.start(75)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2=GPIO.PWM(en2,1000)
p2.start(75)

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")

class MotorController:
    def __init__(self, init_target=100, eps=1):
        self.target_pos = init_target
        self.cur_pos = 0
        self.eps = eps
        self.vel = 100.0/20.0

    def start(self):
        Thread(target=self._start, args=()).start()
        return self

    def _start(self):
        vel = 0
        while not self.stopped:
            t = time.time()
            while abs(self.cur_pos - self.target_pos) > self.eps:
                if self.cur_pos < self.target_pos:
                    vel = self.vel
                    GPIO.output(in1,GPIO.HIGH)
                    GPIO.output(in2,GPIO.LOW)
                else:
                    vel = -self.vel
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.HIGH)

                time.sleep(0.01)
                self.cur_pos += (time.time() - t) * vel
                t = time.time()

            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)

    def stop(self):
        self.stopped = True

    def set(self, target_pos):
        self.target_pos = target_pos

# def set_pos(x):
#     if(x > cur_pos):
#         time_t = 20.0 * (x - cur_pos) / 100.0
#         start_time = time.time()
#         cur_time = start_time
#         while(cur_time - start_time < time_t):
#             GPIO.output(in1,GPIO.HIGH)
#             GPIO.output(in2,GPIO.LOW)
#             cur_time = time.time()

#         GPIO.output(in1,GPIO.LOW)
#         GPIO.output(in2,GPIO.LOW)
#         cur_pos = x

#     if(x < cur_pos):
#         time_t = 20.0 * (cur_pos - x) / 100.0
#         start_time = time.time()
#         cur_time = start_time
#         while(cur_time - start_time < time_t):
#             GPIO.output(in1,GPIO.LOW)
#             GPIO.output(in2,GPIO.HIGH)
#             cur_time = time.time()

#         GPIO.output(in1,GPIO.LOW)
#         GPIO.output(in2,GPIO.LOW)
#         cur_pos = x


# while(1):

#     x = input()
#     x = int(x)

#     set_pos(x)
    
    
    """ if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         
         GPIO.output(in3,GPIO.HIGH)
         GPIO.output(in4,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)

         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)

        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)

        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        p2.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        p2.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        p2.ChangeDutyCycle(75)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")"""
