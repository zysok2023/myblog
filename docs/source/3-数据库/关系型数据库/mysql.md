# Mysql
![日志提纲](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/提纲.jpg)
![锁提纲](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/锁提纲.jpg)
![索引提纲](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/索引提纲.jpg)
![bufferpool提纲](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/bufferpool提纲.jpg)
## 语句执行过程
### SELECT 语句
![mysql查询流程](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/mysql查询流程.jpg)
MySQL 的架构共分为两层：Server 层和存储引擎层
- Server 层负责建立连接、分析和执行 SQL。MySQL 大多数的核心功能模块都在这实现，主要包括连接器，查询缓存、解析器、预处理器、优化器、执行器等。另外，所有的内置函数（如日期、时间、数学和加密函数等）和所有跨存储引擎的功能（如存储过程、触发器、视图等。）都在 Server 层实现。
- 存储引擎层负责数据的存储和提取。支持 InnoDB、MyISAM、Memory 等多个存储引擎，不同的存储引擎共用一个 Server 层。现在最常用的存储引擎是 InnoDB，从 MySQL 5.5 版本开始， InnoDB 成为了 MySQL 的默认存储引擎。我们常说的索引数据结构，就是由存储引擎层实现的，不同的存储引擎支持的索引类型也不相同，比如 InnoDB 支持索引类型是 B+树 ，且是默认使用，也就是说在数据表中创建的主键索引和二级索引默认使用的是 B+ 树索引。
第一步：连接器
连接的过程需要先经过 TCP 三次握手，因为 MySQL 是基于 TCP 协议进行传输的，如果 MySQL 服务并没有启动，则会收到报错。如果 MySQL 服务正常运行，完成 TCP 连接的建立后，连接器就要开始验证你的用户名和密码，如果用户名或密码不对，就收到一个"Access denied for user"的错误，然后客户端程序结束执行。
如果用户密码都没有问题，连接器就会获取该用户的权限，然后保存起来，后续该用户在此连接里的任何操作，都会基于连接开始时读到的权限进行权限逻辑的判断。
所以，如果一个用户已经建立了连接，即使管理员中途修改了该用户的权限，也不会影响已经存在连接的权限。修改完成后，只有再新建的连接才会使用新的权限设置。
可以执行 show processlist 命令进行查看 MySQL 服务被多少个客户端连接了
Q1:空闲连接会一直占用着吗？
MySQL 定义了空闲连接的最大空闲时长，由 wait_timeout 参数控制的，默认值是 8 小时（28880秒），如果空闲连接超过了这个时间，连接器就会自动将它断开。
也可以手动断开空闲的连接，使用的是 kill connection + id 的命令
一个处于空闲状态的连接被服务端主动断开后，这个客户端并不会马上知道，等到客户端在发起下一个请求的时候，才会收到这样的报错“ERROR 2013 (HY000): Lost connection to MySQL server during query”。
Q2:MySQL 的连接数有限制吗？
MySQL 服务支持的最大连接数由 max_connections 参数控制，比如我的 MySQL 服务默认是 151 个,超过这个值，系统就会拒绝接下来的连接请求，并报错提示“Too many connections”。
MySQL 的连接也跟 HTTP 一样，有短连接和长连接的概念，它们的区别如下：
```
// 短连接
连接 mysql 服务（TCP 三次握手）
执行sql
断开 mysql 服务（TCP 四次挥手）

// 长连接
连接 mysql 服务（TCP 三次握手）
执行sql
执行sql
执行sql
....
断开 mysql 服务（TCP 四次挥手）
```
使用长连接的好处就是可以减少建立连接和断开连接的过程，所以一般是推荐使用长连接。
但是，使用长连接后可能会占用内存增多，因为 MySQL 在执行查询过程中临时使用内存管理连接对象，这些连接对象资源只有在连接断开时才会释放。如果长连接累计很多，将导致 MySQL 服务占用内存太大，有可能会被系统强制杀掉，这样会发生 MySQL 服务异常重启的现象。
Q3:怎么解决长连接占用内存的问题？
有两种解决方式。
第一种，定期断开长连接。既然断开连接后就会释放连接占用的内存资源，那么我们可以定期断开长连接。
第二种，客户端主动重置连接。MySQL 5.7 版本实现了 mysql_reset_connection() 函数的接口，注意这是接口函数不是命令，那么当客户端执行了一个很大的操作后，在代码里调用 mysql_reset_connection 函数来重置连接，达到释放内存的效果。这个过程不需要重连和重新做权限验证，但是会将连接恢复到刚刚创建完时的状态。
总结：
- 连接器与客户端进行 TCP 三次握手建立连接；
- 校验客户端的用户名和密码，如果用户名或密码不对，则会报错；
- 如果用户名和密码都对了，会读取该用户的权限，然后后面的权限逻辑判断都基于此时读取到的权限；
第二步：查询缓存
连接器得工作完成后，客户端就可以向 MySQL 服务发送 SQL 语句了，MySQL 服务收到 SQL 语句后，就会解析出 SQL 语句的第一个字段，看看是什么类型的语句。
如果 SQL 是查询语句（select 语句），MySQL 就会先去查询缓存（ Query Cache ）里查找缓存数据，看看之前有没有执行过这一条命令，这个查询缓存是以 key-value 形式保存在内存中的，key 为 SQL 查询语句，value 为 SQL 语句查询的结果。
如果查询的语句命中查询缓存，那么就会直接返回 value 给客户端。如果查询的语句没有命中查询缓存中，那么就要往下继续执行，等执行完后，查询的结果就会被存入查询缓存中。
**查询缓存还挺有用，但是其实查询缓存挺鸡肋的。**
对于更新比较频繁的表，查询缓存的命中率很低的，因为只要一个表有更新操作，那么这个表的查询缓存就会被清空。如果刚缓存了一个查询结果很大的数据，还没被使用的时候，刚好这个表有更新操作，查询缓冲就被清空了，相当于缓存了个寂寞。
**MySQL 8.0 版本直接将查询缓存删掉了，也就是说 MySQL 8.0 开始，执行一条 SQL 查询语句，不会再走到查询缓存这个阶段了。**
这里说的查询缓存是 server 层的，也就是 MySQL 8.0 版本移除的是 server 层的查询缓存，并不是 Innodb 存储引擎中的 buffer pool。
第三步：解析SQL
在正式执行 SQL 查询语句之前， MySQL 会先对 SQL 语句做解析，这个工作交由「解析器」来完成。
解析器会做如下两件事情。
第一件事情，词法分析。MySQL 会根据你输入的字符串识别出关键字出来，例如，SQL语句 select username from userinfo，在分析之后，会得到4个Token，其中有2个Keyword，分别为select和from：
第二件事情，语法分析。根据词法分析的结果，语法解析器会根据语法规则，判断你输入的这个 SQL 语句是否满足 MySQL 语法，如果没问题就会构建出 SQL 语法树，这样方便后面模块获取 SQL 类型、表名、字段名、 where 条件等等。
![mysql语法树](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/mysql语法树.jpg)
如果我们输入的 SQL 语句语法不对，就会在解析器这个阶段报错。比如，我下面这条查询语句，把 from 写成了 form，这时 MySQL 解析器就会给报错。
**解析器只负责检查语法和构建语法树，但是不会去查表或者字段存不存在。**
第四步：执行SQL
经过解析器后，接着就要进入执行 SQL 查询语句的流程了，每条SELECT 查询语句流程主要可以分为下面这三个阶段：
- prepare 阶段，也就是预处理阶段；
预处理阶段主要做两件事情：
1. 检查SQL查询语句的表或者字段是否存在
2. 将select *中的* 扩展为表上的所有列
- optimize 阶段，也就是优化阶段；
经过预处理阶段后，还需要为 SQL 查询语句先制定一个执行计划，这个工作交由「优化器」来完成的。
优化器主要负责将 SQL 查询语句的执行方案确定下来，比如在表里面有多个索引的时候，优化器会基于查询成本的考虑，来决定选择使用哪个索引。
要想知道优化器选择了哪个索引，我们可以在查询语句最前面加个 explain 命令，这样就会输出这条 SQL 语句的执行计划，然后执行计划中的 key 就表示执行过程中使用了哪个索引。
如果查询语句的执行计划里的 key 为 null 说明没有使用索引，那就会全表扫描（type = ALL），这种查询扫描的方式是效率最低档次的。
- execute 阶段，也就是执行阶段；
经历完优化器后，就确定了执行方案，接下来 MySQL 就真正开始执行语句了，这个工作是由「执行器」完成的。在执行的过程中，执行器就会和存储引擎交互了，交互是以记录为单位的。
1. 主键索引查询
```
select * from product where id = 1;
```
这条查询语句的查询条件用到了主键索引，而且是等值查询，同时主键 id 是唯一，不会有 id 相同的记录，所以优化器决定选用访问类型为 const 进行查询，也就是使用主键索引查询一条记录，那么执行器与存储引擎的执行流程是这样的：
  - 执行器第一次查询，会调用 read_first_record 函数指针指向的函数，因为优化器选择的访问类型为 const，这个函数指针被指向为 InnoDB 引擎索引查询的接口，把条件 id = 1 交给存储引擎，让存储引擎定位符合条件的第一条记录。
  - 存储引擎通过主键索引的 B+ 树结构定位到 id = 1的第一条记录，如果记录是不存在的，就会向执行器上报记录找不到的错误，然后查询结束。如果记录是存在的，就会将记录返回给执行器；
  - 执行器从存储引擎读到记录后，接着判断记录是否符合查询条件，如果符合则发送给客户端，如果不符合则跳过该记录。
  - 执行器查询的过程是一个 while 循环，所以还会再查一次，但是这次因为不是第一次查询了，所以会调用 read_record 函数指针指向的函数，因为优化器选择的访问类型为 const，这个函数指针被指向为一个永远返回 - 1 的函数，所以当调用该函数的时候，执行器就退出循环，也就是结束查询了。
