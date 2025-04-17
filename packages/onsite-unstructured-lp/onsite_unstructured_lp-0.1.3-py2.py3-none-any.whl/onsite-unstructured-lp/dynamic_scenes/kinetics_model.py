#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： Wentao Zheng
# datetime： 2024/3/4 21:13 
# ide： PyCharm
import os
import sys
import shlex
import platform
import subprocess
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

# 自定义库
from dynamic_scenes.socket_module import Client
from dynamic_scenes.observation import Observation

class KineticsModelStarter():
    def __init__(self, observation: Observation, python_port=25000, matlab_port=25001, ip_address='127.0.0.1'):
        initial_state = self._get_init_state_of_ego(observation)
        self.client = Client(Send_IP=ip_address, Send_Port=matlab_port, Receive_IP=ip_address, Receive_Port=python_port)
        self._write_temp_script(initial_state[0], initial_state[1], initial_state[2], initial_state[3], python_port, matlab_port, ip_address)
        self._check_completed()
        pass

    @property
    def get_client(self):
        return self.client

    def _get_init_state_of_ego(self, observation:Observation):
        x = observation.vehicle_info['ego']['x']
        y = observation.vehicle_info['ego']['y']
        yaw = observation.vehicle_info['ego']['yaw_rad']
        v0 = observation.vehicle_info['ego']['v_mps']
        return x,y,yaw,v0

    def _write_temp_script(self, x:float, y:float, yaw:float, v0:float, python_port:int, matlab_port:int, ip_address:str):
        current_path = Path(__file__).parent
        os_type = self._judge_platform()
        
        # 获取模板路径 
        template_path = current_path.parent / 'kinetic_model' / f'{os_type}' / 'control_simulink.m'
        
        # 为每个端口组合创建唯一的脚本文件名，避免多进程冲突
        port_str = f'{python_port}_{matlab_port}'
        script_filename = f'tempScript_{port_str}.m'
        control_script_filename = f'control_simulink_{port_str}.m'
        
        tempscript = current_path.parent / 'kinetic_model' / f'{os_type}' / script_filename
        control_script = current_path.parent / 'kinetic_model' / f'{os_type}' / control_script_filename
        
        if os.path.exists(tempscript):
            os.remove(tempscript)
        if os.path.exists(control_script):
            os.remove(control_script)

        # 创建端口特定的控制脚本
        if os.path.exists(template_path):
            try:
                print(f"创建唯一的MATLAB脚本: {control_script_filename}")
                with open(template_path, 'r', encoding='utf-8') as source_file:
                    control_script_content = source_file.read()
                    
                with open(control_script, 'w', encoding='utf-8') as target_file:
                    target_file.write(control_script_content)
            except Exception as e:
                print(f"读取模板文件失败: {e}")
                return None
        else:
            print(f"错误：找不到控制脚本模板: {template_path}")
            return None
        
        # 编写一个tempScript.m脚本用于存储初始化信息
        print(f"创建唯一的MATLAB脚本: {script_filename} (Python端口: {python_port}, MATLAB端口: {matlab_port})")
        with open(tempscript, 'w', encoding='utf-8') as f:
            f.write(f"currentDir = pwd;\n")
            f.write(f"cd ..\n")
            f.write(f"cd(currentDir);\n")
            f.write(f"x0={x};\n")
            f.write(f"y0={y};\n")
            f.write(f"yaw={yaw};\n")
            #f.write(f"head={yaw};\n")
            f.write(f"v0={v0};\n")
            f.write("acc=0.0;\n")  # 初始加速度
            f.write("gear=2;\n")  # 初始档位：1-前进档；2-驻车档；3-倒车档
            f.write("steer=0.0;\n")  # 初始前轮转角
            # f.write("slope=getGradient(x0, y0, head, grid, vx, vy);\n")  # 初始坡度值
            f.write("slope=-0.2;\n")
            f.write("load('a_brake.mat');\n")
            f.write("load('a_thr.mat');\n")
            f.write("load('brake.mat');\n")
            f.write("load('thr.mat');\n")
            f.write(f"localPort = {matlab_port};\n")  # MATLAB监听端口
            f.write(f"remotePort = {python_port};\n")  # Python端口
            f.write(f"remoteIP = '{ip_address}';\n")  # 控制端IP
            f.write("modelName='VehicleModel_SJTU';\n")
            # 使用端口特定的控制脚本，而不是共享的
            f.write(f"run('{control_script_filename}');\n")
            
        command = f"matlab -r \"run('{tempscript.as_posix()}')\""
        result = subprocess.Popen(shlex.split(command))
        
        return result

    def _check_completed(self):
        # Check whether the initialization is complete
        data, _ = self.client.client_receive_sock.recvfrom(1024)  # 假设信号很小，不需要大缓冲区
        if data.decode() == 'ready':
            print("MATLAB就绪，继续执行")

    def _judge_platform(self):
        os_type = platform.system()
        if os_type == "Windows":
            return 'win'
        elif os_type == "Linux" or os_type == "Darwin":
            return 'linux'
        else:
            print(f"不支持的操作系统: {os_type}")