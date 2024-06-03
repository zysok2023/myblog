# 1.WGET工具
wget是一个下载网页文件的免费工具。它将互联网上的数据保存到一个文件或展示在终端上。它支持通过 FTP、SFTP、HTTP 和 HTTPS 下载。
wget Options
| Option                            | Description                                                                                                                                                     |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -b, --background                  | Goes to background immediately after startup.                                                                                                                   |
| -q, --quiet                       | Runs wget in quiet mode, suppressing output except for errors and essential messages.                                                                           |
| -d, --debug                       | Turns on debug output.                                                                                                                                          |
| -O, --output-document=[file]      | Specifies the output file name.                                                                                                                                 |
| -e [command], --execute [command] | Executes a command after the download completes. This is useful for performing additional actions, such as running a script.                                    |
| -v, --verbose                     | Turns on verbose output with all the available data. The default output is verbose.                                                                             |
| -nv, --no-verbose                 | Turns on verbose output with all the available data. The default output is verbose.                                                                             |
| -c, --continue                    | Resumes downloading a partially downloaded file.                                                                                                                |
| -r, --recursive                   | Enables recursive downloading.                                                                                                                                  |
| -P, --directory-prefix=[prefix]   | Specifies the directory where downloaded files are to be saved.                                                                                                 |
| -l, --level=[depth]               | Limits the recursion depth when downloading recursively.                                                                                                        |
| --limit-rate=[rate]               | Limits the download rate to the specified value.                                                                                                                |
| -R, --reject=[list]               | Specifies a comma-separated list of file extensions to reject during recursive downloads.                                                                       |
| -A, --accept=[list]               | Specifies a comma-separated list of file extensions to accept during recursive downloads.                                                                       |
| -i, --input-file                  | Specifies a file containing a list of URLs wget downloads.                                                                                                      |
| -m, --mirror                      | Downloads all of the website's content recursively, including directories, subdirectories, and linked pages, while preserving the original directory structure. |
| --tries=[number_of_tries]         | Sets the maximum number of retries for failed downloads when using wget.                                                                                        |
| --no-check-certificate            | Disables SSL certificate verification when making HTTPS connections.                                                                                            |
| U, --user-agent="user-agent-here" | Allows users to specify a custom user agent string for HTTP requests.                                                                                           |
## 1.1 使用 Wget 命令下载单个文件
最基本的 wget 命令示例之一是下载单个文件并将其存储在当前工作目录中。例如，您可以使用以下方法获取最新版本的 WordPress：
```
wget https://wordpress.org/latest.zip
```
在此示例中，将下载名为 latest.zip 的文件到当前工作目录中。您还将看到其他信息，例如下载进度、速度、大小、时间和日期。
## 1.2 使用 wget 命令下载多个文件
可以将 wget 的使用更进一步，一次下载多个文件。为此，我们需要创建一个文本文档并将下载 URL 放在那里。在此示例中，我们将使用 wget 检索最新版本的 WordPress、Joomla 和 Drupal。输入以下内容
```
nano example.txt
https://wordpress.org/latest.zip
https://downloads.joomla.org/cms/joomla3/3-8-5/Joomla_3-8-5-Stable-Full_Package.zip
https://ftp.drupal.org/files/projects/drupal-8.4.5.zip
wget -i example.txt

```
## 1.3 使用 wget 命令获取不同名称的文件
在这个 wget 示例中，我们将借助 -O 选项使用不同的名称保存文件：
```
wget -O wordpress-install.zip https://wordpress.org/latest.zip
```
## 1.4 使用 wget 命令将文件保存在指定目录中
可以使用 -P 函数利用 wget 将文件放置在另一个目录中
```
wget -P documents/archives/ https://wordpress.org/latest.zip
```
## 1.5 使用 Wget 命令限制下载速度
使用 wget，您还可以限制下载速度。这在检索大文件时很有用，可以防止它使用所有带宽。此 wget 示例将限制设置为 500k：
```
wget --limit-rate=500k https://wordpress.org/latest.zip
```
## 1.6 使用 Wget 命令设置重试次数
Internet 连接问题可能会导致下载中断。为了解决这个问题，我们可以使用 -tries 函数增加重试次数：
```
wget -tries=100 https://wordpress.org/latest.zip
```
## 1.7 使用 Wget 命令在后台下载
对于非常大的文件，您可以利用 -b 函数。它将在后台下载您的内容。
```
wget -b http://example.com/beefy-file.tar.gz
```
wget-log 将出现在您的工作目录中，可用于检查您的下载进度和状态。您还可以使用 tail 命令：
```
tail -f wget-log
```
## 1.8 使用Wget命令通过FTP下载
使用wget命令下载ftp服务器上的文件和文件夹
```
wget ftp://ip:port/file --ftp-user=name --ftp-password=password -r
wget ftp://name:password@ip:port/file -r --no-passive-ftp
# 参数说明
ip:服务器ip
port:服务器端口
file ：服务器上的文件名
name：ftp用户
password：ftp用户密码
-r:递归下载
--no-passive-ftp:关闭ftp被动模式
```
## 1.9 使用 Wget 命令检索整个网站
也可以使用 wget 命令下载整个站点的内容。这将允许您在没有互联网连接的情况下在本地查看它。下面是一个示例：
```
wget --mirror --convert-links --page-requisites --no-parent -P documents/websites/ https://some-website.com
```
## 1.10 使用 Wget 命令查找断开的链接
我们可以使用 wget 命令来查找在特定网站上显示 404 错误的所有损坏的 URL。首先执行以下操作：
```
wget -o wget-log -r -l 5 --spider http://example.com
# 参数
-o 将输出收集到文件中供以后使用。
-l 指定递归级别。
-r 使下载递归。
--spider 将 wget 设置为蜘蛛模式
```
现在可以调查 wget-log 文件以查找断开链接的列表。下面是执行此操作的命令：
```
grep -B 2 '404' wget-log | grep "http" | cut -d " " -f 4 | sort -u
```
## 1.11 使用 Wget 命令断点续传
当文件特别大或者网络特别慢的时候，往往一个文件还没有下载完，连接就已经被切断，此时就需要断点续传。wget的断点续传是自动的，只需要使用-c参数。
```
 wget -c http://the.url.of/incomplete/file
```
## 1.12 选择性的下载
可以指定让wget只下载一类文件，或者不下载什么文件。例如：
```
 wget -m –reject=gif http://target.web.site/subdirectory
```
 表示下载http://target.web.site/subdirectory，但是忽略gif文件。–accept=LIST 可以接受的文件类型，–reject=LIST拒绝接受的文件类型。
