# PG数据库
## 简介
PostgreSQL是一款功能，性能，可靠性都可以和高端的国外商业数据库相媲美的开源数据库。而且PostgreSQL的许可和生态完全开放，不被任何一个单一的公司或国家所操控，保证了使用者没有后顾之忧。国内越来越多的企业开始用PostgreSQL代替原来昂贵的国外商业数据库。
## 安装工具选择
PostgreSQL的开源HA工具有很多种，下面几种算是比较常用的:
- PAF(PostgreSQL Automatic Failomianver)
- repmgr
- Patroni
![PG高可用工具比较](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/PG高可用工具比较.webp)
其中Patroni不仅简单易用而且功能非常强大。
- 支持自动failover和按需switchover
- 支持一个和多个备节点
- 支持级联复制
- 支持同步复制，异步复制
- 支持同步复制下备库故障时自动降级为异步复制（功效类似于MySQL的半同步，但是更加智能）
- 支持控制指定节点是否参与选主，是否参与负载均衡以及是否可以成为同步备机
- 支持通过pg_rewind自动修复旧主
- 支持多种方式初始化集群和重建备机，包括pg_basebackup和支持wal_e，pgBackRest，barman等备份工具的自定义脚本
- 支持自定义外部callback脚本
- 支持REST API
- 支持通过watchdog防止脑裂
- 支持k8s，docker等容器化环境部署
- 支持多种常见DCS(Distributed Configuration Store)存储元数据，包括etcd，ZooKeeper，Consul，Kubernetes

## Patroni使用
![PG高可用-patroni](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/PG高可用-patroni.jpg)

## 高可用模拟故障测试用例
### 高可用测试 Keepalived
|测试类型|测试方式|测试命令|测试结果|
|--|--|--|--|
| 进程故障 | 1\. 主端killall进程 | killall keepalived | VIP从主端自动转移到备端，5000端口和5001端口连接正常 |
| \- | \- | systemctl start keepalived | VIP从备端自动转移到主端，5000端口和5001端口连接正常 |
| \- | 2\. 备端killall进程 | systemctl stop keepalived | VIP在主端正常运行，5000端口和5001端口连接正常 |
| \- | \- | systemctl start keepalived | VIP在主端正常运行，5000端口和5001端口连接正常 |
| \- | 3\. 主端同时kill所有进程 | \- | 主端VIP未卸掉，备端也启动VIP，此时主备端均存在VIP（异常现象），5000端口和5001端口连接正常 |
| \- | \- | systemctl start keepalived | VIP转移到主端正常运行，备端无VIP，5000端口和5001端口连接正常 |
| \- | 4\. 主端只kill主进程 | kill -9 | VIP从主端自动转移到备端，VIP只在备端启动，5000端口和5001端口连接正常 |
| \- | \- | systemctl start keepalived | VIP转移到主端正常运行，备端无VIP，5000端口和5001端口连接正常 |
| \- | 5\. 主端只kill子进程 | \- | VIP从主端自动转移到备端，等待主进程自动生成子进程后，VIP从备端自动转移到主端，5000端口和5001端口连接正常 |
| \- | 6\. 备端kill 进程 | \- | IP在主端正常运行，5000端口和5001端口连接正常 |
| 网卡故障 | 1\. 主端down网卡 | ifdown ens33 | VIP从主端自动转移到备端，PostgreSQL发生故障转移到其中一个备库，5000端口和5001端口连接正常，patroni和etcd均不显示故障节点 |
| \- | 2\. 主端up网卡 | ifup ens33 | VIP从备端自动转移到主端，故障节点以备库角色添加到集群，patroni和etcd节点状态显示正常，5000端口和5001端口连接正常 |
| \- | 3\. 备端down网卡 | ifdown ens32 | VIP在主端正常运行，5000端口和5001端口连接正常，patroni和etcd均不显示故障节点，故障节点上的各个进程还在运行 |
| \- | 4\. 备端up网卡 | ifup ens32 | patroni和etcd节点状态显示正常 |

