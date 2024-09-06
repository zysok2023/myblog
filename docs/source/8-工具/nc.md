# nc命令
## 简介
全称netcat，用于TCP、UDP或unix域套接字(uds)的数据流操作，它可以打开TCP连接，发送UDP数据包，监听任意TCP 和UDP端口，同时也可用作做端口扫描，支持IPv4和IPv6，与Telnet的不同在于nc可以编写脚本。
## 文件传输
接收方提前设置监听端口与要接收的文件名（文件名可自定义）：
nc -lp 8888 > node.tar.gz
传输方发文件
nc -nv 192.168.75.121 8888  < node_exporter-1.3.1.linux-amd64.tar.gz
注意：192.168.75.121是接收方的ip地址
## TCP端口扫描
nc -zv -w2 ip port-port