# 2.CRUL工具
curl （“客户端 URL”的缩写）是一个命令行工具，支持通过各种网络协议传输数据。它通过指定相关的 URL 和需要发送或接收的数据来与 Web 或应用程序服务器进行通信。

curl还支持SSL认证、HTTP POST、HTTP PUT、FTP上传, HTTP form based upload、proxies、HTTP/2、cookies、用户名+密码认证(Basic, Plain, Digest, CRAM-MD5, NTLM, Negotiate and Kerberos)、file transfer resume、proxy tunneling。
## 2.1 curl 协议

cURL支持的通信协议有FTP、FTPS、HTTP、HTTPS、TFTP、SFTP、Gopher、SCP、Telnet、DICT、FILE、LDAP、LDAPS、IMAP、POP3、SMTP和RTSP。
| Protocol            | Description                                                                                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------------- |
| DICT                | 一种字典网络协议，用于向字典服务器查询单词的含义                                                              |
| FILE                | 使用 curl 从本地文件系统获取文件的 URL 方案。                                                                 |
| FTP, FTPS FTP、FTPS | 文件传输协议，用于客户端和服务器之间的文件传输。FTPS 是添加了 SSL/TLS 安全层的相同协议的版本                  |
| GOPHER, GOPHERS     | 超文本传输协议，用于网络和互联网数据传输。HTTPS 是添加了 SSL/TLS 安全层的相同协议的版本                       |
| TTP, HTTPS          | 超文本传输协议，用于网络和互联网数据传输。HTTPS 是添加了 SSL/TLS 安全层的相同协议的版本。                     |
| IMAP、IMAPS         | internet 消息访问协议，用于电子邮件访问和管理。IMAPS 是添加了 SSL/TLS 安全层的相同协议的版本                  |
| LDAP、LDAPS         | 轻量级目录访问协议，用于分布式目录信息访问和管理。LDAPS 是添加了 SSL/TLS 安全层的相同协议的版本。             |
| MQTT                | 消息队列遥测传输 - 用于在小型设备（通常是 IoT 系统）之间交换数据的协议。                                      |
| POP3, POP3S         | 邮局协议版本 3 - 从服务器检索电子邮件的协议。POP3S 是添加了 SSL/TLS 安全层的相同协议的版本。                  |
| RTMP                | 实时消息传递协议 - 音频、视频和其他数据的流协议                                                               |
| RTSP                | 实时流协议，用于流媒体服务器管理。                                                                            |
| SCP                 | SSH 文件传输协议 - 使用 SSH 连接的文件传输协议版本                                                            |
| SFTP                | SSH 文件传输协议 - 使用 SSH 连接的文件传输协议版本。                                                          |
| SMB, SMBS           | 服务器消息块 - 用于管理对文件和计算机外围设备的共享访问的协议。SMBS 是添加了 SSL/TLS 安全层的相同协议的版本。 |
| SMTP, SMPTS         | 简单邮件传输协议 - 一种电子邮件协议，用于轻松传输电子邮件。SMTPS 是添加了 SSL/TLS 安全层的相同协议的版本。    |
| TELNET              | 用于面向文本的双向交互式通信的应用层协议。                                                                    |
| TFTP                | 简单文件传输协议，用于将文件上传或下载到远程主机或从远程主机下载文件。                                        |

