#include <Arduino.h>
#include "PinMap.h"

int dir[3][4]={{1,1,1,1},{-1,1,-1,1},{-1,-1,1,1}};
int vxg, vyg;
int direction[4]={1,1,1,1};
int pwm[4]={100,100,100,100};
int mot_vel[4];
int vx,vy,vw;

// put function declarations here:

void rotation(time_t time){
  float theta = vw*time/100;
  float vxg = vx*cos(theta) - vy*sin(theta);
  float vyg = vx*sin(theta) + vy*cos(theta);
  vx = vxg;
  vy = vyg;
}

void multiplication(int vx,int vy,int vw)
{
  mot_vel[0]=vx*dir[0][0]+vy*dir[1][0]+vw*dir[2][0];
  mot_vel[1]=vx*dir[0][1]+vy*dir[1][1]+vw*dir[2][1];
  mot_vel[2]=vx*dir[0][2]+vy*dir[1][2]+vw*dir[2][2];
  mot_vel[3]=vx*dir[0][3]+vy*dir[1][3]+vw*dir[2][3];
}

void direction_pwm()
{
  for (int i =0;i<4;i++)
  {
    if (mot_vel[i] >0) 
    {direction[i] = 0;}
    pwm[i] = map(abs(mot_vel[i]),0,10,0,100);
  }
}

/*
void setup() {
  // put your setup code here, to run once:
  pinMode(MD1_DIR,OUTPUT);
  pinMode(MD2_DIR,OUTPUT);
  pinMode(MD3_DIR,OUTPUT);
  pinMode(MD4_DIR,OUTPUT);
  pinMode(MD1_PWM,OUTPUT);
  pinMode(MD2_PWM,OUTPUT);
  pinMode(MD3_PWM,OUTPUT);
  pinMode(MD4_PWM,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  time_t time = millis();
  //rotation(time);
  multiplication(vx,vy,vw);
  direction_pwm();
  digitalWrite(MD1_DIR,direction[0]);
  digitalWrite(MD2_DIR,direction[1]);
  digitalWrite(MD3_DIR,direction[2]);
  digitalWrite(MD4_DIR,direction[3]);
  analogWrite(MD1_PWM,pwm[0]);
  analogWrite(MD2_PWM,pwm[1]);
  analogWrite(MD3_PWM,pwm[2]);
  analogWrite(MD4_PWM,pwm[3]);
}
*/