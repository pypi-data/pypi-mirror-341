%% 清理资源（每次仿真前运行）
% fclose(u);
% delete(u);
% clear u;

%% 启动仿真
% clear,clc,close all;

% 加载初始状态（根据需要调整）
% run("init.m"); 
% init(x, y, yaw, v0, acc);

%% UDP参数设置
% localPort和remotePort以及remoteIP由tempScript.m传入
% 如果未定义，使用默认值
if ~exist('localPort', 'var')
    localPort = 25001;        % MATLAB监听端口（默认值）
end
if ~exist('remotePort', 'var')
    remotePort = 25000;       % 控制端端口（默认值）
end
if ~exist('remoteIP', 'var')
    remoteIP = '127.0.0.1';   % 控制端IP（默认值）
end
chunkSize = 16;            % 每次发送的 double 数据数量

%% 端口检测
disp(['MATLAB将尝试使用以下通信参数:']);
disp(['  - 本地端口: ', num2str(localPort)]);
disp(['  - 远程端口: ', num2str(remotePort)]);
disp(['  - 远程IP: ', remoteIP]);

% 检查MATLAB端口是否可用
try
    % 使用try-catch块创建UDP对象并检查端口可用性
    disp(['正在检查本地端口 ', num2str(localPort), ' 是否可用...']);
    temp_u = udp(remoteIP, 'LocalPort', localPort, 'RemotePort', remotePort);
    try
        fopen(temp_u);
        disp(['端口检查成功: 本地端口 ', num2str(localPort), ' 可用']);
        fclose(temp_u);
        delete(temp_u);
        clear temp_u;
    catch ME
        disp(['端口检查失败: 本地端口 ', num2str(localPort), ' 可能已被占用!']);
        disp(['错误信息: ', ME.message]);
        disp('提示: 请尝试使用不同的端口号或关闭占用此端口的程序');
        error('无法使用指定的本地端口，请检查端口占用情况或更换端口号');
    end
catch
    disp('创建临时UDP对象失败，请检查网络设置');
    rethrow(lasterror);
end

%% 创建UDP对象
try
    disp(['正在创建UDP对象...']);
    u = udp(remoteIP, 'LocalPort', localPort, 'RemotePort', remotePort);
    disp(['UDP对象创建成功']);
catch ME
    disp(['创建UDP对象失败: ', ME.message]);
    rethrow(lasterror);
end

try
    disp(['正在打开UDP通信...']);
    fopen(u);
    disp(['UDP通信打开成功']);
catch ME
    disp(['打开UDP通信失败: ', ME.message]);
    if strcmp(ME.identifier, 'MATLAB:icinterface:fopen:connectionRefused')
        disp('原因: 连接被拒绝，请检查远程IP和端口是否正确');
    elseif strcmp(ME.identifier, 'MATLAB:icinterface:fopen:addressInUse')
        disp('原因: 地址已被使用，该端口可能已被其他程序占用');
        disp('提示: 请尝试使用不同的端口号或关闭占用此端口的程序');
    else
        disp(['原因: ', ME.message]);
    end
    disp('错误详情:');
    disp(getReport(ME));
    error('UDP通信打开失败，请检查端口和IP设置');
end

modelName = 'VehicleModel_SJTU';  % 模型名称
load_system(modelName);
set_param(modelName, 'StopTime', '150');

%% 初始化变量
state_history = [];       % 存储当前控制周期内的状态
if_first = true;          % 首次运行标志

%% 发送就绪信号
readyMessage = 'ready';
fwrite(u, readyMessage, 'char');
disp("开始接收消息");
disp(['使用以下通信参数: localPort=', num2str(localPort), ', remotePort=', num2str(remotePort), ', remoteIP=', remoteIP]);