## 2.2 curl 命令选项
参考[curl使用手册](https://curl.se/docs/tutorial.html)
curl 接受多种选项，这使其成为一个非常通用的命令。选项以一个或两个破折号开头。如果它们不需要其他值，则可以将单破折号选项写入在一起.
![curl命令](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/curl命令.png)
```
-A/--user-agent <string>              设置用户代理发送给服务器
-b/--cookie <name=string/file>    cookie字符串或文件读取位置
-c/--cookie-jar <file>                    操作结束后把cookie写入到这个文件中
-C/--continue-at <offset>            断点续转
-D/--dump-header <file>              把header信息写入到该文件中
-e/--referer                                  来源网址
-f/--fail                                          连接失败时不显示http错误
-o/--output                                  把输出写到该文件中
-O/--remote-name                      把输出写到该文件中，保留远程文件的文件名
-r/--range <range>                      检索来自HTTP/1.1或FTP服务器字节范围
-s/--silent                                    静音模式。不输出任何东西
-T/--upload-file <file>                  上传文件
-u/--user <user[:password]>      设置服务器的用户和密码
-w/--write-out [format]                什么输出完成后
-x/--proxy <host[:port]>              在给定的端口上使用HTTP代理
-#/--progress-bar                        进度条显示当前的传送状态
```
## 2.2 curl 示例
```
curl ftp://name:passwd@ftp.server.example:port/full/path/to/file
curl -u name:passwd ftp://ftp.server.example:port/full/path/to/file
curl http://name:passwd@http.server.example/full/path/to/file
curl -u name:passwd http://http.server.example/full/path/to/file
curl -x my-proxy:888 ftp://ftp.example.com/README
curl -u user:passwd -x my-proxy:888 http://www.example.com/
curl -U user:passwd -x my-proxy:888 http://www.example.com/
curl --noproxy example.com -x my-proxy:888 http://www.example.com/
curl -L https://apt.example.org/llvm-snapshot.gpg.key | sudo apt-key add -
curl -r 0-99 http://www.example.com/
curl -r -500 http://www.example.com/
curl -T - ftp://ftp.example.com/myfile
curl -T uploadfile -u user:passwd ftp://ftp.example.com/myfile
curl -T localfile -a ftp://ftp.example.com/remotefile
curl --proxytunnel -x proxy:port -T localfile ftp.example.com
## 必须先将 HTTP 服务器配置为接受 PUT，然后才能成功执行此操作
curl -T - http://www.example.com/myfile
curl -v ftp://ftp.example.com/
curl --trace trace.txt www.haxx.se
curl --dump-header headers.txt curl.se
curl -d "name=Rafael%20Sagula&phone=3320780" http://www.example.com/guest.cgi
curl --data-urlencode "name=Rafael Sagula&phone=3320780" http://www.example.com/guest.cgi
curl -w "@curl-format" -o /dev/null  -sL "http://cloud.tencent.com/"
curl -c cookiec.txt  http://www.linux.com
curl -b cookiec.txt http://www.linux.com
curl -A "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.0)" http://www.linux.com
curl -e "www.linux.com" http://mail.linux.com
curl -O http://www.linux.com/{hello,bb}/dodo[1-5].JPG
curl -o #1_#2.JPG http://www.linux.com/{hello,bb}/dodo[1-5].JPG
curl -r 0-100 -o dodo1_part1.JPG http://www.linux.com/dodo1.JPG
curl -C -O http://www.linux.com/dodo1.JPG
```
## 2.3 可用的 --write-out 变量
![curl的w选项](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/curl的w选项.png)
在 curl 8.1.0 中，添加了仅输出特定 URL 组件的变量，以防 url or url_effective 变量显示的内容超出您的预期。
参考(everying-curl)[https://everything.curl.dev/usingcurl/verbose/writeout.html]

## 2.4  Unicode 编码的响应的转换
当使用 curl 命令发出请求并收到 Unicode 编码的响应时，中文字符可能会显示为 Unicode 转义序列（例如 \u4f60\u597d），而不是实际的中文字符（例如 你好）。这是因为 curl 默认不会对输出进行 Unicode 解码。
```
curl -s https://api.example.com/data | jq .
```
-s 选项会使 curl 静默模式运行，避免输出进度信息。jq . 会格式化 JSON 响应并正确处理 Unicode 字符。
