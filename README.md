# nezha-prometheus
适用于哪吒面板json api转为Prometheus格式方便接入到数据源

# Docker构建使用
docker build -t nezha-prometheus-exporter .
docker run -d -p 9091:9091 --name=nezha-prometheus -e NEZHA_URL=http[s]://nezha_url/api/v1/server/details -e NEZHA_TOKEN=nezha_TOKEN nezha-prometheus-exporter

# 在线拉取
docker run -d -p 9091:9091 --name=nezha-prometheus -e NEZHA_URL=http[s]://nezha_url/api/v1/server/details -e NEZHA_TOKEN=nezha_TOKEN  1275788667/nezha-prometheus-exporter:latest