### 高可用测试 HAProxy

| 测试类型 | 测试方式 | 测试命令 | 测试结果 |
|--|--|--|--|
| 进程故障 | 1\. 主端killall进程 | killall haproxy | keepalived 未检测 haproxy 进程，自动将VIP从主端转移到备端，5000端口和5001端口连接正常 |
| \- | \- | systemctl start haproxy | keepalived 检测到 haproxy 进程，自动将VIP从备端转移到主端，5000端口和5001端口连接正常 |
| \- | 2\. 备端killall进程 | killall haproxy | VIP在主端正常运行，5000端口和5001端口连接正常 |
| \- | \- | systemctl start haproxy | VIP在主端正常运行，5000端口和5001端口连接正常 |
| \- | 3\. 主端同时kill所有进程 | \- | keepalived 未检测 haproxy 进程，自动将VIP从主端转移到备端，5000端口和5001端口连接正常 |
| \- | \- | systemctl start haproxy | keepalived 检测到 haproxy 进程，自动将VIP从备端转移到主端，5000端口和5001端口连接正常 |
| \- | 4\. 主端只kill主进程 | \- | keepalived 未检测 haproxy 进程，自动将VIP从主端转移到备端，5000端口和5001端口连接正常 |
| \- | \- | systemctl start haproxy | keepalived 检测到 haproxy 进程，自动将VIP从备端转移到主端，5000端口和5001端口连接正常 |
| \- | 5\. 主端只kill子进程 | \- | haproxy 的所有进程都死了，keepalived 未检测 haproxy 进程，自动将VIP从主端转移到备端，5000端口和5001端口连接正常 |
| \- | \- | systemctl start haproxy | keepalived 检测到 haproxy 进程，自动将VIP从备端转移到主端，5000端口和5001端口连接正常 |

### 高可用测试 Patroni
以下是在Patroni开启了auto failover的情况下进行测试

| 测试类型 | 测试方式 | 测试命令 | 测试结果 |
|--|--|--|--|
| 进程故障 | 1\. 主端killall进程 | killall patroni | 1\. 触发故障切换到备库其中一个节点，备库另一个节点同步新主库，切换时间在30秒内 2. 原主库(pgtest1)的 PostgreSQL 被关闭 3. etcd haproxy keepalived 在原主库正常运行，VIP 运行在原主库 4. VIP + 5000端口连接切换后的新主库，VIP + 5001端口连接另一个备库 |
| \- | \- | systemctl start patroni | 原主库(pgtest1)变成新主库(pgtest2)的备库 |
| \- | 2\. 主库kill patroni 进程 | kill -9 | 1\. 触发故障切换到备库其中一个节点，备库另一个节点同步新主库，切换时间在30秒内 2. 原主库(pgtest1)的 PostgreSQL 还在运行，并且是读写模式 3. etcd haproxy keepalived 在原主库正常运行，VIP 运行在原主库 4. VIP + 5000端口连接切换后的新主库，VIP + 5001端口连接另一个备库 |
| \- | \- | systemctl start patroni | 原主库(pgtest1)被 pg\_rewind 成新主库(pgtest2)的备库 |
| \- | 3\. 一个备库kill patroni 进程 | \- | 1\. 使用killall，将会同时关闭备库，使用kill，此备库的 PostgreSQL 还在以只读模式运行，且与主库正常同步数据 2. VIP + 5000端口正常连接主库，VIP+5001端口不能连接此备库，可以连接另一个备库 3. 主库与另一个备库不受影响 4. 此备库上的 etcd haproxy keepalived 正常运行 |
| \- | \- | systemctl start patroni | 自动恢复正常状态，与主库保持同步 |
| \- | 4\. 两个备库kill patroni 进程 | \- | 1\. 使用killall，将会同时关闭备库，使用kill，两个备库的 PostgreSQL 还在以只读模式运行，且与主库正常同步数据 2. VIP + 5000端口只连接主库，VIP + 5001端口连接失败 3. 主库不受影响 4. 备库上的 etcd haproxy keepalived 正常运行 |
| \- | \- | systemctl start patroni | 自动恢复正常状态，与主库保持同步 |

