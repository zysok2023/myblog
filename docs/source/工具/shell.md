# shell

## 1. 快捷键
**编辑命令**
- Ctrl + a ：移到命令行首
- Ctrl + e ：移到命令行尾
- Ctrl + f ：按字符前移（右向）
- Ctrl + b ：按字符后移（左向）
- Alt + f ：按单词前移（右向）
- Alt + b ：按单词后移（左向）
- Ctrl + xx：在命令行首和光标之间移动
- Ctrl + u ：从光标处删除至命令行首
- Ctrl + k ：从光标处删除至命令行尾
- Ctrl + w ：从光标处删除至字首
- Alt + d ：从光标处删除至字尾
- Ctrl + d ：删除光标处的字符
- Ctrl + h ：删除光标前的字符
- Ctrl + y ：粘贴至光标后
- Alt + c ：从光标处更改为首字母大写的单词
- Alt + u ：从光标处更改为全部大写的单词
- Alt + l ：从光标处更改为全部小写的单词
- Ctrl + t ：交换光标处和之前的字符
- Alt + t ：交换光标处和之前的单词
- Alt + Backspace：与 Ctrl + w 相同类似，分隔符有些差别
**重新执行命令**
- Ctrl + r：逆向搜索命令历史
- Ctrl + g：从历史搜索模式退出
- Ctrl + p：历史中的上一条命令
- Ctrl + n：历史中的下一条命令
- Alt + .：使用上一条命令的最后一个参数
**控制命令**
- Ctrl + l：清屏
- Ctrl + o：执行当前命令，并选择上一条命令
- Ctrl + s：阻止屏幕输出
- Ctrl + q：允许屏幕输出
- Ctrl + c：终止命令
- Ctrl + z：挂起命令
- Bang (!) 命令
- !!：执行上一条命令
- !blah：执行最近的以 blah 开头的命令，如 !ls
- !blah:p：仅打印输出，而不执行
- !$：上一条命令的最后一个参数，与 Alt + . 相同
- !$:p：打印输出 !$ 的内容
- !*：上一条命令的所有参数
- !*:p：打印输出 !* 的内容
- ^blah：删除上一条命令中的 blah
- ^blah^foo：将上一条命令中的 blah 替换为 foo
- ^blah^foo^：将上一条命令中所有的 blah 都替换为 foo

## 2.命令
BRE 是较为传统的正则表达式语法，要求更多的转义字符。
ERE 是扩展语法，简化了许多常用模式的写法，无需大量转义。
sed和grep都是使用的BRE，如果需要使用ERE则需要加参数-E

### 2.1 grep
- 使用 --color 选项对 grep 结果进行着色
- 在所有目录中递归搜索字符串 grep -r "string-name" *
- 忽略大小写 grep -i "linux" welcome.txt
- 计算字符串与 -c 选项匹配的行数 grep -c "Linux" welcome.txt
- 使用 grep 反向输出  grep -v "Linux" welcome.txt
- 使用 -n 选项对包含搜索模式的行进行编号 grep -n "Linux" welcome.txt
- 使用 -w 选项搜索完全匹配的单词 grep -w "opensource" welcome.txt
- 显示搜索模式之前或之后的行数 grep -A2 -B3 welcome.txt

### 2.2 sed
- 替换或替换字符串 sed 's/unix/linux/' geekfile.txt
- 替换一行中第 n 次出现的模式 sed 's/unix/linux/2' geekfile.txt
- 替换行中出现的所有模式 sed 's/unix/linux/g' geekfile.txt
- 从第 n 次出现替换为一行中的所有出现  sed 's/unix/linux/3g' geekfile.txt
- 括号中每个单词的第一个字符 echo "Welcome To The Geek Stuff" | sed 's/\(\b[A-Z]\)/\(\1\)/g'
- 替换特定行号上的字符串 sed '3 s/unix/linux/' geekfile.txt
- 使用 /p 标志复制替换行 sed 's/unix/linux/p' geekfile.txt
- 仅打印替换的行 sed -n 's/unix/linux/p' geekfile.txt
- 在一系列行上替换字符串 sed '1,3 s/unix/linux/' geekfile.txt
- 从特定文件中删除行 sed '5d' filename.txt
- 删除最后一行 sed '$d' filename.txt
- 删除 x 到 y 范围内的行 sed 'x,yd' filename.txt
- 删除第n行到最后一行 sed 'nth,$d' filename.txt
- 删除模式匹配行 sed '/abc/d' filename.txt