2. 全表扫描
```
select * from product where name = 'iphone';
```
这条查询语句的查询条件没有用到索引，所以优化器决定选用访问类型为 ALL 进行查询，也就是全表扫描的方式查询，那么这时执行器与存储引擎的执行流程是这样的：
  - 执行器第一次查询，会调用 read_first_record 函数指针指向的函数，因为优化器选择的访问类型为 all，这个函数指针被指向为 InnoDB 引擎全扫描的接口，让存储引擎读取表中的第一条记录；
  - 执行器会判断读到的这条记录的 name 是不是 iphone，如果不是则跳过；如果是则将记录发给客户的（是的没错，Server 层每从存储引擎读到一条记录就会发送给客户端，之所以客户端显示的时候是直接显示所有记录的，是因为客户端是等查询语句查询完成后，才会显示出所有的记录）。
  - 执行器查询的过程是一个 while 循环，所以还会再查一次，会调用 read_record 函数指针指向的函数，因为优化器选择的访问类型为 all，read_record 函数指针指向的还是 InnoDB 引擎全扫描的接口，所以接着向存储引擎层要求继续读刚才那条记录的下一条记录，存储引擎把下一条记录取出后就将其返回给执行器（Server层），执行器继续判断条件，不符合查询条件即跳过该记录，否则发送到客户端；
  - 一直重复上述过程，直到存储引擎把表中的所有记录读完，然后向执行器（Server层） 返回了读取完毕的信息；
  - 执行器收到存储引擎报告的查询完毕的信息，退出循环，停止查询。

3. 索引下推
索引下推能够减少二级索引在查询时的回表操作，提高查询的效率，因为它将 Server 层部分负责的事情，交给存储引擎层去处理了。
一张用户表，对 age 和 reward 字段建立了联合索引（age，reward）
联合索引当遇到范围查询 (>、<) 就会停止匹配，也就是 age 字段能用到联合索引，但是 reward 字段则无法利用到索引。
不使用索引下推（MySQL 5.6 之前的版本）时，执行器与存储引擎的执行流程是这样的：
 - Server 层首先调用存储引擎的接口定位到满足查询条件的第一条二级索引记录，也就是定位到 age > 20 的第一条记录；
 - 存储引擎根据二级索引的 B+ 树快速定位到这条记录后，获取主键值，然后进行回表操作，将完整的记录返回给 Server 层；
 - Server 层在判断该记录的 reward 是否等于 100000，如果成立则将其发送给客户端；否则跳过该记录；
 - 接着，继续向存储引擎索要下一条记录，存储引擎在二级索引定位到记录后，获取主键值，然后回表操作，将完整的记录返回给 Server 层；
 - 如此往复，直到存储引擎把表中的所有记录读完。
可以看到，没有索引下推的时候，每查询到一条二级索引记录，都要进行回表操作，然后将记录返回给 Server，接着 Server 再判断该记录的 reward 是否等于 100000。
而使用索引下推后，判断记录的 reward 是否等于 100000 的工作交给了存储引擎层，过程如下 ：
 - Server 层首先调用存储引擎的接口定位到满足查询条件的第一条二级索引记录，也就是定位到 age > 20 的第一条记录；
 - 存储引擎定位到二级索引后，先不执行回表操作，而是先判断一下该索引中包含的列（reward列）的条件（reward 是否等于 100000）是否成立。如果条件不成立，则直接跳过该二级索引。如果成立，则执行回表操作，将完成记录返回给 Server 层。
 - Server 层在判断其他的查询条件（本次查询没有其他条件）是否成立，如果成立则将其发送给客户端；否则跳过该记录，然后向存储引擎索要下一条记录。
 - 如此往复，直到存储引擎把表中的所有记录读完。
使用了索引下推后，虽然 reward 列无法使用到联合索引，但是因为它包含在联合索引（age，reward）里，所以直接在存储引擎过滤出满足 reward = 100000 的记录后，才去执行回表操作获取整个记录。相比于没有使用索引下推，节省了很多回表操作。
当你发现执行计划里的 Extr 部分显示了 “Using index condition”，说明使用了索引下推。
### UPDATE 语句
```
UPDATE t_user SET name = 'xiaolin' WHERE id = 1;
```
- 客户端先通过连接器建立连接，连接器自会判断用户身份；
- 因为这是一条 update 语句，所以不需要经过查询缓存，但是表上有更新语句，是会把整个表的查询缓存清空的，所以说查询缓存很鸡肋，在 MySQL 8.0 就被移除这个功能了；
- 解析器会通过词法分析识别出关键字 update，表名等等，构建出语法树，接着还会做语法分析，判断输入的语句是否符合 MySQL 语法；
- 预处理器会判断表和字段是否存在；
- 优化器确定执行计划，因为 where 条件中的 id 是主键索引，所以决定要使用 id 这个索引；
- 执行器负责具体执行，找到这一行，然后更新。
不过，更新语句的流程会涉及到 undo log（回滚日志）、redo log（重做日志） 、binlog （归档日志）这三种日志。
## 事务
从转账说起：
![银行转账](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/银行转账.jpg)
这个转账的过程涉及到了两次修改数据库的操作。
假设在执行第三步骤之后，服务器忽然掉电了，就会发生一个不好的事情，我的账户扣了 100 万，但是钱并没有到你的账户上，也就是说这 100 万消失了！
要解决这个问题，就要保证转账业务里的所有数据库的操作是不可分割的，要么全部执行成功 ，要么全部失败，不允许出现中间状态的数据。
数据库中的「事务（Transaction）」就能达到这样的效果。在转账操作前先开启事务，等所有数据库操作执行完成后，才提交事务，对于已经提交的事务来说，该事务对数据库所做的修改将永久生效，如果中途发生发生中断或错误，那么该事务期间对数据库所做的修改将会被回滚到没执行该事务之前的状态。
### 事务特性
事务看起来感觉简单，但是要实现事务必须要遵守 4 个特性：
- 原子性（Atomicity）：**一个事务中的所有操作，要么全部完成，要么全部不完成**，不会结束在中间某个环节，而且事务在执行过程中发生错误，会被回滚到事务开始前的状态，就像这个事务从来没有执行过一样，就好比买一件商品，购买成功时，则给商家付了钱，商品到手；购买失败时，则商品在商家手中，消费者的钱也没花出去。
- 一致性（Consistency）：是指**事务操作前和操作后，数据满足完整性约束，数据库保持一致性状态。**比如，用户 A 和用户 B 在银行分别有 800 元和 600 元，总共 1400 元，用户 A 给用户 B 转账 200 元，分为两个步骤，从 A 的账户扣除 200 元和对 B 的账户增加 200 元。一致性就是要求上述步骤操作后，最后的结果是用户 A 还有 600 元，用户 B 有 800 元，总共 1400 元，而不会出现用户 A 扣除了 200 元，但用户 B 未增加的情况（该情况，用户 A 和 B 均为 600 元，总共 1200 元）。
- 隔离性（Isolation）：数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致，因为多个事务同时使用相同的数据时，不会相互干扰，每个事务都有一个完整的数据空间，对其他并发事务是隔离的。也就是说，消费者购买商品这个事务，是不影响其他消费者购买的。
- 持久性（Durability）：事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。
Q1:InnoDB 引擎通过什么技术来保证事务的这四个特性的呢？
持久性是通过 redo log （重做日志）来保证的；
原子性是通过 undo log（回滚日志） 来保证的；
隔离性是通过 MVCC（多版本并发控制） 或锁机制来保证的；
**一致性则是通过持久性+原子性+隔离性来保证；**

Q2:并行事务会引发什么问题？
MySQL 服务端是允许多个客户端连接的，这意味着 MySQL 会出现同时处理多个事务的情况。
那么在同时处理多个事务的时候，就可能出现脏读（dirty read）、不可重复读（non-repeatable read）、幻读（phantom read）的问题。