### 高可用测试 etcd

| 测试类型 | 测试方式 | 测试命令 | 测试结果 |
|--|--|--|--|
| 进程故障 | 1\. 主库kill etcd 进程 | \- | 不影响主库和备库, patroni 会连接其它节点上的etcd，VIP+5000/5001端口连接正常 |
| \- | 2\. 一个备库停止 etcd 进程 | \- | 不影响主库和备库, patroni 会连接其它节点上的etcd，VIP+5000/5001端口连接正常 |
| \- | 3\. 两个备库停止 etcd 进程 | \- | 此时超过了etcd的最大允许故障节点数，主备库3个节点均以只读模式运行，VIP + 5000端口连接失败，VIP + 5001端口轮询连接主备库3个节点 |
| \- | \- | 先启动第一个备库的 etcd 进程 | 主库从只读模式切换成读写模式，主从数据同步恢复正常，VIP + 5000/5001端口连接正常 |
| \- | \- | 再启动第二个备库的 etcd 进程 | 自动恢复正常状态，与主库保持同步 |

### 高可用测试 PostgreSQL
| 测试类型 | 测试方式 | 测试命令 | 测试结果 |
|--|--|--|--|
| \- | 停主库PostgreSQL实例 | \- | 主库被Patroni自动拉起，VIP + 5000/5001端口连接正常 |
| \- | 停备库PostgreSQL实例 | \- | 备库被Patroni自动拉起，VIP + 5000/5001端口连接正常 |

### 高可用测试 操作系统

| 测试类型 | 测试方式 | 测试命令 | 测试结果 |
|--|--|--|--|
| \- | 停PostgreSQL主库主机(同时是haproxy + keepalived 的主机) | reboot | 1\. 触发故障切换到备库其中一个节点，备库另一个节点同步新主库，切换时间在30秒内 2. VIP漂移到备库 3. VIP + 5000端口连接切换后的新主库，VIP + 5001端口连接另一个备库 |
| \- | \- | 启动 | 原主库(pgtest1)变成新主库(pgtest2)的备库，VIP从keepalived的备端自动转移到主端，5000端口和5001端口连接正常 |
| \- | 停备库的主机就不测试了 | \- | \- |

## 自动切换和脑裂防护
Patroni在主库故障时会自动执行failover，确保服务的高可用。但是自动failover如果控制不当会有产生脑裂的风险。因此Patroni在保障服务的可用性和防止脑裂的双重目标下会在特定场景下执行一些自动化动作。

| 故障位置 | 场景 | Patroni的动作 |
|--|--|--|--|
| 备库 | 备库PG停止 | 停止备库PG |
| 备库 | 停止备库Patroni | 停止备库PG |
| 备库 | 强杀备库Patroni（或Patroni crash） | 无操作 |
| 备库 | 备库无法连接etcd | 无操作 |
| 备库 | 非Leader角色但是PG处于生产模式 | 重启PG并切换到恢复模式作为备库运行 |
| 主库 | 主库PG停止 | 重启PG，重启超过`master_start_timeout`设定时间，进行主备切换 |
| 主库 | 停止主库Patroni | 停止主库PG，并触发failover |
| 主库 | 强杀主库Patroni（或Patroni crash） | 触发failover，此时出现"双主" |
| 主库 | 主库无法连接etcd | 将主库降级为备库，并触发failover |
| \- | etcd集群故障 | 将主库降级为备库，此时集群中全部都是备库。 |
| \- | 同步模式下无可用同步备库 | 临时切换主库为异步复制，在恢复为同步复制之前自动failover暂不生效 |

