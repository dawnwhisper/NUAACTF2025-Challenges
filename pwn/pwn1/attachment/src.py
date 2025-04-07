import time
import socket
import select

flag = ""

def calculate_expression(expression):
    try:
        result = eval(expression)
        return result
    except ZeroDivisionError:
        return "错误: 除零错误"
    except SyntaxError:
        return "错误: 语法错误"
    except NameError:
        return "错误: 名称错误"
    except Exception as e:
        return f"错误: {str(e)}"

def banner():
    return "c10uds在小猿口算中取得了100分的好成绩，你也来试试吧！\n请输入一个表达式（或输入 'exit' 退出)\n"

def main():
    global flag
    with open("flag.txt", "r") as f:
        flag = f.read().strip()
    
    count = 0
    start_time = time.time()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(1)
    print("服务器已启动，等待连接...")

    while True:
        client_socket, client_address = server_socket.accept()
        # print(f"连接来自: {client_address}")
        client_socket.sendall(banner().encode())

        last_interaction_time = time.time()

        while True:
            try:
                # 使用 select 模块设置超时时间
                ready_to_read, _, _ = select.select([client_socket], [], [], 60)
                if not ready_to_read:
                    print("连接超时，关闭连接")
                    break

                # 接收数据
                data = client_socket.recv(1024).decode().strip()
                if not data or data.lower() == 'exit':
                    break
                
                # 计算并发送结果
                result = calculate_expression(data)
                client_socket.sendall(f">>> {result}\n".encode())
                
                # 增加计数器
                count += 1
                
                # 检查时间和计数器
                current_time = time.time()
                if current_time - start_time <= 1:
                    if count >= 100:
                        client_socket.sendall(f"Flag: {flag}\n".encode())
                        break
                else:
                    # 重置计数器和时间
                    count = 0
                    start_time = current_time

                # 更新最后交互时间
                last_interaction_time = current_time
                    
            except KeyboardInterrupt:
                print("\n服务器中断")
                break
            except Exception as e:
                print(f"发生错误: {e}")
                break

        client_socket.close()
        print(f"连接关闭: {client_address}")

if __name__ == "__main__":
    main()