# encoding=utf-8
# Author：Wentao Zheng
# E-mail: swjtu_zwt@163.com
# developed time: 2024/2/8 12:17
import os
import socket
import struct  # 解析simulink模型打包来的数据要用
import time
import platform
import subprocess
from pathlib import Path

class Client():
    def __init__(self, Send_IP='127.0.0.1', Send_Port=25001, Receive_IP='127.0.0.1', Receive_Port=25000):
        self.send_ip = Send_IP
        self.send_port = Send_Port
        self.receive_ip = Receive_IP
        self.receive_port = Receive_Port
        self._build_client()

    def _build_client(self):
        # 发送端
        self.client_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 接收端
        self.client_receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # 检查接收端口是否被占用
        try:
            # 尝试使用指定端口创建一个临时socket
            temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_sock.settimeout(0.1)  # 设置超时时间为短暂的0.1秒
            temp_sock.bind((self.receive_ip, self.receive_port))
            temp_sock.close()
            print(f"Python端口检查: {self.receive_ip}:{self.receive_port} 未被占用，可以使用")
        except socket.error as e:
            print(f"Python端口检查警告: {self.receive_ip}:{self.receive_port} 可能已被占用: {e}")
            
        # 绑定接收socket
        try:
            self.client_receive_sock.bind((self.receive_ip, self.receive_port))
            print(f"成功绑定Python接收socket到 {self.receive_ip}:{self.receive_port}")
        except socket.error as e:
            print(f"绑定Python接收socket失败: {self.receive_ip}:{self.receive_port}, 错误: {e}")
            raise  # 重新抛出异常，让上层知道出了问题
            
        print(f"UDP通信设置完成:")
        print(f"  - Python接收: {self.receive_ip}:{self.receive_port}")
        print(f"  - MATLAB接收: {self.send_ip}:{self.send_port}")

    def send_message(self, gear, acceleration, steering_angle, continue_simulation, slope=0):
        try:
            message = struct.pack('>ddddd', gear, acceleration, steering_angle, continue_simulation, slope)
            self.client_send_sock.sendto(message, (self.send_ip, self.send_port))
            if continue_simulation == 1:
                print('进入下一控制量计算过程...')
            else:
                print('控制量已发送，等到接收下一个状态量...')
        except Exception as e:
            print(f"通信出现问题！，具体原因为{e}")

    def receive_message(self):
        """接收状态数据，持续接收直到接收到结束标志"""
        received_data = []
        chunk_size = 16  # 每次接收 16 个 double 类型数据
        buffer_size = chunk_size*8  # 设置缓冲区大小
        end_flag = [-10, -10, -10, -10]  # 结束标志是 4 个 -10

        while True:
            try:
                # 接收数据
                data, addr = self.client_receive_sock.recvfrom(buffer_size)
                if not data:  # 如果没有数据可读
                    print("没有接收到数据，退出循环")
                    break

                # 解析数据长度
                num_doubles = len(data) // 8
                #print("接收到数量：",num_doubles)

                if num_doubles % 4 != 0:
                    print(f"无效数据长度: {num_doubles} doubles")
                    return None, None

                # 解包原始数据
                fmt = f'>{num_doubles}d'
                raw = struct.unpack(fmt, data)

                # 检查是否接收到结束标志
                if list(raw[-4:]) == end_flag:  # 检查最后 4 个元素是否为结束标志
                    #print("接收到结束标志，停止接收数据")
                    received_data.extend(raw[:-4])  # 排除结束标志
                    print('状态量已接收，等待计算下一个控制量...')
                    break
                else:
                    received_data.extend(raw)  # 累积接收到的数据

            except socket.error as e:
                print(f"网络错误: {e}")
                break
            except struct.error as e:
                print(f"解包错误: {e}")
                break
            except Exception as e:
                print(f"接收错误: {e}")
                break

        # 计算接收到的状态数量
        #print("receive长度",len(received_data))
        step = len(received_data) // 4

        return received_data, step


    def send_and_receive(self, gear, acceleration, steering_angle,slope):
        try:
            message = struct.pack('>dddd', gear, acceleration, steering_angle,slope)
            print("steer", steering_angle)
            self.client_send_sock.sendto(message, (self.send_ip, self.send_port))
            t1=time.time()
            print('控制量已发送，等到接收下一个状态量...')

            data, addr = self.client_receive_sock.recvfrom(1024)
            print('状态量已接收，等待计算下一个控制量...')
            t2=time.time()
            print(f"接收到数据包，耗时{t2-t1}秒")
            if data:
                unpacked_data = struct.unpack('>dddd', data)
                return unpacked_data
        except Exception as e:
            print(f"通信出现问题！，具体原因为{e}")

    def close_sockets(self):
        self.client_send_sock.close()
        self.client_receive_sock.close()
        
        # 清理可能存在的临时脚本文件
        try:
            self._cleanup_temp_scripts()
        except Exception as e:
            print(f"清理临时文件时出错: {e}")
    
    def _cleanup_temp_scripts(self):
        """清理相关的临时脚本文件"""
        import os
        import glob
        
        # 获取当前文件所在目录
        current_path = Path(__file__).parent
        
        # 获取操作系统类型并确定临时文件目录
        os_type = self._get_platform_type()
        temp_dir = current_path.parent / 'kinetic_model' / os_type
        
        # 如果目录不存在，说明还没有创建过临时文件
        if not temp_dir.exists():
            print(f"临时脚本目录 {temp_dir} 不存在，无需清理")
            return
        
        port_str = f"{self.receive_port}_{self.send_port}"
        found_files = False
        
        # 查找并清理所有tempScript_*文件
        pattern = os.path.join(temp_dir, f"tempScript_{port_str}.m")
        for script_file in glob.glob(pattern):
            found_files = True
            try:
                os.remove(script_file)
                print(f"已清理临时脚本文件: {script_file}")
            except Exception as e:
                print(f"删除临时文件 {script_file} 失败: {e}")
        
        # 查找并清理所有control_simulink_*文件
        pattern_control = os.path.join(temp_dir, f"control_simulink_{port_str}.m")
        for script_file in glob.glob(pattern_control):
            found_files = True
            try:
                os.remove(script_file)
                print(f"已清理控制脚本文件: {script_file}")
            except Exception as e:
                print(f"删除控制脚本文件 {script_file} 失败: {e}")
        
        if not found_files:
            print(f"未找到与当前进程相关的脚本文件 (端口组合: {port_str})")
            
        # 可选: 如果目录为空，删除整个目录
        # 但在多进程环境下可能会有冲突，所以这里不实现

    def _get_platform_type(self):
        """获取当前操作系统类型"""
        import platform
        os_type = platform.system()
        if os_type == "Windows":
            return 'win'
        elif os_type == "Linux" or os_type == "Darwin":
            return 'linux'
        else:
            return 'win'  # 默认返回win
            
    def send_terminate_signal(self, send_ip=None, send_port=None):
        """向MATLAB发送终止信号，使MATLAB自行退出
        
        Args:
            send_ip: 可选，指定发送IP地址。如果为None则使用实例的默认IP
            send_port: 可选，指定发送端口。如果为None则使用实例的默认端口
        """
        try:
            # 使用传入的IP和端口，如果没有则使用默认值
            target_ip = send_ip if send_ip is not None else self.send_ip
            target_port = send_port if send_port is not None else self.send_port
            
            # 发送包含终止标志(-999)的消息
            # 前5个值为正常控制量，第6个值为终止标志
            message = struct.pack('>dddddd', 2, 0.0, 0.0, 0, 0.0, -999.0)
            self.client_send_sock.sendto(message, (target_ip, target_port))
            print(f'已发送终止信号给MATLAB进程({target_ip}:{target_port})，MATLAB将自行退出')
            # 等待一小段时间，确保信号被接收
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"发送终止信号时出错: {e}")
            return False