### 脏读&不可重复读&幻读
- 幻读
在一个事务内多次查询某个符合查询条件的「记录数量」，如果出现前后两次查询到的记录数量不一样的情况，就意味着发生了「幻读」现象。
![幻读](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/幻读.jpg)
- 脏读
如果一个事务「读到」了另一个「未提交事务修改过的数据」，就意味着发生了「脏读」现象。
![脏读](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/脏读.jpg)
- 不可重复读
在一个事务内多次读取同一个数据，如果出现前后两次读到的数据不一样的情况，就意味着发生了「不可重复读」现象。
**不可重复读主要关注同一行数据的多次读取结果是否一致。UPDATE和DELETE操作会导致不可重复读**
**幻读关注的是在事务中执行相同的查询时，查询结果的行数是否一致，INSERT和DELETE操作会导致幻读。**
**脏读强调的则是读取了未提交的数据**

### 隔离级别
SQL 标准提出了四种隔离级别来规避这些现象，隔离级别越高，性能效率就越低，这四个隔离级别如下：
- 读未提交（read uncommitted），指一个事务还没提交时，它做的变更就能被其他事务看到；
- 读提交（read committed），指一个事务提交之后，它做的变更才能被其他事务看到；
- 可重复读（repeatable read），指一个事务执行过程中看到的数据，一直跟这个事务启动时看到的数据是一致的，MySQL InnoDB 引擎的默认隔离级别；
- 串行化（serializable ）；会对记录加上读写锁，在多个事务对这条记录进行读写操作时，如果发生了读写冲突的时候，后访问的事务必须等前一个事务执行完成，才能继续执行；
按隔离水平高低排序如下：
串行化 > 可重复读 > 读提交 > 读未提交
![隔离级别与读](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/隔离级别与读.jpg)

MySQL 在「可重复读」隔离级别下，可以很大程度上避免幻读现象的发生（**注意是很大程度避免，并不是彻底避免**），所以 MySQL 并不会使用「串行化」隔离级别来避免幻读现象的发生，因为使用「串行化」隔离级别会影响性能。
Q1:什么是幻读？
The so-called phantom problem occurs within a transaction when the same query produces different sets of rows at different times. For example, if a SELECT is executed twice, but returns a row the second time that was not returned the first time, the row is a “phantom” row.
当同一个查询在不同的时间产生不同的结果集时，事务中就会出现所谓的幻象问题。
Q2:幻读是如何产生的？
幻读发生在两个事务之间，其中一个事务在读取某一范围的数据时，另外一个事务对该范围的数据进行了插入或删除数据,从而导致了前一个事务在后续读取数据时发现了幻影数据。

MySQL InnoDB 引擎的默认隔离级别虽然是「可重复读」，但是它很大程度上避免幻读现象（并不是完全解决了，解决的方案有两种：
- 针对快照读（普通 select 语句），是通过 MVCC 方式解决了幻读，因为可重复读隔离级别下，事务执行过程中看到的数据，一直跟这个事务启动时看到的数据是一致的，即使中途有其他事务插入了一条数据，是查询不出来这条数据的，所以就很好了避免幻读问题。
- 针对当前读（select ... for update 等语句），是通过 next-key lock（记录锁+间隙锁）方式解决了幻读，因为当执行 select ... for update 语句的时候，会加上 next-key lock，如果有其他事务在 next-key lock 锁范围内插入了一条记录，那么这个插入语句就会被阻塞，无法成功插入，所以就很好了避免幻读问题。
Q1:快照读是如何避免幻读的？
可重复读隔离级是由 MVCC（多版本并发控制）实现的，实现的方式是开始事务后（执行 begin 语句后），在执行第一个查询语句后，会创建一个 Read View，后续的查询语句利用这个 Read View，通过这个 Read View 就可以在 undo log 版本链找到事务开始时的数据，所以事务过程中每次查询的数据都是一样的，即使中途有其他事务插入了新纪录，是查询不出来这条数据的，所以就很好了避免幻读问题。
Q2:当前读是如何避免幻读的？
MySQL 里除了普通查询是快照读，其他都是当前读，比如 update、insert、delete，这些语句执行前都会查询最新版本的数据，然后再做进一步的操作。
这很好理解，假设你要 update 一个记录，另一个事务已经 delete 这条记录并且提交事务了，这样不是会产生冲突吗，所以 update 的时候肯定要知道最新的数据。
另外，select ... for update 这种查询语句是当前读，每次执行的时候都是读取最新的数据。
**如果当前读的事务先启动，那么别的事务修改数据就会被堵塞,直到当前读的事务完成；如果当前读的事务后启动，那么就会别的事务阻塞，直到背的事务执行完成**
Innodb 引擎为了解决「可重复读」隔离级别使用「当前读」而造成的幻读问题，就引出了间隙锁。
假设，表中有一个范围 id 为（3，5）间隙锁，那么其他事务就无法插入 id = 4 这条记录了，这样就有效的防止幻读现象的发生。
![gap锁](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/gap锁.jpg)
举个具体例子，场景如下：
事务 A 执行了这面这条锁定读语句后，就在对表中的记录加上 id 范围为 (2, +∞] 的 next-key lock（next-key lock 是间隙锁+记录锁的组合）。
然后，事务 B 在执行插入语句的时候，判断到插入的位置被事务 A 加了 next-key lock，于是事物 B 会生成一个插入意向锁，同时进入等待状态，直到事务 A 提交了事务。这就避免了由于事务 B 插入新记录而导致事务 A 发生幻读的现象。
Q3:幻读被完全解决了吗？
**可重复读隔离级别下虽然很大程度上避免了幻读，但是还是没有能完全解决幻读。**
场景1:
事务 A 执行查询 id = 5 的记录，此时表中是没有该记录的，所以查询不出来。
```sql
# 事务 A
mysql> begin;
Query OK, 0 rows affected (0.00 sec)

mysql> select * from t_stu where id = 5;
Empty set (0.01 sec)
```
然后事务 B 插入一条 id = 5 的记录，并且提交了事务。
```sql
# 事务 B
mysql> begin;
Query OK, 0 rows affected (0.00 sec)

mysql> insert into t_stu values(5, '小美', 18);
Query OK, 1 row affected (0.00 sec)

mysql> commit;
Query OK, 0 rows affected (0.00 sec)
```
此时，事务 A 更新 id = 5 这条记录，对没错，事务 A 看不到 id = 5 这条记录，但是他去更新了这条记录，这场景确实很违和，然后再次查询 id = 5 的记录，事务 A 就能看到事务 B 插入的纪录了，幻读就是发生在这种违和的场景。
```sql
# 事务 A
mysql> update t_stu set name = '小林coding' where id = 5;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> select * from t_stu where id = 5;
```
在可重复读隔离级别下，事务 A 第一次执行普通的 select 语句时生成了一个 ReadView，之后事务 B 向表中新插入了一条 id = 5 的记录并提交。接着，事务 A 对 id = 5 这条记录进行了更新操作，在这个时刻，这条新记录的 trx_id 隐藏列的值就变成了事务 A 的事务 id，之后事务 A 再使用普通 select 语句去查询这条记录时就可以看到这条记录了，于是就发生了幻读。
因为这种特殊现象的存在，所以我们认为 MySQL Innodb 中的 MVCC 并不能完全避免幻读现象。

场景2:
除了上面这一种场景会发生幻读现象之外，还有下面这个场景也会发生幻读现象。
- T1 时刻：事务 A 先执行「快照读语句」：select * from t_test where id > 100 得到了 3 条记录。
- T2 时刻：事务 B 往插入一个 id= 200 的记录并提交；
- T3 时刻：事务 A 再执行「当前读语句」 select * from t_test where id > 100 for update 就会得到 4 条记录，此时也发生了幻读现象。
要避免这类特殊场景下发生幻读的现象的话，就是尽量在开启事务之后，马上执行 select ... for update 这类当前读的语句，因为它会对记录加 next-key lock，从而避免其他事务插入一条新记录。

### 隔离级别案例分析
![隔离级别案例](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/隔离级别案例.jpg)

- 在「读未提交」隔离级别下，事务 B 修改余额后，虽然没有提交事务，但是此时的余额已经可以被事务 A 看见了，于是事务 A 中余额 V1 查询的值是 200 万，余额 V2、V3 自然也是 200 万了；
- 在「读提交」隔离级别下，事务 B 修改余额后，因为没有提交事务，所以事务 A 中余额 V1 的值还是 100 万，等事务 B 提交完后，最新的余额数据才能被事务 A 看见，因此额 V2、V3 都是 200 万；
- 在「可重复读」隔离级别下，事务 A 只能看见启动事务时的数据，所以余额 V1、余额 V2 的值都是 100 万，当事务 A 提交事务后，就能看见最新的余额数据了，所以余额 V3 的值是 200 万；
- 在「串行化」隔离级别下，事务 B 在执行将余额 100 万修改为 200 万时，由于此前事务 A 执行了读操作，这样就发生了读写冲突，于是就会被锁住，直到事务 A 提交后，事务 B 才可以继续执行，所以从 A 的角度看，余额 V1、V2 的值是 100 万，余额 V3 的值是 200万。