## 客户端访问配置
HA集群的主节点是动态的，主备发生切换时，客户端对数据库的访问也需要能够动态连接到新主上。有下面几种常见的实现方式，下面分别介绍。
- 多主机URL
- vip
- haproxy
### 多主机URL
pgjdbc和libpq驱动可以在连接字符串中配置多个IP，由驱动识别数据库的主备角色，连接合适的节点。
1. JDBC的多主机URL功能全面，支持**failover，读写分离和负载均衡**。可以通过参数配置不同的连接策略。
```
jdbc:postgresql://192.168.234.201:5432,192.168.234.202:5432,192.168.234.203:5432/postgres?targetServerType=primary
连接主节点(实际是可写的节点)。当出现"双主"甚至"多主"时驱动连接第一个它发现的可用的主节点
```
```
优先连接备节点，无可用备节点时连接主节点，有多个可用备节点时随机连接其中一个。
jdbc:postgresql://192.168.234.201:5432,192.168.234.202:5432,192.168.234.203:5432/postgres?targetServerType=preferSecondary&loadBalanceHosts=true
```
```
jdbc:postgresql://192.168.234.201:5432,192.168.234.202:5432,192.168.234.203:5432/postgres?targetServerType=any&loadBalanceHosts=true
随机连接任意一个可用的节点
```
2. libpq的多主机URL功能相对pgjdbc弱一点，只支持failover。
```
postgres://192.168.234.201:5432,192.168.234.202:5432,192.168.234.203:5432/postgres?target_session_attrs=read-write
连接主节点(实际是可写的节点)
postgres://192.168.234.201:5432,192.168.234.202:5432,192.168.234.203:5432/postgres?target_session_attrs=any
连接任一可用节点
基于libpq实现的其他语言的驱动相应地也可以支持多主机URL，比如python和php。下面是python程序使用多主机URL创建连接的例子
import psycopg2
conn=psycopg2.connect("postgres://192.168.234.201:5432,192.168.234.202:5432/postgres?target_session_attrs=read-write&password=123456")
```
### VIP(通过Patroni回调脚本实现VIP漂移）
多主机URL的方式部署简单，但是不是每种语言的驱动都支持，而且如果数据库出现意外的“双主”，配置多主机URL的客户端在多个主上同时写入的概率比较高，而如果客户端通过VIP的方式访问则在VIP上又多了一层防护.
Patroni支持用户配置在特定事件发生时触发回调脚本。因此我们可以配置一个回调脚本，在主备切换后动态加载VIP。
### VIP(通过keepalived实现VIP漂移)
使用REST API，Patroni可以和外部组件搭配使用。比如可以配置keepalived动态在主库或备库上绑VIP。
### haproxy
haproxy作为服务代理和Patroni配套使用可以很方便地支持failover，读写分离和负载均衡，也是Patroni社区作为Demo的方案。缺点是haproxy本身也会占用资源，所有数据流量都经过haproxy，性能上会有一定损耗。

## 通过端口实现读写分离机制
读写分离的核心思想是将数据库的读操作和写操作分开处理，通常通过以下方式实现：
- 主从复制（Master-Slave Replication）：将写操作发送到主数据库（Master），并将读操作发送到一个或多个从数据库（Slave）。
- 代理层（Proxy Layer）：在应用程序和数据库之间引入一个代理层，代理层根据请求类型（读或写）将其路由到相应的数据库实例。
- 应用程序逻辑：在应用程序中实现读写分离逻辑，根据操作类型将请求发送到不同的数据库节点。

实现读写分离的具体方法取决于所使用的数据库和应用程序。例如，对于PostgreSQL，可以使用主从复制和Patroni来实现读写分离。对于MySQL，可以使用主从复制和ProxySQL来实现读写分离。对于应用程序，可以使用数据库连接池和连接字符串来实现读写分离。