### 2.3 awk
AWK 操作：逐行扫描文件 - 将每个输入行拆分为字段 - 将输入行/字段与模式进行比较 - 对匹配的行执行操作
- Awk 的默认行为：默认情况下，Awk 打印指定文件中的每一行数据。awk '{print}' 员工.txt
- 打印与给定模式匹配的行 awk '/manager/{print}'员工.txt
- 将一行拆分为字段 对于每条记录（即行），awk 命令默认以空格字符分隔记录并将其存储在 $n 变量中。如果该行有 4 个单词，则分别存储在 $1、$2、$3 和 $4 中。另外，$0 代表整行 awk '{print $1,$4}' 员工.txt
Awk 中的内置变量
- NR： NR 命令保存当前输入记录的数量。请记住，记录通常是行。Awk 命令对文件中的每个记录执行一次模式/操作语句。
- NF： NF 命令会统计当前输入记录中的字段数量。
- FS： FS 命令包含字段分隔符，用于在输入行上划分字段。默认为“空白”，即空格和制表符。可以将 FS 重新分配给另一个字符（通常在 BEGIN 中）以更改字段分隔符。
- RS： RS 命令存储当前记录分隔符。由于默认情况下，输入行是输入记录，因此默认的记录分隔符是换行符。
- OFS： OFS 命令存储输出字段分隔符，Awk 打印字段时会用该分隔符分隔字段。默认为空格。每当 print 有多个用逗号分隔的参数时，它会在每个参数之间打印 OFS 的值。
- ORS： ORS 命令存储输出记录分隔符，Awk 打印输出行时，它会分隔输出行。默认为换行符。print 会自动 将 ORS 的内容输出到打印内容的末尾。
```
# NR内置变量的使用（显示行号）
awk'{print NR,$0}'员工.txt
# NF 内置变量的使用（显示最后一个字段）
awk '{print $1,$NF}' 员工.txt
# NR内置变量的另一种用法（显示第3行到第6行）
awk 'NR==3，NR==6 {print NR,$0}' 员工.txt
#
```
### 2.4 xargs
xargs命令的-n和-L选项都用于控制每次传递给命令的参数数量
- -n <max-args>：这个选项指定每次传递给命令的最大参数数量。例如，-n1表示每次只传递一个参数给命令。如果输入的参数超过最大参数数量，xargs会将它们分批处理。
- -L <number>：这个选项指定每次传递给命令的行数（而不是参数数量）。例如，-L1表示每次传递一行给命令。-L选项通常用于处理以行为单位的输入数据，而不是以空格分隔的参数。

### 2.5 find
Linux 中的 find 命令是一个动态实用程序，设计用于在分层结构中进行全面的文件和目录搜索。它的适应性允许用户按名称、大小、修改时间或内容进行搜索，提供灵活而有效的解决方案。
- 在 Linux 中使用 find 命令搜索空文件和目录 find ./GFG -empty
- 在Linux中使用“find”命令搜索具有特定权限的文件 find ./GFG -perm 664
- 在 Linux 中使用“find”命令显示存储库层次结构 find . -type d
- 在 Linux 中使用“find”命令在多个文件中搜索文本 find ./ -type f -name "*.txt" -exec grep 'Geek'  {} \;
- 在 Linux 中使用“find”命令按修改时间查找文件 find /path/to/search -mtime -7
|字符|类型|说明|
|--|--|--|
|b |block (buffered) special|块设备|
|c |character (unbuffered) special|字符设备|
|d |directory|目录|
|p |named pipe (FIFO)|管道|
|f |regular file|常规文件|
|l |symbolic link;|符号链接|
|s |socket|套接字|
|D |door (Solaris)||