四种隔离级别具体是如何实现的：
- 对于「读未提交」隔离级别的事务来说，因为可以读到未提交事务修改的数据，所以直接读取最新的数据就好了；
- 对于「串行化」隔离级别的事务来说，通过加读写锁的方式来避免并行访问；
- 对于「读提交」和「可重复读」隔离级别的事务来说，它们是通过 Read View 来实现的，它们的区别在于创建 Read View 的时机不同，大家可以把 Read View 理解成一个数据快照，就像相机拍照那样，定格某一时刻的风景。「读提交」隔离级别是在「每个语句执行前」都会重新生成一个 Read View，而「可重复读」隔离级别是「启动事务时」生成一个 Read View，然后整个事务期间都在用这个 Read View。
注意，执行「开始事务」命令，并不意味着启动了事务。在 MySQL 有两种开启事务的命令，分别是：
- 第一种：begin/start transaction 命令；
- 第二种：start transaction with consistent snapshot 命令；
这两种开启事务的命令，事务的启动时机是不同的：
- 执行了 begin/start transaction 命令后，并不代表事务启动了。事务真正启动的时机通常是在事务执行了第一个读或写操作时
- 执行了 start transaction with consistent snapshot 命令，就会马上启动事务。
## MVCC
多版本并发控制（Multi-Version Concurrency Control, MVCC）是一种用于解决数据库系统中并发事务控制问题的机制。MVCC 通过维护数据的多个版本，允许并发事务对同一数据行进行读写操作，而不会相互阻塞，从而提高数据库的性能和并发性。
### 聚簇索引
只有InnoDB 存储引擎才支持聚簇索引，InnoDB 存储引擎中的每个表都有一个聚簇索引。聚簇索引将数据行和主键值存储在一起。
- 主键：如果表定义了主键，InnoDB 会将主键作为聚簇索引。
- 没有主键：如果表没有定义主键，InnoDB 会选择一个唯一非空索引作为聚簇索引。
- 没有唯一非空索引：如果表既没有主键，也没有唯一非空索引，InnoDB 会自动生成一个隐藏的聚簇索引。

Q1:Read View 到底是个什么东西？
![readview结构](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/readview结构.jpg)
Read View 有四个重要的字段：
- m_ids ：指的是在创建 Read View 时，当前数据库中「活跃事务」的事务 id 列表，注意是一个列表，“活跃事务”指的就是，启动了但还没提交的事务。
- min_trx_id ：指的是在创建 Read View 时，当前数据库中「活跃事务」中事务 id 最小的事务，也就是 m_ids 的最小值。
- max_trx_id ：这个并不是 m_ids 的最大值，而是创建 Read View 时当前数据库中应该给下一个事务的 id 值，也就是全局事务中最大的事务 id 值 + 1；
- creator_trx_id ：指的是创建该 Read View 的事务的事务 id。
![隐藏列](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/隐藏列.jpg)
对于使用 InnoDB 存储引擎的数据库表，它的聚簇索引记录中都包含下面两个隐藏列：
- trx_id，当一个事务对某条聚簇索引记录进行改动时，就会把该事务的事务 id 记录在 trx_id 隐藏列里；
- roll_pointer，每次对某条聚簇索引记录进行改动时，都会把旧版本的记录写入到 undo 日志中，然后这个隐藏列是个指针，指向每一个旧版本记录，于是就可以通过它找到修改前的记录。
![ReadView](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/ReadView.jpg)
一个事务去访问记录的时候，除了自己的更新记录总是可见之外，还有这几种情况：
- 如果记录的 trx_id 值小于 Read View 中的 min_trx_id 值，表示这个版本的记录是在创建 Read View 前已经提交的事务生成的，所以该版本的记录对当前事务可见。
- 如果记录的 trx_id 值大于等于 Read View 中的 max_trx_id 值，表示这个版本的记录是在创建 Read View 后才启动的事务生成的，所以该版本的记录对当前事务不可见。
- 如果记录的 trx_id 值在 Read View 的 min_trx_id 和 max_trx_id 之间，需要判断 trx_id 是否在 m_ids 列表中：
  - 如果记录的 trx_id 在 m_ids 列表中，表示生成该版本记录的活跃事务依然活跃着（还没提交事务），所以该版本的记录对当前事务不可见。
  - 如果记录的 trx_id 不在 m_ids列表中，表示生成该版本记录的活跃事务已经被提交，所以该版本的记录对当前事务可见。
这种通过「版本链」来控制并发事务访问同一个记录时的行为就叫 MVCC（多版本并发控制）。

Q2:可重复读是如何工作的？
可重复读隔离级别是启动事务时生成一个 Read View，然后整个事务期间都在用这个 Read View。
假设事务 A （事务 id 为51）启动后，紧接着事务 B （事务 id 为52）也启动了，那这两个事务创建的 Read View 如下：
![事务ab的视图](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/事务ab的视图.jpg)
事务 A 和 事务 B 的 Read View 具体内容如下：
- 在事务 A 的 Read View 中，它的事务 id 是 51，由于它是第一个启动的事务，所以此时活跃事务的事务 id 列表就只有 51，活跃事务的事务 id 列表中最小的事务 id 是事务 A 本身，下一个事务 id 则是 52。
- 在事务 B 的 Read View 中，它的事务 id 是 52，由于事务 A 是活跃的，所以此时活跃事务的事务 id 列表是 51 和 52，活跃的事务 id 中最小的事务 id 是事务 A，下一个事务 id 应该是 53。
接着，在可重复读隔离级别下，事务 A 和事务 B 按顺序执行了以下操作：
- 事务 B 读取小林的账户余额记录，读到余额是 100 万；
- 事务 A 将小林的账户余额记录修改成 200 万，并没有提交事务；
- 事务 B 读取小林的账户余额记录，读到余额还是 100 万；
- 事务 A 提交事务；
- 事务 B 读取小林的账户余额记录，读到余额依然还是 100 万；
事务 B 第一次读小林的账户余额记录，在找到记录后，它会先看这条记录的 trx_id，此时发现 trx_id 为 50，比事务 B 的 Read View 中的 min_trx_id 值（51）还小，这意味着修改这条记录的事务早就在事务 B 启动前提交过了，所以该版本的记录对事务 B 可见的，也就是事务 B 可以获取到这条记录。
接着，事务 A 通过 update 语句将这条记录修改了（还未提交事务），将小林的余额改成 200 万，这时 MySQL 会记录相应的 undo log，并以链表的方式串联起来，形成版本链，如下图：
![事务ab的视图2](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/事务ab的视图2.jpg)
可以在上图的「记录的字段」看到，由于事务 A 修改了该记录，以前的记录就变成旧版本记录了，于是最新记录和旧版本记录通过链表的方式串起来，而且最新记录的 trx_id 是事务 A 的事务 id（trx_id = 51）。
然后事务 B 第二次去读取该记录，发现这条记录的 trx_id 值为 51，在事务 B 的 Read View 的 min_trx_id 和 max_trx_id 之间，则需要判断 trx_id 值是否在 m_ids 范围内，判断的结果是在的，那么说明这条记录是被还未提交的事务修改的，这时事务 B 并不会读取这个版本的记录。而是沿着 undo log 链条往下找旧版本的记录，直到找到 trx_id 「小于」事务 B 的 Read View 中的 min_trx_id 值的第一条记录，所以事务 B 能读取到的是 trx_id 为 50 的记录，也就是小林余额是 100 万的这条记录。

最后，当事物 A 提交事务后，由于隔离级别时「可重复读」，所以事务 B 再次读取记录时，还是基于启动事务时创建的 Read View 来判断当前版本的记录是否可见。所以，即使事物 A 将小林余额修改为 200 万并提交了事务， 事务 B 第三次读取记录时，读到的记录都是小林余额是 100 万的这条记录。

就是通过这样的方式实现了，「可重复读」隔离级别下在事务期间读到的记录都是事务启动前的记录。

Q3:读提交是如何工作的?
读提交隔离级别是在每次读取数据时，都会生成一个新的 Read View。
也意味着，事务期间的多次读取同一条数据，前后两次读的数据可能会出现不一致，因为可能这期间另外一个事务修改了该记录，并提交了事务。
假设事务 A （事务 id 为51）启动后，紧接着事务 B （事务 id 为52）也启动了，接着按顺序执行了以下操作：
- 事务 B 读取数据（创建 Read View），小林的账户余额为 100 万；
- 事务 A 修改数据（还没提交事务），将小林的账户余额从 100 万修改成了 200 万；
- 事务 B 读取数据（创建 Read View），小林的账户余额为 100 万；
- 事务 A 提交事务；
- 事务 B 读取数据（创建 Read View），小林的账户余额为 200 万；
那具体怎么做到的呢？我们重点看事务 B 每次读取数据时创建的 Read View。前两次 事务 B 读取数据时创建的 Read View 如下图：

