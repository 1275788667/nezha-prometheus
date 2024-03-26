import requests
from flask import Flask, Response
import sys

app = Flask(__name__)

if len(sys.argv) < 3:
    print("用法: python app.py http[s]://nezha_url/api/v1/server/details nezha_TOKEN")
    sys.exit(1)

JSON_URL = sys.argv[1]
API_TOKEN = sys.argv[2]

@app.route('/metrics')
def metrics():
    headers = {'Authorization': f'{API_TOKEN}'}
    response = requests.get(JSON_URL, headers=headers)
    data = response.json()

    if 'result' not in data:
        print("错误：未在JSON数据中找到'result'键")
        return Response("错误：未在JSON数据中找到'result'键", status=500)

    metrics_list = []

    for item in data['result']:
        id_ = item.get("id", "")
        name = item.get("name", "").replace('"', '')
        tag = item.get("tag", "")
        last_active = item.get("last_active", 0)
        ipv4 = item.get("ipv4", "")
        ipv6 = item.get("ipv6", "")
        valid_ip = item.get("valid_ip", "")

        # 添加服务器的元数据指标
        metrics_list.extend([
            f'nezha_tag{{id="{id_}", name="{name}"}} {tag}',
            f'nezha_last_active{{id="{id_}", name="{name}"}} {last_active}',
            f'nezha_ipv4{{id="{id_}", name="{name}"}} {ipv4}',
            f'nezha_ipv6{{id="{id_}", name="{name}"}} {ipv6}',
            f'nezha_valid_ip{{id="{id_}", name="{name}"}} {valid_ip}'
        ])

        # Host信息
        host_info = item.get('host', {})
        for key, value in host_info.items():
            if isinstance(value, list):  # 假设CPU是列表类型
                value = ' '.join(value)
            metric_name = f'nezha_host_{key.lower()}{{id="{id_}", name="{name}"}}'
            metrics_list.append(f'{metric_name} {value}')

        # Status信息
        status = item.get("status", {})
        for key, value in status.items():
            metric_name = f'nezha_status_{key.lower()}{{id="{id_}", name="{name}"}}'
            metrics_list.append(f'{metric_name} {value}')

    return Response('\n'.join(metrics_list), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9091)