## SQLAlchemy调用
[sqlalchemy](https://fahadahammed.medium.com/unlocking-scalability-magic-run-postgres-read-write-nodes-on-docker-and-implement-it-with-pythons-5914804cd85a)

## VIP
**Keepalived**
优点
- 成熟稳定：Keepalived是一个成熟的解决方案，被广泛使用在生产环境中。
- 丰富的功能：支持VRRP（虚拟路由冗余协议）、健康检查、预防分裂脑（split-brain）等功能。
- 易于配置：配置文件结构清晰，易于理解和管理。
- 广泛支持：支持多种操作系统，如Linux和FreeBSD。
- 负载均衡支持：除了高可用性，Keepalived还可以配置简单的负载均衡功能。
缺点
- 复杂性：对于简单的HA需求，Keepalived的配置和管理可能显得过于复杂。
- 额外依赖：需要安装和配置额外的软件包。
**VIP Manager**
优点
- 专注高可用性：VIP Manager专注于管理虚拟IP地址，确保高可用性和故障转移。
- 轻量级：相对于Keepalived，VIP Manager可能更加轻量级，适合简单的HA需求。
- 灵活性：可以与各种负载均衡器和服务结合使用。
缺点
- 功能有限：VIP Manager可能不具备Keepalived的所有高级功能，如健康检查和负载均衡。
- 社区支持：相比Keepalived，VIP Manager的社区和文档可能相对较少。

## 连接池
### PgBouncer 和 SQLAlchemy 连接池的对比
**PgBouncer：**
特点：
- 外部服务：PgBouncer 是一个独立于应用程序的外部连接池服务。
- 轻量级：非常轻量级，易于部署和配置。
- 多应用共享：可以被多个应用程序共享，适用于多个数据库客户端。
连接池类型：
- Session pooling：每个客户端连接对应一个数据库连接。
- Transaction pooling：每个事务对应一个数据库连接。
- Statement pooling：每个 SQL 语句对应一个数据库连接。
配置灵活：可以通过配置文件调整不同的连接池策略和参数。
优点：
- 独立性：独立于应用程序，减少了应用程序的复杂性。
- 集成性：可以与任何支持 PostgreSQL 的客户端库一起使用。
- 性能：在高并发环境下表现良好，特别是事务和语句级别的池化。
缺点：
- 复杂性：需要额外的部署和管理。
- 调试难度：调试连接相关问题时可能需要更多的知识和工具。

**SQLAlchemy 连接池**
特点：
- 嵌入式：嵌入在应用程序代码中，作为 SQLAlchemy 库的一部分。
- 多种策略：支持多种连接池策略，如 QueuePool、SingletonThreadPool、StaticPool 等。
- 配置简单：通过 Python 代码进行配置，易于集成和使用。
- 内建支持：与 SQLAlchemy ORM 和 Core 紧密集成。
优点：
- 简单集成：无需额外的部署和配置，直接在应用程序代码中配置。
- 灵活性：可以根据具体的应用需求调整连接池策略和参数。
- 调试方便：调试连接池相关问题时更直观，直接在应用代码中进行。
缺点：
- 资源占用：连接池资源占用在应用程序进程中，对于内存和 CPU 有一定的消耗。
- 单一应用：每个应用实例需要单独配置和管理连接池，无法跨应用共享。

**使用选择**
使用 PgBouncer 的情景
多应用共享：如果有多个应用程序需要访问同一个数据库，PgBouncer 可以作为一个集中式的连接池服务，减少数据库连接数。
高并发要求：在高并发的环境下，PgBouncer 的事务和语句级别池化策略可以显著提高性能。
数据库连接管理：希望将数据库连接管理从应用程序中分离出来，简化应用程序的复杂性。
使用 SQLAlchemy 连接池的情景
单一应用：如果只有一个应用程序需要数据库连接池，使用 SQLAlchemy 内建的连接池更为简单直接。
开发和调试：在开发和调试阶段，SQLAlchemy 连接池配置简单，调试方便。
灵活配置：需要根据具体的应用需求灵活调整连接池策略和参数，SQLAlchemy 提供了多种内建策略，易于调整。
结论
选择使用 PgBouncer 还是 SQLAlchemy 内建的连接池，取决于具体的应用场景和需求：
PgBouncer 更适合多应用共享、高并发环境、需要独立管理数据库连接的场景。
SQLAlchemy 连接池 更适合单一应用、开发和调试阶段、需要灵活配置的场景。