![读提交事务](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/读提交事务.jpg)
我们来分析下为什么事务 B 第二次读数据时，读不到事务 A （还未提交事务）修改的数据？

事务 B 在找到小林这条记录时，会看这条记录的 trx_id 是 51，在事务 B 的 Read View 的 min_trx_id 和 max_trx_id 之间，接下来需要判断 trx_id 值是否在 m_ids 范围内，判断的结果是在的，那么说明这条记录是被还未提交的事务修改的，这时事务 B 并不会读取这个版本的记录。而是，沿着 undo log 链条往下找旧版本的记录，直到找到 trx_id 「小于」事务 B 的 Read View 中的 min_trx_id 值的第一条记录，所以事务 B 能读取到的是 trx_id 为 50 的记录，也就是小林余额是 100 万的这条记录。

我们来分析下为什么事务 A 提交后，事务 B 就可以读到事务 A 修改的数据？

在事务 A 提交后，由于隔离级别是「读提交」，所以事务 B 在每次读数据的时候，会重新创建 Read View，此时事务 B 第三次读取数据时创建的 Read View 如下：
![读提交事务2](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/读提交事务2.jpg)
事务 B 在找到小林这条记录时，会发现这条记录的 trx_id 是 51，比事务 B 的 Read View 中的 min_trx_id 值（52）还小，这意味着修改这条记录的事务早就在创建 Read View 前提交过了，所以该版本的记录对事务 B 是可见的。

正是因为在读提交隔离级别下，事务每次读数据时都重新创建 Read View，那么在事务期间的多次读取同一条数据，前后两次读的数据可能会出现不一致，因为可能这期间另外一个事务修改了该记录，并提交了事务。

## 三大日志(redolog、undolog、binlog)
### undo log
undo log（回滚日志）：是 Innodb 存储引擎层生成的日志，实现了事务中的原子性，主要用于事务回滚和 MVCC。
Q1:为什么需要undo log?
数据刷盘和事务提交是独立的两个过程，也就是说事务没有提交成功，数据也可能被刷盘。为了保证数据的原子性，需要记录undo log进行事务回滚。
Q2:那些操作需要记录undo log?
每当 InnoDB 引擎对一条记录进行操作（修改、删除、新增）时，要把回滚时需要的信息都记录到 undo log 里，比如：
- 在插入一条记录时，要把这条记录的主键值记下来，这样之后回滚时只需要把这个主键值对应的记录删掉就好了；
- 在删除一条记录时，要把这条记录中的内容都记下来，这样之后回滚时再把由这些内容组成的记录插入到表中就好了；
- 在更新一条记录时，要把被更新的列的旧值记下来，这样之后回滚时再把这些列更新为旧值就好了。
在发生回滚时，就读取 undo log 里的数据，然后做原先相反操作。
不同的操作，需要记录的内容也是不同的，所以不同类型的操作（修改、删除、新增）产生的 undo log 的格式也是不同的。
一条记录的每一次更新操作产生的 undo log 格式都有一个 roll_pointer 指针和一个 trx_id 事务id：
- 通过 trx_id 可以知道该记录是被哪个事务修改的；
- 通过 roll_pointer 指针可以将这些 undo log 串成一个链表，这个链表就被称为版本链；
![版本链](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/版本链.jpg)

另外，undo log 还有一个作用，通过 ReadView + undo log 实现 MVCC（多版本并发控制）。

对于「读提交」和「可重复读」隔离级别的事务来说，它们的快照读（普通 select 语句）是通过 Read View + undo log 来实现的，它们的区别在于创建 Read View 的时机不同：
- 「读提交」隔离级别是在每个 select 都会生成一个新的 Read View，也意味着，事务期间的多次读取同一条数据，前后两次读的数据可能会出现不一致，因为可能这期间另外一个事务修改了该记录，并提交了事务。
- 「可重复读」隔离级别是启动事务时生成一个 Read View，然后整个事务期间都在用这个 Read View，这样就保证了在事务期间读到的数据都是事务启动前的记录。
这两个隔离级别实现是通过「事务的 Read View 里的字段」和「记录中的两个隐藏列（trx_id 和 roll_pointer）」的比对，如果不满足可见行，就会顺着 undo log 版本链里找到满足其可见性的记录，从而控制并发事务访问同一个记录时的行为，这就叫 MVCC（多版本并发控制）
undo log 两大作用：
- 实现事务回滚，保障事务的原子性。事务处理过程中，如果出现了错误或者用户执行了ROLLBACK语句，MySQL 可以利用undo log中的历史数据将数据恢复到事务开始之前的状态。
- 实现MVCC（多版本并发控制）关键因素之一。MVCC 是通过 ReadView + undo log 实现的。undo log 为每条记录保存多份历史数据，MySQL 在执行快照读（普通 select 语句）的时候，会根据事务的 Read View 里的信息，顺着 undo log 的版本链找到满足其可见性的记录。
Q3:undo log 是如何刷盘（持久化到磁盘）的？
undo log 和数据页的刷盘策略是一样的，都需要通过 redo log 保证持久化。buffer pool 中有 undo 页，对 undo 页的修改也都会记录到 redo log。redo log 会每秒刷盘，提交事务时也会刷盘，数据页和 undo 页都是靠这个机制保证持久化的。
### redo log
**即使事务提交并且执行成功，也可能会出现数据未落盘的情况**
redo log（重做日志）：是 Innodb 存储引擎层生成的日志，实现了事务中的持久性，主要用于掉电等故障恢复；
redo是重做的意思，redo log就是重做日志的意思。redo log是如何保证数据不会丢失的呢？
就是在修改之后，先将修改后的值记录到磁盘上的redo log中，就算突然断电了，Buffer Pool中的数据全部丢失了，来电的时候也可以根据redo log恢复Buffer Pool，这样既利用到了Buffer Pool的内存高效性，也保证了数据不会丢失。
![redolog做恢复](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/redolog做恢复.gif)

既然redo log文件也在磁盘上，数据文件也在磁盘上，都是磁盘操作，为什么不直接将修改的数据写到数据文件里面去呢？因为redo log是磁盘顺序写，数据刷盘是磁盘随机写，磁盘的顺序写比随机写高效的多。
这种先预写日志后面再将数据刷盘的机制，有一个高大上的专业名词——WAL（Write-ahead logging），翻译成中文就是预写式日志。
虽然磁盘顺序写已经很高效了，但是和内存操作还是有一定的差距。给redo log也加一个内存buffer，也就是redo log buffer，用这种套娃式的方法进一步提高效率。

以MySQL挂了有两种情况：
- MySQL挂了，操作系统也挂了，也就是常说的服务器宕机了。这种情况Buffer Pool里面的数据会全部丢失，操作系统的os cache里面的数据也会丢失。
- MySQL挂了，操作系统没有挂。这种情况Buffer Pool里面的数据会全部丢失，操作系统的os cache里面的数据不会丢失。