### 2.6 ps
ps命令提供了-o选项，用于自定义输出的格式。可以指定要显示的字段，并使用逗号分隔。常见的字段包括pid（进程ID）、ppid（父进程ID）、user（用户）、cmd（命令）等。例如：ps -o pid,ppid,user,cmd,%mem,%cpu,etime
- 按 CPU 占用排序进程  ps aux --sort=-%cpu
- 按内存占用排序进程 ps aux --sort=-%mem
- 按 PID 列出进程，使用命令 ps -fp PID
- 按 PPID 列出进程 ps -f –ppid
- 使用进程名查找 PID ps -C
- 打印流程树 ps -e --forest
- 根据线程过滤一个进程 ps -T 1446
- 显示组进程 列出组进程类似于列出用户进程 ps -fG
- 显示指定进程ID（PID）的所有线程信息 ps -eLf
ps 命令可以显示不同状态的进程，常见的进程状态包括：
- R ：运行状态。进程正在运行或准备运行
- S ：休眠状态。进程暂时停止执行，等待某个事件的发生，例如等待I/O操作完成或等待信号。
- Z ：僵尸进程。进程已经终止，但其父进程尚未对其进行善后处理（回收其资源），因此仍然保留在进程表中。
- D ：不可中断状态。进程处于不可中断的睡眠状态，通常是等待磁盘I/O操作完成
- T ：停止状态。进程已经停止执行，通常是由于接收到一个停止信号（如Ctrl+Z）
- +（Foreground process）：在Unix系统中，进程是前台进程，正在与用户交互
- -（Background process）：在Unix系统中，进程是后台进程，不与用户交互。

### 2.7 lsof
lsof（list open files）是一个查看当前系统文件的工具。在linux环境下，任何事物都以文件的形式存在，通过文件不仅仅可以访问常规数据，还可以访问网络连接和硬件。如传输控制协议 (TCP) 和用户数据报协议 (UDP) 套接字等，系统在后台都为该应用程序分配了一个文件描述符，该文件描述符提供了大量关于这个应用程序本身的信息。
- 使用-i显示所有连接 lsof -i，使用-i 6仅获取IPv6流量
- 通过某个进程号显示该进程打开的文件 lsof -p 11968
- 仅显示TCP连接（同理可获得UDP连接） lsof -iTCP
- 使用-i:port来显示与指定端口相关的网络信息 lsof -i :22
- 使用@host来显示指定到指定主机的连接 lsof -i@172.16.12.5
- 使用@host:port显示基于主机与端口的连接  lsof -i@172.16.12.5:22
- 找出正等候连接的端口 lsof -i -sTCP:LISTEN
- 找出已建立的连接 lsof -i -sTCP:ESTABLISHED
- 使用-u显示指定用户打开了什么  lsof -u daniel
- 使用-u ^user来显示除指定用户以外的其它所有用户所做的事情 lsof -u ^daniel
- 杀死指定用户所做的一切事情 kill -9 `lsof -t -u daniel`
- 使用-c查看指定的命令正在使用的文件和网络连接 lsof -c syslog-ng
- 使用-p查看指定进程ID已打开的内容 lsof -p 10075
- -t选项只返回PID lsof -t -c Mail
- 显示与指定目录交互的所有一切 lsof /var/log/messages/
- 显示与指定文件交互的所有一切 lsof /home/daniel/firewall_whitelist.txt
- 显示daniel连接到1.1.1.1所做的一切 lsof -u daniel -i @1.1.1.1
- 同时使用-t和-c选项以给进程发送 HUP 信号  kill -HUP `lsof -t -c sshd`
- lsof +L1显示所有打开的链接数小于1的文件 lsof +L1
- 显示某个端口范围的打开的连接 lsof -i @fw.google.com:2150=2180

