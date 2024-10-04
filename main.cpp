#include <Arduino.h>
#include "PinMap.h"
#include "functions.h"
#include <micro_ros_platformio.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <geometry_msgs/msg/twist.h>


void setup() {
  // put your setup code here, to run once:
  set_microros_serial_transports(Serial);
  allocator = rcl_get_default_allocator();
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));
  RCCHECK(rclc_node_init_default(&node, "microros", "", &support));
  const char *cmdvel_name = "/cmd_vel";
  const rosidl_message_type_support_t *Twist_type =
  ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist);
  RCCHECK(rclc_subscription_init_default(
      &cmdvel_subscriber, &node,
      Twist_type, cmdvel_name));
  RCCHECK(rclc_executor_init(&executor, &support.context, 4, &allocator));
  RCCHECK(rclc_executor_add_subscription(&executor, &cmdvel_subscriber, &msg_cmdvel, &cmdvel_callback, ON_NEW_DATA));
void cmdvel_callback(const void *msgin)
{
  // subscribes from cmd_vel topic and feeds it to motors
  target_vx = (float) msg_cmdvel.linear.x;
  target_vy = (float) msg_cmdvel.linear.y;
  target_vw = (float) msg_cmdvel.angular.z;
}

  pinMode(MD1_DIR,OUTPUT);
  pinMode(MD2_DIR,OUTPUT);
  pinMode(MD3_DIR,OUTPUT);
  pinMode(MD4_DIR,OUTPUT);
  pinMode(MD1_PWM,OUTPUT);
  pinMode(MD2_PWM,OUTPUT);
  pinMode(MD3_PWM,OUTPUT);
  pinMode(MD4_PWM,OUTPUT);


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