#### redo log的落盘机制
redo log的刷盘机制由参数innodb_flush_log_at_trx_commit控制，这个参数有3个值可以设置：
- innodb_flush_log_at_trx_commit = 1：实时写，实时刷
每次事务提交时，InnoDB 会将 redo log buffer 中的日志数据立即写入操作系统缓存，并立即强制刷新到磁盘。
这提供了最高的数据安全性，但可能会导致更高的 I/O 开销。
- innodb_flush_log_at_trx_commit = 0：延迟写，延迟刷
Redo log buffer 中的日志数据每秒写入操作系统缓存，并且每秒从操作系统缓存刷新到磁盘。这个行为由 InnoDB 后台线程控制。如果 MySQL 崩溃，最近 1 秒内的数据可能会丢失。
innodb_flush_log_at_timeout 参数来设置具体的刷新时间间隔
- innodb_flush_log_at_trx_commit = 2：实时写，延迟刷
每次事务提交时，InnoDB 会将 redo log buffer 中的日志数据立即写入操作系统缓存，但不会立即强制刷新到磁盘。
这种情况下如果MySQL进程挂了，操作系统没挂的话，操作系统还是会将os cache刷到磁盘，数据不会丢失。但如果MySQL所在的服务器挂掉了，也就是操作系统都挂了，那么os cache也会被清空，数据还是会丢失。
所以，这种redo log刷盘策略是上面两种策略的折中策略，效率比较高，丢失数据的风险比较低，绝大多情况下都推荐这种策略。
总结一下，redo log的作用是用于恢复数据，写redo log的过程是磁盘顺序写，有三种刷盘策略，有innodb_flush_log_at_trx_commit 参数控制，推荐设置成2。
### 归档 - binlog
binlog （归档日志）：是 Server 层生成的日志，主要用于数据备份和主从复制。
undo log记录的是修改之前的数据，提供回滚的能力。
redo log记录的是修改之后的数据，提供了崩溃恢复的能力。
binlog记录的是修改之后的数据，用于归档。
和redo log日志类似，binlog也有着自己的刷盘策略，通过sync_binlog参数控制：
- sync_binlog = 0 ：每次提交事务前将binlog写入os cache，由操作系统控制什么时候刷到磁盘
- sync_binlog =1 ：采用同步写磁盘的方式来写binlog，不使用os cache来写binlog
- sync_binlog = N ：当每进行n次事务提交之后，调用一次fsync将os cache中的binlog强制刷到磁盘
binlog的三种记录方式
1. STATEMENT 模式（SQL 语句级别）
2. ROW 模式（行级别），在 ROW 模式下，binlog 会记录每一行的完整值（变化前后的数据），适用于需要高一致性和精确复制的场景
3. MIXED 模式（混合模式）
### redolog和binlog的区别
binlog和redo log都是记录的修改之后的值，这两者有什么区别呢？有redo log为什么还需要binlog呢？
- binlog是逻辑日志，记录的是对哪一个表的哪一行做了什么修改；redo log是物理日志，记录的是对哪个数据页中的哪个记录做了什么修改，如果你还不了解数据页，你可以理解成对磁盘上的哪个数据做了修改。
- binlog是追加写；redo log是循环写，日志文件有固定大小，会覆盖之前的数据。
- binlog是Server层的日志；redo log是InnoDB的日志。如果不使用InnoDB引擎，是没有redo log的。
不用redo log取代binlog最大的原因：
第一点，binlog的生态已经建立起来。MySQL高可用主要就是依赖binlog复制，还有很多公司的数据分析系统和数据处理系统，也都是依赖的binlog。
第二点，binlog并不是MySQL的瓶颈，花时间在没有瓶颈的地方没必要。
### redolog和undolog的区别
- redo log是物理日志，记录的是在某个数据页上做了什么修改，是物理结构，记录的是数据页的物理修改。
- undo log是逻辑日志，记录的是某个数据被修改前的值，是逻辑结构，记录的是数据修改的相反操作。
- redo log是循环写，undo log是链表结构。

Redo Log 和 Undo Log 并不一定总是成对存在。虽然在大多数情况下它们会一起使用，但它们的记录情况取决于具体的操作类型和事务的执行情况。下面详细说明两者的区别和在不同操作中的使用情况。
- INSERT、UPDATE、DELETE会触发Redo Log 和 Undo Log
- 纯读操作：SELECT操作不会触发Redo Log和Undo Log的记录，因为没有数据修改
- DDL操作：如CREATE TABLE、ALTER TABLE等操作，主要记录在系统表空间的Redo Log中，通常不会生成Undo Log。
- 仅Redo Log操作：在某些情况下，比如缓存刷新，可能只涉及Redo Log而不涉及Undo Log

CREATE TABLE等DDL操作不需要生成Undo Log，因为这些操作涉及的主要是元数据的修改，且具有立即生效和不可撤销的特性。Undo Log主要用于支持行级操作的撤销和一致性读，而这些需求在DDL操作中并不存在。因此，DDL操作仅需要记录Redo Log以确保在系统崩溃后能够重做这些操作。

### 数据写入机制
- WAL机制：在修改数据时，InnoDB会先将修改记录在redo log中。这确保即使系统崩溃，已经记录在redo log中的修改也可以被重做。
![wal机制](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/wal机制.jpg)
- 缓冲池（Buffer Pool）：InnoDB使用缓冲池来缓存数据页。对数据的修改首先会在缓冲池中进行，而不会立即写入磁盘。这种方式提高了性能。
- 修改数据：当一个事务将age=1修改成age=2时，InnoDB会在缓冲池中修改相应的数据页，并记录undo log和redo log。
- 刷脏页：后台线程会周期性地将缓冲池中的脏页（即被修改但尚未写回磁盘的页）刷入磁盘，以减少内存压力和确保数据的一致性。这时，age=2的数据页可能会被刷入磁盘。
总结：数据刷盘和事务提交是独立的两个过程，共同确保了数据库的持久性和一致性。
1. 数据刷盘可以在事务未提交时进行：事务进行中，修改的数据页会被记录在缓冲池中，并可能在事务提交前就被刷入磁盘。这有助于提高系统性能和内存使用效率。
2. 事务提交依赖redo log：事务提交时，InnoDB会将redo log写入磁盘并标记为已提交。这确保了即使系统崩溃，已经提交的事务也不会丢失。在事务提交前，虽然数据页可能已经被刷入磁盘，但这些数据对其他事务仍不可见。
3. 崩溃恢复：如果系统崩溃，InnoDB会使用redo log来重做已提交但尚未写入磁盘的事务，同时使用undo log来撤销未提交的事务。这确保了数据库在恢复后的一致性。

## Buffer Pool
![掉电丢失数据](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/掉电丢失数据.gif)
**Buffer Pool是基于内存的，而只要一断电，内存里面的数据就会全部丢失。**如果断电的时候Buffer Pool的数据还没来得及刷到磁盘，数据就会丢失。

### buffer_pool的重要性
Innodb 存储引擎设计了一个缓冲池（Buffer Pool），来提高数据库的读写性能。
![缓冲池](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/缓冲池.jpg)
- 当读取数据时，如果数据存在于 Buffer Pool 中，客户端就会直接读取 Buffer Pool 中的数据，否则再去磁盘中读取。
- 当修改数据时，首先是修改 Buffer Pool 中数据所在的页，然后将其页设置为脏页，最后由后台线程将脏页写入到磁盘。
### Buffer Pool 有多大
Buffer Pool 是在 MySQL 启动的时候，向操作系统申请的一片连续的内存空间，默认配置下 Buffer Pool 只有 128MB 。
可以通过调整 innodb_buffer_pool_size 参数来设置 Buffer Pool 的大小，一般建议设置成可用物理内存的 60%~80%。
### Buffer Pool 缓存什么
InnoDB 会把存储的数据划分为若干个「页」，以页作为磁盘和内存交互的基本单位，一个页的默认大小为 16KB。因此，Buffer Pool 同样需要按「页」来划分。在 MySQL 启动的时候，InnoDB 会为 Buffer Pool 申请一片连续的内存空间，然后按照默认的16KB的大小划分出一个个的页， Buffer Pool 中的页就叫做缓存页。此时这些缓存页都是空闲的，之后随着程序的运行，才会有磁盘上的页被缓存到 Buffer Pool 中。

MySQL 刚启动的时候，会观察到使用的虚拟内存空间很大，而使用到的物理内存空间却很小，这是因为只有这些虚拟内存被访问后，操作系统才会触发缺页中断，接着将虚拟地址和物理地址建立映射关系。
Buffer Pool 除了缓存「索引页」和「数据页」，还包括了 undo 页，插入缓存、自适应哈希索引、锁信息等等。
![bufferpool内容](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/bufferpool内容.jpg)

为了更好的管理这些在 Buffer Pool 中的缓存页，InnoDB 为每一个缓存页都创建了一个控制块，控制块信息包括「缓存页的表空间、页号、缓存页地址、链表节点」等等。
控制块也是占有内存空间的，它是放在 Buffer Pool 的最前面，接着才是缓存页，如下图：

![缓存页](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/缓存页.jpg)
上图中控制块和缓存页之间灰色部分称为碎片空间。

Q1:查询一条记录，就只需要缓冲一条记录吗？
当我们查询一条记录时，InnoDB 是会把整个页的数据加载到 Buffer Pool 中，因为，通过索引只能定位到磁盘中的页，而不能定位到页中的一条记录。将页加载到 Buffer Pool 后，再通过页里的页目录去定位到某条具体的记录。

### 如何管理 Buffer Pool
- 如何管理空闲页？

- 如何管理脏页？
- 如何提高缓存命中率？
LRU（Least recently used）算法：该算法的思路是，链表头部的节点是最近使用的，而链表末尾的节点是最久没被使用的。那么，当空间不够了，就淘汰最久没被使用的节点，从而腾出空间。
简单的 LRU 算法的实现思路是这样的：
1. 当访问的页在 Buffer Pool 里，就直接把该页对应的 LRU 链表节点移动到链表的头部。
2. 当访问的页不在 Buffer Pool 里，除了要把页放入到 LRU 链表的头部，还要淘汰 LRU 链表末尾的节点。
![lru链表](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/lru链表.png)
Buffer Pool 里有三种页和链表来管理数据。
![bufferpoll_page](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/bufferpoll_page.jpg)
1. Free Page（空闲页），表示此页未被使用，位于 Free 链表；
2. Clean Page（干净页），表示此页已被使用，但是页面未发生修改，位于LRU 链表。
3. Dirty Page（脏页），表示此页「已被使用」且「已经被修改」，其数据和磁盘上的数据已经不一致。当脏页上的数据写入磁盘后，内存数据和磁盘数据一致，那么该页就变成了干净页。脏页同时存在于 LRU 链表和 Flush 链表。

