#include <Servo.h>
#define  screenmax   640   //屏幕宽度
#define  servocenter   90  // 舵机初始位置
#define  servopin   9   // 舵机PWM接口
#define  baudrate 9600  
#define distance 1  // 每次移动距离
int pos = 0;
char var=0;
Servo servo;
void setup() {
  Serial.begin(baudrate);       //链接舵机
  pinMode(servopin,OUTPUT);    //舵机接口初始化
  servo.attach(servopin); 
  servo.write(servocenter); //初始化舵机位置
  delay(200);
}

void loop () {
  while(Serial.available() <=0); // 等待信号
    var=Serial.read();//从串口读操作
    pos = servo.read();//舵机位置获取
    //舵机位置控制
    if(var=='0'){pos++;}
    if(var=='1'){pos--;}
    servo.write(pos);
    }   