try
    while true
        %% 检查UDP消息
        if u.BytesAvailable > 0
            % 读取控制量
            data = fread(u, u.BytesAvailable, 'double');
            
            % 检查是否接收到终止信号
            if length(data) >= 6 && data(6) == -999.0
                disp('接收到Python进程发送的终止信号，MATLAB进程即将退出...');
                % 先确保模型停止运行
                try
                    % 使用stop_system停止模型
                    set_param(modelName, 'SimulationCommand', 'stop');
                    disp(['已自动停止模型 ', modelName]);
                    % 等待模型完全停止
                    while ~strcmp(get_param(modelName,'SimulationStatus'), 'stopped')
                        pause(0.1);
                    end
                catch ME
                    disp(['停止模型时出错: ', ME.message]);
                end
                break;  % 立即退出循环
            end
            
            gear = data(1);
            acc = data(2);
            steer = data(3);
            continue_simulation = data(4);
            slope = data(5);
            
            disp("接收到消息");
            disp(acc)
            disp(steer)
            
            % 更新模型参数
            set_param(modelName, 'SimulationCommand', 'update'); % 更新模型
            
            % 处理历史数据
            send_data = state_history; 

            % 获取新状态
            if continue_simulation==0  
                if if_first
                    set_param(modelName, 'SimulationCommand', 'start');
                    if_first = false;
                else
                    set_param(modelName, 'SimulationCommand', 'step');
                end
            
                % 等待仿真暂停
                while ~strcmp(get_param(modelName,'SimulationStatus'),'paused')
                    pause(0.01);
                end

                current_x = out.x.Data(end);
                current_y = out.y.Data(end);
                current_v = out.velocity.Data(end);
                current_head = out.phi.Data(end);
                new_state = [current_v,current_head,current_x, current_y];
                %slope=getGradient(current_x, current_y, current_head, grid, vx, vy);
                % slope = -0.2;
                send_data = [send_data; new_state];  % 追加新状态
                send_data = reshape(send_data', [], 1);
                numChunks = ceil(numel(send_data) / chunkSize);
            
                % 分块发送组合数据，防止超出缓冲区
                for i = 1:numChunks
                    startIdx = (i - 1) * chunkSize + 1;
                    endIdx = min(i * chunkSize, numel(send_data));
                    chunk = send_data(startIdx:endIdx);
                    fwrite(u, chunk, 'double');
                    pause(0.01);  % 稍作延迟，避免发送过快
                end
                
                % 发送结束标志
                endMessage = [-10, -10, -10, -10];  % 假设结束标志是 4 个 -10
                fwrite(u, endMessage, 'double');
                state_history = [];  % 初始化新周期记录

            else
                %% 继续步进采集后续状态
                while u.BytesAvailable == 0
                    % 执行步进
                    set_param(modelName,'SimulationCommand','update');
                    set_param(modelName, 'SimulationCommand', 'step');
               
                    % 等待仿真暂停
                    while ~strcmp(get_param(modelName,'SimulationStatus'),'paused')
                        pause(0.01);
                    end
                    
                    % 记录状态
                    current_x = out.x.Data(end);
                    current_y = out.y.Data(end);
                    current_v = out.velocity.Data(end);
                    current_head = out.phi.Data(end);
                    %slope=getGradient(current_x, current_y, current_head, grid, vx, vy);
                    % slope = -0.2;
                    state_history = [state_history; 
                                   current_v,current_head,current_x, current_y];
                    % disp("运行但不发送")
                    if u.BytesAvailable > 0
                        break;
                    end
                end
            end
            
        else
            pause(0.1);  % 降低CPU占用
        end
    end
catch ME
    fprintf('运行异常: %s\n', ME.message);  % 打印错误信息
    fprintf('堆栈信息:\n');
    for i = 1:length(ME.stack)
        stackItem = ME.stack(i);
        fprintf('  文件: %s\n', stackItem.file);
        fprintf('  函数: %s\n', stackItem.name);
        fprintf('  行号: %d\n', stackItem.line);
        fprintf('  -----------------------------\n');
    end
end

%% 清理资源
fclose(u);
delete(u);
clear u;

%% 退出MATLAB
disp('MATLAB进程即将退出...');
pause(1);  % 给一点时间让消息显示

exit;