- 脏页什么时候会被刷入磁盘？
引入了 Buffer Pool 后，当修改数据时，首先是修改 Buffer Pool 中数据所在的页，然后将其页设置为脏页，但是磁盘中还是原数据。
因此，脏页需要被刷入磁盘，保证缓存和磁盘数据一致，但是若每次修改数据都刷入磁盘，则性能会很差，因此一般都会在一定时机进行批量刷盘。
下面几种情况会触发脏页的刷新：
1. 当 redo log 日志满了的情况下，会主动触发脏页刷新到磁盘；
2. Buffer Pool 空间不足时，需要将一部分数据页淘汰掉，如果淘汰的是脏页，需要先将脏页同步到磁盘；
3. MySQL 认为空闲时，后台线程会定期将适量的脏页刷入到磁盘；
4. MySQL 正常关闭之前，会把所有的脏页刷入到磁盘；
在我们开启了慢 SQL 监控后，如果你发现**「偶尔」会出现一些用时稍长的 SQL**，这可能是因为脏页在刷新到磁盘时可能会给数据库带来性能开销，导致数据库操作抖动。
如果间断出现这种现象，就需要调大 Buffer Pool 空间或 redo log 日志的大小。

总结：
- Innodb 存储引擎设计了一个缓冲池（Buffer Pool），来提高数据库的读写性能。
- Buffer Pool 以页为单位缓冲数据，可以通过 innodb_buffer_pool_size 参数调整缓冲池的大小，默认是 128 M。
- Innodb 通过三种链表来管理缓页：
1. Free List （空闲页链表），管理空闲页；
2. Flush List （脏页链表），管理脏页；
3. LRU List，管理脏页+干净页，将最近且经常查询的数据缓存在其中，而不常查询的数据就淘汰出去。；
InnoDB 对 LRU 做了一些优化，我们熟悉的 LRU 算法通常是将最近查询的数据放到 LRU 链表的头部，而 InnoDB 做 2 点优化：
- 将 LRU 链表 分为young 和 old 两个区域，加入缓冲池的页，优先插入 old 区域；页被访问时，才进入 young 区域，目的是为了解决预读失效的问题。
- 当**「页被访问」且「 old 区域停留时间超过 innodb_old_blocks_time 阈值（默认为1秒）」**时，才会将页插入到 young 区域，否则还是插入到 old 区域，目的是为了解决批量数据访问，大量热数据淘汰的问题。
可以通过调整 innodb_old_blocks_pct 参数，设置 young 区域和 old 区域比例。

## 索引
所谓的存储引擎，说白了就是如何存储数据、如何为存储的数据建立索引和如何更新、查询数据等技术的实现方法。MySQL 存储引擎有 MyISAM 、InnoDB、Memory，其中 InnoDB 是在 MySQL 5.5 之后成为默认的存储引擎。
### 索引的分类
可以按照四个角度来分类索引：
- 按「数据结构」分类：B+tree索引、Hash索引、Full-text索引。
![索引分类](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/索引分类.JPG)
InnoDB 是在 MySQL 5.5 之后成为默认的 MySQL 存储引擎，B+Tree 索引类型也是 MySQL 存储引擎采用最多的索引类型。
在创建表时，InnoDB 存储引擎会根据不同的场景选择不同的列作为索引：
1. 如果有主键，默认会使用主键作为聚簇索引的索引键（key）；
2. 如果没有主键，就选择第一个不包含 NULL 值的唯一列作为聚簇索引的索引键（key）；
3. 在上面两个都没有的情况下，InnoDB 将自动生成一个隐式自增 id 列作为聚簇索引的索引键（key）；
其它索引都属于辅助索引（Secondary Index），也被称为二级索引或非聚簇索引。**创建的主键索引和二级索引默认使用的是 B+Tree 索引。**
```sql
CREATE TABLE `product`  (
  `id` int(11) NOT NULL,
  `product_no` varchar(20)  DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `price` decimal(10, 2) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
```
商品表里，有这些行数据：
![商品表](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/商品表.jpg)
这些行数据，存储在 B+Tree 索引时是长什么样子的？
B+Tree 是一种多叉树，叶子节点才存放数据，非叶子节点只存放索引，而且每个节点里的数据是按主键顺序存放的。每一层父节点的索引值都会出现在下层子节点的索引值中，因此在叶子节点中，包括了所有的索引值信息，并且每一个叶子节点都有两个指针，分别指向下一个叶子节点和上一个叶子节点，形成一个双向链表。
![btree](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/btree.jpg)
- 通过主键查询商品数据的过程
```sql
select * from product where id= 5;
```
这条语句使用了主键索引查询 id 号为 5 的商品。查询过程是这样的，B+Tree 会自顶向下逐层进行查找：
1. 将 5 与根节点的索引数据 (1，10，20) 比较，5 在 1 和 10 之间，所以根据 B+Tree的搜索逻辑，找到第二层的索引数据 (1，4，7)；
2. 在第二层的索引数据 (1，4，7)中进行查找，因为 5 在 4 和 7 之间，所以找到第三层的索引数据（4，5，6）；
3. 在叶子节点的索引数据（4，5，6）中进行查找，然后我们找到了索引值为 5 的行数据。
数据库的索引和数据都是存储在硬盘的，我们可以把读取一个节点当作一次磁盘 I/O 操作。那么上面的整个查询过程一共经历了 3 个节点，也就是进行了 3 次 I/O 操作。
**B+Tree 存储千万级的数据只需要 3-4 层高度就可以满足，这意味着从千万级的表查询目标数据最多需要 3-4 次磁盘 I/O，所以B+Tree 相比于 B 树和二叉树来说，最大的优势在于查询效率很高，因为即使在数据量很大的情况，查询一个数据的磁盘 I/O 依然维持在 3-4次。**
- 通过二级索引查询商品数据的过程
主键索引的 B+Tree 和二级索引的 B+Tree 区别如下：
1. 主键索引的 B+Tree 的叶子节点存放的是实际数据，所有完整的用户记录都存放在主键索引的 B+Tree 的叶子节点里；
2. 二级索引的 B+Tree 的叶子节点存放的是主键值，而不是实际数据。
将前面的商品表中的 product_no （商品编码）字段设置为二级索引，那么二级索引的 B+Tree 如下图
![二级索引btree](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/二级索引btree.jpg)

