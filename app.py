import requests
from flask import Flask, Response
import sys  # 导入sys模块

app = Flask(__name__)

# 检查是否提供了足够的命令行参数
if len(sys.argv) < 3:
    print("用法: python app.py http[s]://nezha_url/api/v1/server/details nezha_TOKEN")
    sys.exit(1)  # 终止程序

# 从命令行参数获取URL和Token
JSON_URL = sys.argv[1]
API_TOKEN = sys.argv[2]

@app.route('/metrics')
def metrics():
    headers = {'Authorization': f'{API_TOKEN}'}  # 使用Token认证
    response = requests.get(JSON_URL, headers=headers)
    data = response.json()

    print(f'状态码: {response.status_code}')
    print(f'响应体: {data}')

    metrics_list = []

    if 'result' in data:
        for item in data['result']:
            metrics_list.append(f'host_cpu{{id="{item["id"]}", name="{item["name"]}"}} {item["status"]["CPU"]}')
            metrics_list.append(f'host_mem_used{{id="{item["id"]}", name="{item["name"]}"}} {item["status"]["MemUsed"]}')
            metrics_list.append(f'host_disk_used{{id="{item["id"]}", name="{item["name"]}"}} {item["status"]["DiskUsed"]}')
            metrics_list.append(f'host_net_in_speed{{id="{item["id"]}", name="{item["name"]}"}} {item["status"]["NetInSpeed"]}')
            metrics_list.append(f'host_net_out_speed{{id="{item["id"]}", name="{item["name"]}"}} {item["status"]["NetOutSpeed"]}')
    else:
        print("错误：未在JSON数据中找到'result'键")
        return Response("错误：未在JSON数据中找到'result'键", status=500)

    return Response('\n'.join(metrics_list), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9091)
