import socket
import concurrent.futures
import requests

target_domain = input("请输入域名: ")  # 目标域名
output_file = "ok.txt"  # 保存成功结果的文件路径
invalid_file = "invalid.txt"  # 保存无法访问的子域名的文件路径

subdomains = []  # 存储待爆破的子域名

# 从用户输入或自定义文本中获取子域名列表
option = input("请输入爆破方式（1 - 用户输入，2 - 自定义文本）：")
if option == "1":
    subdomain_input = input("请输入子域名，多个子域名用空格分隔：")
    subdomains = subdomain_input.split()
elif option == "2":
    subdomain_file = input("请输入包含子域名字典文件：")
    with open(subdomain_file, "r") as file:
        subdomains = [line.strip() for line in file]

# 用户自定义线程数
num_threads = int(input("请输入线程数："))

def test_subdomain(subdomain):
    full_domain = f"{subdomain}.{target_domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        if ip != full_domain:
            response = requests.get(f"http://{full_domain}")
            if response.status_code == 200:
                with open(output_file, "a") as ok_file:
                    ok_file.write(f"{full_domain} ({ip})\n")
                print(f"发现子域名: {full_domain} (IP地址: {ip})")
            else:
                with open(invalid_file, "a") as invalid_file:
                    invalid_file.write(f"{full_domain}\n")
                print(f"无法访问的子域名: {full_domain}")
        else:
            with open(invalid_file, "a") as invalid_file:
                invalid_file.write(f"{full_domain}\n")
            print(f"无法解析子域名: {full_domain}")
    except socket.gaierror:
        with open(invalid_file, "a") as invalid_file:
            invalid_file.write(f"{full_domain}\n")
        print(f"无法解析子域名: {full_domain}")

# 使用多线程测试子域名
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    executor.map(test_subdomain, subdomains)

print("爆破完成！成功结果保存在ok.txt文件中，无法访问的子域名保存在invalid.txt文件中。")