其中非叶子的 key 值是 product_no（图中橙色部分），叶子节点存储的数据是主键值（图中绿色部分）。
```sql
select * from product where product_no = '0002';
```
会先检二级索引中的 B+Tree 的索引值（商品编码，product_no），找到对应的叶子节点，然后获取主键值，然后再通过主键索引中的 B+Tree 树查询到对应的叶子节点，然后获取整行数据。这个过程叫**「回表」**，也就是说要查两个 B+Tree 才能查到数据。
![回表](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/回表.jpg)
当查询的数据是能在二级索引的 B+Tree 的叶子节点里查询到，这时就不用再查主键索引查，比如下面这条查询语句：
```sql
select id from product where product_no = '0002';
```
这种在二级索引的 B+Tree 就能查询到结果的过程就叫作**「覆盖索引」**，也就是只需要查一个 B+Tree 就能找到数据。
Q1:为什么 MySQL InnoDB 选择 B+tree 作为索引的数据结构？
1. B+Tree vs B Tree
B+Tree 只在叶子节点存储数据，而 B 树 的非叶子节点也要存储数据，所以 B+Tree 的单个节点的数据量更小，在相同的磁盘 I/O 次数下，就能查询更多的节点。
另外，B+Tree 叶子节点采用的是双链表连接，适合 MySQL 中常见的基于范围的顺序查找，而 B 树无法做到这一点。
2. B+Tree vs 二叉树
对于有 N 个叶子节点的 B+Tree，其搜索复杂度为O(logdN)，其中 d 表示节点允许的最大子节点个数为 d 个。
在实际的应用当中， d 值是大于100的，这样就保证了，即使数据达到千万级别时，B+Tree 的高度依然维持在 3~4 层左右，也就是说一次数据查询操作只需要做 3~4 次的磁盘 I/O 操作就能查询到目标数据。
而二叉树的每个父节点的儿子节点个数只能是 2 个，意味着其搜索复杂度为 O(logN)，这已经比 B+Tree 高出不少，因此二叉树检索到目标数据所经历的磁盘 I/O 次数要更多。
3. B+Tree vs Hash
Hash 在做等值查询的时候效率贼快，搜索复杂度为 O(1)。
但是 Hash 表不适合做范围查询，它更适合做等值的查询，这也是 B+Tree 索引要比 Hash 表索引有着更广泛的适用场景的原因。
- 按「物理存储」分类：聚簇索引（主键索引）、二级索引（辅助索引）
从物理存储的角度来看，索引分为聚簇索引（主键索引）、二级索引（辅助索引）。
1. 主键索引的 B+Tree 的叶子节点存放的是实际数据，所有完整的用户记录都存放在主键索引的 B+Tree 的叶子节点里；
2. 二级索引的 B+Tree 的叶子节点存放的是主键值，而不是实际数据。
在查询时使用了二级索引，如果查询的数据能在二级索引里查询的到，那么就不需要回表，这个过程就是覆盖索引。如果查询的数据不在二级索引里，就会先检索二级索引，找到对应的叶子节点，获取到主键值后，然后再检索主键索引，就能查询到数据了，这个过程就是回表。
- 按「字段特性」分类：主键索引、唯一索引、普通索引、前缀索引。
从字段特性的角度来看，索引分为主键索引、唯一索引、普通索引、前缀索引。
1. 主键索引
主键索引就是建立在主键字段上的索引，通常在创建表的时候一起创建，一张表最多只有一个主键索引，索引列的值不允许有空值。
在创建表时，创建主键索引的方式如下：
```SQL
CREATE TABLE table_name  (
  ....
  PRIMARY KEY (index_column_1) USING BTREE
);
```
2. 唯一索引
唯一索引建立在 UNIQUE 字段上的索引，一张表可以有多个唯一索引，索引列的值必须唯一，但是允许有空值。
在创建表时，创建唯一索引的方式如下：
```SQL
CREATE TABLE table_name  (
  ....
  UNIQUE KEY(index_column_1,index_column_2,...)
);
```
建表后，如果要创建唯一索引，可以使用这面这条命令：
```sql
CREATE UNIQUE INDEX index_name
ON table_name(index_column_1,index_column_2,...);
```
3. 普通索引
普通索引就是建立在普通字段上的索引，既不要求字段为主键，也不要求字段为 UNIQUE。
在创建表时，创建普通索引的方式如下：
```sql
CREATE TABLE table_name  (
  ....
  INDEX(index_column_1,index_column_2,...)
);
```
建表后，如果要创建普通索引，可以使用这面这条命令：

```sql
CREATE INDEX index_name
ON table_name(index_column_1,index_column_2,...);
```
4. 前缀索引
前缀索引是指对字符类型字段的前几个字符建立的索引，而不是在整个字段上建立的索引，前缀索引可以建立在字段类型为 char、 varchar、binary、varbinary 的列上。
使用前缀索引的目的是为了减少索引占用的存储空间，提升查询效率。
在创建表时，创建前缀索引的方式如下：
```sql
CREATE TABLE table_name(
    column_list,
    INDEX(column_name(length))
);
```
建表后，如果要创建前缀索引，可以使用这面这条命令：
```sql
CREATE INDEX index_name
ON table_name(column_name(length));
```
- 按「字段个数」分类：单列索引、联合索引。
建立在单列上的索引称为单列索引，比如主键索引；
建立在多列上的索引称为联合索引；
1. 联合索引
通过将多个字段组合成一个索引，该索引就被称为联合索引。
比如，将商品表中的 product_no 和 name 字段组合成联合索引(product_no, name)，创建联合索引的方式如下：
```sql
CREATE INDEX index_product_no_name ON product(product_no, name);
```
联合索引(product_no, name) 的 B+Tree 示意图如下:
![联合索引](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/联合索引.jpg)
联合索引的非叶子节点用两个字段的值作为 B+Tree 的 key 值。当在联合索引查询数据时，先按 product_no 字段比较，在 product_no 相同的情况下再按 name 字段比较。
也就是说，联合索引查询的 B+Tree 是先按 product_no 进行排序，然后再 product_no 相同的情况再按 name 字段排序。
因此，使用联合索引时，存在**最左匹配原则**，也就是按照最左优先的方式进行索引的匹配。在使用联合索引进行查询的时候，如果不遵循「最左匹配原则」，联合索引会失效，这样就无法利用到索引快速查询的特性了。
比如，如果创建了一个 (a, b, c) 联合索引，如果查询条件是以下这几种，就可以匹配上联合索引：
1. where a=1；
2. where a=1 and b=2 and c=3；
3. where a=1 and b=2；
需要注意的是，因为有查询优化器，所以 a 字段在 where 子句的顺序并不重要。
但是，如果查询条件是以下这几种，因为不符合最左匹配原则，所以就无法匹配上联合索引，联合索引就会失效:
1. where b=2；
2. where c=3；
3. where b=2 and c=3；
上面这些查询条件之所以会失效，是因为(a, b, c) 联合索引，是先按 a 排序，在 a 相同的情况再按 b 排序，在 b 相同的情况再按 c 排序。所以，b 和 c 是全局无序，局部相对有序的，这样在没有遵循最左匹配原则的情况下，是无法利用到索引的。
举联合索引（a，b）的例子，该联合索引的 B+ Tree 如下:
![联合索引案例](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/联合索引案例.jpg)
a 是全局有序的（1, 2, 2, 3, 4, 5, 6, 7 ,8），而 b 是全局是无序的（12，7，8，2，3，8，10，5，2）。因此，直接执行where b = 2这种查询条件没有办法利用联合索引的，利用索引的前提是索引里的 key 是有序的。
只有在 a 相同的情况才，b 才是有序的，比如 a 等于 2 的时候，b 的值为（7，8），这时就是有序的，这个有序状态是局部的，因此，执行where a = 2 and b = 7是 a 和 b 字段能用到联合索引的，也就是联合索引生效了。
联合索引范围查询
联合索引有一些特殊情况，并不是查询过程使用了联合索引查询，就代表联合索引中的所有字段都用到了联合索引进行索引查询，也就是可能存在部分字段用到联合索引的 B+Tree，部分字段没有用到联合索引的 B+Tree 的情况。
这种特殊情况就发生在范围查询。联合索引的最左匹配原则会一直向右匹配直到遇到「范围查询」就会停止匹配。也就是范围查询的字段可以用到联合索引，但是在范围查询字段的后面的字段无法用到联合索引。
范围查询有很多种，那到底是哪些范围查询会导致联合索引的最左匹配原则会停止匹配呢？
接下来，举例几个范围查例子。
Q1: select * from t_table where a > 1 and b = 2，联合索引（a, b）哪一个字段用到了联合索引的 B+Tree？
由于联合索引（二级索引）是先按照 a 字段的值排序的，所以符合 a > 1 条件的二级索引记录肯定是相邻，于是在进行索引扫描的时候，可以定位到符合 a > 1 条件的第一条记录，然后沿着记录所在的链表向后扫描，直到某条记录不符合 a > 1 条件位置。所以 a 字段可以在联合索引的 B+Tree 中进行索引查询。
但是在符合 a > 1 条件的二级索引记录的范围里，b 字段的值是无序的。比如前面图的联合索引的 B+ Tree 里，下面这三条记录的 a 字段的值都符合 a > 1 查询条件，而 b 字段的值是无序的：
1. a 字段值为 5 的记录，该记录的 b 字段值为 8；
2. a 字段值为 6 的记录，该记录的 b 字段值为 10；
3. a 字段值为 7 的记录，该记录的 b 字段值为 5；
因此，我们不能根据查询条件 b = 2 来进一步减少需要扫描的记录数量（b 字段无法利用联合索引进行索引查询的意思）。
所以在执行 Q1 这条查询语句的时候，对应的扫描区间是 (2, + ∞)，形成该扫描区间的边界条件是 a > 1，与 b = 2 无关。
因此，Q1 这条查询语句只有 a 字段用到了联合索引进行索引查询，而 b 字段并没有使用到联合索引。
我们也可以在执行计划中的 key_len 知道这一点，在使用联合索引进行查询的时候，通过 key_len 我们可以知道优化器具体使用了多少个字段的搜索条件来形成扫描区间的边界条件。
举例个例子 ，a 和 b 都是 int 类型且不为 NULL 的字段，那么 Q1 这条查询语句执行计划如下，可以看到 key_len 为 4 字节（如果字段允许为 NULL，就在字段类型占用的字节数上加 1，也就是 5 字节），说明只有 a 字段用到了联合索引进行索引查询，而且可以看到，即使 b 字段没用到联合索引，key 为 idx_a_b，说明 Q1 查询语句使用了 idx_a_b 联合索引。
通过 Q1 查询语句我们可以知道，a 字段使用了 > 进行范围查询，联合索引的最左匹配原则在遇到 a 字段的范围查询（ >）后就停止匹配了，因此 b 字段并没有使用到联合索引。















## 锁