### 2.8 lscpu
lscpu从sysfs和/proc/cpuinfo收集cpu体系结构信息，命令的输出比较易读,命令输出的信息包含cpu数量，线程，核数，套接字和Nom-Uniform Memeor Access(NUMA)，缓存等.
Architecture:         #架构
CPU(s):               #逻辑cpu颗数
Thread(s) per core:   #每个核心线程
Core(s) per socket:   #每个cpu插槽核数/每颗物理cpu核数
CPU socket(s):        #cpu插槽数
Vendor ID:            #cpu厂商ID
CPU family:           #cpu系列
Model:                #型号
Stepping:             #步进
CPU MHz:              #cpu主频
Virtualization:       #cpu支持的虚拟化技术
L1d cache:            #一级缓存,表示cpu的L1数据缓存
L1i cache:            #一级缓存（具体为L1指令缓存）
L2 cache:             #二级缓存

### 2.9 dd
dd 命令用于按指定的大小和数量来复制文件和转换数据。它可以用于创建、备份、恢复和转换文件。
```shell
dd if=/dev/zero of=/path/to/testfile bs=1G count=1 oflag=direct
dd if=/dev/urandom of=/path/to/random_file bs=1M count=1024
dd if=/path/to/backup.img of=/dev/sdX bs=4M
dd if=/dev/sdX of=/path/to/backup.img bs=4M
dd if=test.der of=test.tbs bs=1 skip=4 count=188
```
### 2.10 xxd
xxd 命令用于创建二进制文件的十六进制（hex）表示和将十六进制表示转换回二进制文件。
```shell
# 将二进制文件转换为十六进制表示
xxd filename
# 将十六进制表示转换回二进制文件,-r表示从十六进制转换，而-p表示使用纯粹的十六进制格式
xxd -r -p hexdata.txt binarydata
```

### 2.11 ulimit
ulimit 命令用于查看和设置用户级别的资源限制。这些限制可以防止某个进程消耗过多的系统资源，从而影响系统的稳定性和性能。
- -a：显示当前所有的限制。
- -c：设置core文件的最大值，单位为块。
- -d：设置数据段的最大值，单位为KB。
- -f：设置文件大小的最大值，单位为块。
- -l：设置可加锁内存的最大值，单位为KB。
- -m：设置进程的最大内存使用量，单位为KB。
- -n：设置文件描述符的最大数量。
- -s：设置堆栈的最大值，单位为KB。
- -t：设置CPU时间的最大值，单位为秒。
- -u：设置用户可打开的最大进程数。

### 2.12 ip
ip 命令用于配置和显示 Linux 系统的网络接口。它可以用于查看网络接口的状态，设置 IP 地址，路由，ARP 表等。
- 给一个网卡绑定多个ip
```shell
ip addr add 192.168.1.100/24 dev eth0
ip addr add 192.168.1.101/24 dev eth0
```

### 2.13 netstat
netstat 命令用于显示网络连接，路由表，接口统计，伪装连接和多播成员等信息。它可以用于查看网络接口的状态，设置 IP 地址，路由，ARP 表等。
- 显示所有TCP连接 netstat -t
- 显示所有UDP连接 netstat -u
- 显示所有TCP和UDP连接 netstat -tu
- 显示所有监听端口 netstat -l
- 显示所有监听端口和TCP连接 netstat -lt
- 显示所有监听端口和UDP连接 netstat -lu
- 显示所有监听端口和所有连接 netstat -tul
以下是常见的netstat命令输出结果中状态列可能包含的一些结果：
- ESTABLISHED：表示TCP连接已经建立，双方可以进行数据传输。
- SYN_SENT：表示正在发送连接请求，即处于TCP的第一次握手过程中。
- SYN_RECEIVED：表示收到连接请求并确认，即处于TCP的第二次握手过程中。
- FIN_WAIT_1：表示连接被关闭，但仍在等待对方发送关闭连接请求。
- FIN_WAIT_2：表示连接已经收到关闭请求，等待对方发送最后的确认。
- TIME_WAIT：表示连接已经关闭，但仍在等待足够的时间以确保对方收到了关闭请求的确认。
- CLOSE_WAIT：表示连接被关闭，但仍有待处理的数据或请求。
- LAST_ACK：表示已发送关闭请求，并等待对方的确认。
- LISTEN：表示服务器正在监听来自客户端的连接请求。
- CLOSING：表示正在关闭连接的最后阶段，即处于TCP的第四次握手过程中。
- UNKNOWN：表示状态未知或无法确定。
