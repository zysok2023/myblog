# Linux收发网络包

## linux收发数据包

### 发送数据包

首先，应用程序会调用 Socket 发送数据包的接口，由于这个是系统调用，所以会从用户态陷入到内核态中的 Socket 层，内核会申请一个内核态的 sk_buff 内存，将用户待发送的数据拷贝到 sk_buff 内存，并将其加入到发送缓冲区。
接下来，网络协议栈从 Socket 发送缓冲区中取出 sk_buff，并按照 TCP/IP 协议栈从上到下逐层处理。
如果使用的是 TCP 传输协议发送数据，那么先拷贝一个新的 sk_buff 副本 ，这是因为 sk_buff 后续在调用网络层，最后到达网卡发送完成的时候，这个 sk_buff 会被释放掉。而 TCP 协议是支持丢失重传的，在收到对方的 ACK 之前，这个 sk_buff 不能被删除。所以内核的做法就是每次调用网卡发送的时候，实际上传递出去的是 sk_buff 的一个拷贝，等收到 ACK 再真正删除。
接着，对 sk_buff 填充 TCP 头。sk_buff 可以表示各个层的数据包，在应用层数据包叫 data，在 TCP 层我们称为 segment，在 IP 层我们叫 packet，在数据链路层称为 frame。为了在层级之间传递数据时，不发生拷贝，只用 sk_buff 一个结构体来描述所有的网络包
然后交给网络层，在网络层里会做这些工作：选取路由（确认下一跳的 IP）、填充 IP 头、netfilter 过滤、对超过 MTU 大小的数据包进行分片。处理完这些工作后会交给网络接口层处理。
网络接口层会通过 ARP 协议获得下一跳的 MAC 地址，然后对 sk_buff 填充帧头和帧尾，接着将 sk_buff 放到网卡的发送队列中。
这一些工作准备好后，会触发「软中断」告诉网卡驱动程序，这里有新的网络包需要发送，驱动程序会从发送队列中读取 sk_buff，将这个 sk_buff 挂到 RingBuffer 中，接着将 sk_buff 数据映射到网卡可访问的内存 DMA 区域，最后触发真实的发送。
当数据发送完成以后，其实工作并没有结束，因为内存还没有清理。当发送完成的时候，网卡设备会触发一个硬中断来释放内存，主要是释放 sk_buff 内存和清理 RingBuffer 内存。
最后，当收到这个 TCP 报文的 ACK 应答时，传输层就会释放原始的 sk_buff 。

### 接收数据包

网卡是计算机里的一个硬件，专门负责接收和发送网络包，当网卡接收到一个网络包后，会通过 DMA 技术，将网络包写入到指定的内存地址，也就是写入到 Ring Buffer ，这个是一个环形缓冲区，接着就会告诉操作系统这个网络包已经到达。
Linux 内核在 2.6 版本中引入了 NAPI 机制，它是混合「中断和轮询」的方式来接收网络包，它的核心概念就是不采用中断的方式读取数据，而是首先采用中断唤醒数据接收的服务程序，然后 poll 的方法来轮询数据。
因此，当有网络包到达时，会通过 DMA 技术，将网络包写入到指定的内存地址，接着网卡向 CPU 发起硬件中断，当 CPU 收到硬件中断请求后，根据中断表，调用已经注册的中断处理函数。
硬件中断处理函数会做如下的事情：

需要先「暂时屏蔽中断」，表示已经知道内存中有数据了，告诉网卡下次再收到数据包直接写内存就可以了，不要再通知 CPU 了，这样可以提高效率，避免 CPU 不停的被中断。
接着，发起「软中断」，然后恢复刚才屏蔽的中断。
至此，硬件中断处理函数的工作就已经完成。

## ASGI/WSGI

[微调](https://tonybaloney.github.io/posts/fine-tuning-wsgi-and-asgi-applications.html)
ASGI（Asynchronous Server Gateway Interface）和 WSGI（Web Server Gateway Interface）是两种用于Python Web应用服务器和框架之间通信的标准接口。
WSGI 是 Python Web 应用程序和 Web 服务器之间的标准接口，由 PEP 3333 定义。它是同步的，意味着它适用于传统的、阻塞的 Web 应用程序。
ASGI 是 WSGI 的异步版本，由 PEP 4843 定义，旨在支持异步编程模型。ASGI 允许处理 WebSockets、HTTP/2、异步任务等现代 Web 开发需求。
使用 Django、Flask 或 FastAPI 等 Python Web 框架进行开发时，您需要在顶部堆叠额外的软件，然后用户才能在 Web 浏览器中浏览您的网站。这些软件是：

- 一个 ASGI/WSGI Web 服务器，用于启动您的 Web 应用程序并侦听 HTTP 上的用户请求
- （可选）高性能 HTTP 服务器，用于提供图片、CSS 样式表和 JavaScript 源文件等静态资源。
  首先介绍两个选项中更简单的一个，即在 Web 框架中的 Python 代码和拥有 Web 浏览器的用户之间连接的 ASGI/WSGI Web 服务器：
  ASGI/WSGI 服务器专门设计用于处理发往 Python 代码的 HTTP 流量。大多数 HTML 页面都有大量静态资源，例如图片、CSS 文件和 JavaScript。通过 ASGI/WSGI Web 服务器发送所有这些请求并让 Python 处理它们是低效的。更好的解决方案是在专门处理静态内容的 ASGI/WSGI 服务器前面放置另一个 HTTP 服务器：
  WSGI 是 Web 服务器和 Python Web 框架之间的标准接口。 WSGI 是一个抽象层，支持 Python Web 服务器的开发，而无需绑定到 Flask 和 Django 等 Web 框架的 API。
  WSGI 的局限性在于它是在 Python 中的异步之前设计的。 Web 应用程序可以极大地受益于 Python 中的异步代码和协程，因为请求管道（传递 Web 请求时发生的事情）的大部分时间都花在等待事情上，例如 SQL 查询的结果或要运行的另一个 API。这些是异步的理想候选者。
  ASGI 是作为 WSGI 的继承者推出的，专门为异步 Web 框架设计。 Web 框架必须支持 ASGI 才能使用。 FastAPI 仅支持 ASGI，因此很简单。 Flask 仅支持 WSGI，但如果您想编写异步 Flask 应用程序，可以使用 Quart。 Django 有点复杂。 Django 3 引入了 ASGI 接口，但它非常有限，并且在版本 4 及更高版本中，Django 提供了完整的异步支持。

| Framework   | Support   |
| ----------- | --------- |
| Flask       | WSGI      |
| Quart       | ASGI      |
| Django <=3  | WSGI      |
| Django >= 4 | WSGI/ASGI |
| FastAPI     | ASGI      |

Gunicorn 是最流行的 WSGI 服务器
Uvicorn 是一个 ASGI 服务器。它既是一个独立的服务器，也是 Gunicorn 的插件
Hypercorn 是同时支持 WSGI 和 ASGI 的替代方案
