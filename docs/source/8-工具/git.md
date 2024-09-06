# git

参考

[https://gist.github.com/abravalheri/34aeb7b18d61392251a2]()

## 1.提交规范

### 1.1 目标

- 允许通过脚本生成CHANGELOG.md
- 允许忽略git bisect的提交(不重要的提交，如格式化)
- 浏览历史记录时提供更好的信息

### 1.2 动机

考虑以下提交消息：

- 修复评论剥离
- 修复损坏的链接
- 一点重构
- 检查链接是否存在并抛出异常
- 修复站点地图包含（在区分大小写的Linux上工作）
- 修复文档小部件中的小拼写错误
- 修复场景的测试
- 文档-各种文档修复
- 文档-剥离额外的新行
- 从Google获取文本时将双换行符替换为单换行符
- 添加了对文档中属性的支持

一方面，查看前 5 条消息不可能确定代码的哪一部分发生了更改。 （其余消息尝试指定更改位置，但它们不共享任何约定......）

另一方面，引入格式更改（添加/删除空格/空行、缩进）、缺少分号、注释等的提交对于调试代码或记录更改来说并不有趣，因为它们内部没有逻辑更改。

虽然可以通过检查哪些文件已更改并执行一些比较来找到更多信息，但在查看 git 历史记录时这是不切实际的。

结构约定可以通过允许过滤来加速这一过程。例如，当二等分时，您可以通过执行以下操作来忽略文件：

`git bisect Skip $( git rev-list --grep irrelevant <好地方> HEAD )`

### 1.3 提议

#### 1.3.1 提交格式

```
<type>(<scope>): <subject> <meta>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

提交消息的第一行不应超过 72 个字符，所有其他行最多应有 100 个字符！这使得该消息在 Github 以及各种 git 工具中更容易阅读。

可以以纯文本形式读取的标记（例如 markdown、reST 等）的使用，特别是在正文和页脚中是可选的，但在自动生成变更日志时很有用。

- 允许 `<type>`

`<type>`根据项目的性质，提交消息的 应该是从本体中提取的单个单词或缩写。本文档指定了一个 **编程本体** ，具有以下元素：

- feat：一项新功能
- fix：错误修复
- docs：仅更改文档
- style：不影响代码含义的更改（空格、格式、缺少分号等）
- refactor：既不修复错误也不添加功能的代码更改
- perf：提高性能的代码更改
- test：添加缺少的测试
- build：对构建/编译/打包过程或辅助工具（例如文档生成）的更改
- ci：持续集成/交付设置的变化

如果项目决定使用不同的本体，则需要在其贡献指南（通常是 `CONTRIBUTING.md`项目根目录中的文件）中指定，或者通过在本文档中包含文本的修改副本来替换上面列出，或通过链接此文档并提供替换类型列表。示例文本：

书籍写作项目本体的一个例子是：**拼写错误** 、  **重组** 、 **写入** 、**移动**等……

- 允许 `<scope>（可选）`

通常，准确提及代码库的哪一部分发生了更改是很方便的。令牌 `<scope>`负责提供该信息。例如，假设网络服务器通过 Facebook 引入 OAuth 登录，则有效的提交消息将是：

`feat(auth): introduce sign in via Facebook`

请注意，这里 `auth`可能指的是概念性架构组件，甚至是存储库中文件的基本名称。虽然范围的粒度可能会有所不同，但它成为项目中所说的“通用语言”的一部分很重要。

请注意，在某些情况下，范围自然*过于广泛* ，因此不值得一提。这种特殊情况的示例：

`docs: replace old website URL    `

`refactor: move folder structure to src directory layout`

- 允许 `<subject>`文本
  主题行应包含更改的简洁描述。

* [X] 使用命令式、现在时：“change”而不是“changed”或“changes”
* [X] 不要将第一个字母大写
* [X] 末尾没有点 (.)

- 允许 `<meta>`(可选)
  此外，主题行的末尾可能包含*主题标签* ，以方便更改日志的生成和分割。

* [X] #wip- 向贡献者表明正在实施的功能尚未完成。不应包含在变更日志中（只有功能的最后一次提交才会写入变更日志）。
* [X] #irrelevant- 提交没有添加有用的信息。在修复拼写错误等时使用...不应包含在变更日志中。

- 消息页脚
  **重大变化**:所有重大变更都必须在页脚中提及，并附上变更说明、理由和迁移说明
  **参考问题**：已关闭的错误应在页脚中的单独行中列出，并以“Closes”关键字为前缀，如下所示：
  Closes #234
  或者如果出现多个问题：
  Closes #123, #245, #992

### 1.4 恢复

如果提交恢复了先前的提交，则应以 revert: 开头，后跟恢复的提交的标头。在正文中应该显示：This reverts commit .，其中哈希是要还原的提交的 SHA。

### 1.5 例子

```
feat($browser): add onUrlChange event (popstate/hashchange/polling)
New $browser event:
- forward popstate event if available
- forward hashchange event if popstate not available
- do polling when neither popstate nor hashchange available
Breaks $browser.onHashChange, which was removed (use onUrlChange instead)
```

```
fix($compile): add unit tests for IE9

Older IEs serialize html uppercased, but IE9 does not...
Would be better to expect case insensitive, unfortunately jasmine does
not allow to user regexps for throw expectations.
Closes #392
Breaks foo.bar api, foo.baz should be used instead
```

```
feat(directive): add directives disabled/checked/multiple/readonly/selected

New directives for proper binding these attributes in older browsers (IE).
Added coresponding description, live examples and e2e tests.

Closes #351
```

```
style($location): add couple of missing semi colons
```

```
docs(guide): update fixed docs from Google Docs

Couple of typos fixed:
- indentation
- batchLogbatchLog -> batchLog
- start periodic checking
- missing brace
```

```
feat($compile): simplify isolate scope bindings

Change the isolate scope binding options to:
  - @attr - attribute binding (including interpolation)
  - =model - by-directional model binding
  - &expr - expression execution binding

This change simplifies the terminology as well as
number of choices available to the developer. It
also supports local name aliasing from the parent.

BREAKING CHANGE: isolate scope bindings definition has changed and
the inject option for the directive controller injection was removed.

To migrate the code follow the example below:

Before:

   scope: {
     myAttr: 'attribute',
     myBind: 'bind',
     myExpression: 'expression',
     myEval: 'evaluate',
     myAccessor: 'accessor'
   }

After:

   scope: {
     myAttr: '@',
     myBind: '@',
     myExpression: '&',
     // myEval - usually not useful, but in cases where the expression is assignable, you can use '='
     myAccessor: '=' // in directive's template change myAccessor() to myAccessor
   }

The removed `inject` wasn't generaly useful for directives so there should be no code using it.
```

## 2.生成CHANGELOG.md

变更日志可能包含三个部分：新功能、错误修复、重大变更。该列表可以在发布时由脚本生成，以及相关提交的链接。当然，您可以在实际发布之前编辑此更改日志，但它可以生成框架。
自上次发布以来所有主题的列表（提交消息中的第一行）：

```shell
git log <最后一个标签> HEAD --pretty=format:%s
```

此版本中的新功能

```shell
git log <最新版本> HEAD --grep feat
```

## 3.在线学习网站

[git在线学习](https://learngitbranching.js.org/?locale=zh_CN)
[git在线学习实验](https://juejin.cn/post/7133051740772892685?from=search-suggest)

## 4.Git常用

### 4.1  代码提交和同步代码

![代码提交和同步代码](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/代码提交和同步代码.png)

- 第零步: 工作区与仓库保持一致
- 第一步: 文件增删改，变为已修改状态
- 第二步: git add ，变为已暂存状态

```shell
git status
git add --all # 当前项目下所有的修改
git add .     # 当前目录下所有的修改
git add xx/xx.py xx/xx2.py  # 添加某几个文件
```

- 第三步: git commit，变为已提交状态

```
git commit -m"<这里写commit的描述>"

```

第四步: git push，变为已推送状态

```
git push -u origin master # 第一次需要关联上
git push # 之后再推送就不用指明应该推送的远程分支了
git branch # 可以查看本地仓库的分支
git branch -a # 可以查看本地仓库和本地远程仓库(远程仓库的本地镜像)的所有分支
```

### 4.2  代码撤销和撤销同步

![代码撤销和撤销同步](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/代码撤销和撤销同步.png)

#### 已修改，但未暂存

git diff # 列出所有的修改
git diff xx/xx.py xx/xx2.py # 列出某(几)个文件的修改
git checkout . # 撤销当前文件夹下所有的修改
git checkout xx/xx.py xx/xx2.py # 撤销某几个文件的修改
git clean -f # untracked状态，撤销新增的文件
git clean -df # untracked状态，撤销新增的文件和文件夹

#### 已暂存,未提交

这个时候已经执行过git add，但未执行git commit，但是用git diff已经看不到任何修改。 因为git diff检查的是工作区与暂存区之间的差异。
git diff --cached # 这个命令显示暂存区和本地仓库的差异
git reset # 暂存区的修改恢复到工作区
git reset --soft # 与git reset等价，回到已修改状态，修改的内容仍然在工作区中
git reset --hard # 回到未修改状态，清空暂存区和工作区

#### 已提交,未推送

执行完commit之后，会在仓库中生成一个版本号(hash值)，标志这次提交。之后任何时候，都可以借助这个hash值回退到这次提交。
git diff `<branch-name1>` `<branch-name2>` # 比较2个分支之间的差异
git diff master origin/master # 查看本地仓库与本地远程仓库的差异
git reset --hard origin/master # 回退与本地远程仓库一致
git reset --hard HEAD^ # 回退到本地仓库上一个版本
git reset --hard `<hash code>` # 回退到任意版本
git reset --soft/git reset # 回退且回到已修改状态，修改仍保留在工作区中。

#### 已推送到远程

git push -f orgin master # 强制覆盖远程分支
git push -f # 如果之前已经用 -u 关联过，则可省略分支名

### 4.3  相对引用

在Git 中，git checkout 命令用于切换分支或还原文件到不同的状态。相对引用是一种在 git checkout 命令中使用的方式，它可以让你基于相对位置来引用分支、提交或文件状态。

- 相对于当前分支
- git checkout HEAD：切换到当前分支的最新提交状态
- 相对于其他分支
- git checkout branchName~3：切换到名为 branchName 分支的倒数第三个提交状态
- 相对于提交哈希值
- git checkout commitHash~1
- 相对于文件状态
- git checkout HEAD~2 \-\- filename
  使用相对引用最多的就是移动分支。可以直接使用 -f 选项让分支指向另一个提交
  git branch -f main HEAD~3
  上面的命令会将 main 分支强制指向 HEAD 的第 3 级 parent 提交。

* `~` 符号主要用于按步数向上移动父链，适用于所有提交。
* `** ^` 符号主要用于选择合并提交的指定父提交，适用于处理合并提交的情况。**
* `**HEAD^2` 表示当前提交的第二个父提交（仅在当前提交是合并提交时有效）**

### 4.4 整理提交记录

开发人员有时会说“我想要把这个提交放到这里, 那个提交放到刚才那个提交的后面”, 而接下来就讲的就是它的实现方式，非常清晰、灵活，还很生动。
cherry-pick 可以将提交树上任何地方的提交记录取过来追加到 HEAD 上（只要不是 HEAD 上游的提交就没问题）。
git cherry-pick <提交号>
![本地栈式提交](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/本地栈式提交.png)
场景:
来看一个在开发中经常会遇到的情况：我正在解决某个特别棘手的 Bug，为了便于调试而在代码中添加了一些调试命令并向控制台打印了一些信息。
这些调试和打印语句都在它们各自的提交记录里。最后我终于找到了造成这个 Bug 的根本原因，解决掉以后觉得沾沾自喜！
最后就差把 bugFix 分支里的工作合并回 main 分支了。你可以选择通过 fast-forward 快速合并到 main 分支上，但这样的话 main 分支就会包含我这些调试语句了。你肯定不想这样，应该还有更好的方式

### 4.5 合并分支

- 第一种命令
  git merge <被合并对象>
  在 Git 中合并两个分支时会产生一个特殊的提交记录，它有两个 parent 节点。翻译成自然语言相当于：“我要把这两个 parent 节点本身及它们所有的祖先都包含进来。”
  ![分支合并-1](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/分支合并-1.png)
  ![合并分支-2](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/合并分支-2.png)
  ![合并分支-merge](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/合并分支-merge.png)
- 第二种命令
  git rebase <目标分支>
  Rebase 实际上就是取出一系列的提交记录，“复制”它们，然后在另外一个地方逐个的放下去。
  Rebase 的优势就是可以创造更线性的提交历史，这听上去有些难以理解。如果只允许使用 Rebase 的话，代码库的提交历史将会变得异常清晰。
  其中，<目标分支> 是你希望将当前分支的提交应用到的目标分支。git rebase 命令会将当前分支上的提交逐个应用到目标分支上，并将目标分支的最新提交设置为最新的基准点。
  注意:**rebase会将分支上进行的每个提交应用到目标分支上**
  ![rebase-合并提交](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/rebase-合并提交.png)
  ![分支合并-rebase操作-01](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/分支合并-rebase操作-01.png)
  git pull 就是fetch和merge的简写
  git pull --rebase就是fetch和rebase的简写

### 4.6  冲突与合并

在Git中，<<<<<<<, =======, 和 >>>>>>> 是用于标记合并冲突的标记。这些标记出现在合并冲突文件中，帮助你识别和解决合并冲突。

- 合并冲突示例
  假设你在合并两个分支时，某个文件中同一个位置有不同的更改，Git 会插入这些冲突标记，显示两个分支的不同之处：

```plaintext
这是从当前分支 (HEAD) 的更改。
这是从要合并进来的分支的更改。
```

- <<<<<<< HEAD：标记冲突的开始部分，下面的内容是当前分支（通常是 HEAD 分支）中的更改。
- =======：标记冲突的中间部分，分隔当前分支和要合并进来的分支的更改
- >>>>>>> branch-to-merge：标记冲突的结束部分，branch-to-merge 表示要合并进来的分支名，下面的内容是该分支中的更改
  >>>>>>>
  >>>>>>
  >>>>>
  >>>>
  >>>
  >>
  >

#### 解决冲突

解决冲突时，需要手动编辑文件，选择保留哪部分内容，或者进行必要的合并。编辑完成后，移除这些冲突标记并保存文件。然后，添加并提交修改。

```
git add .
git rebase --continue
```

### 4.7  日志查看

git log 用于查看 Git 仓库的提交历史，它显示了每个提交的详细信息，包括提交哈希值、作者、日期、提交消息等。git log 可以帮助你了解项目的演进历史，跟踪每个提交的更改内容。以下是常用的参数，可用于定制 git log 命令的输出：

- --oneline：以简洁的单行格式显示每个提交信息
- --graph：以 ASCII 图形的形式展示分支和合并历史
- --decorate：在提交记录中显示分支和标签的名称
- --author=`<author>`：过滤指定作者的提交记录
- --since=`<date>`：仅显示指定日期之后的提交记录
- --until=`<date>`：仅显示指定日期之前的提交记录
- --grep=`<pattern>`：仅显示提交信息中包含指定模式的提交记录
- --all：显示所有分支的提交记录，而不仅限于当前分支
- --follow：显示某个文件的完整历史，包括文件的重命名
- --stat：在每个提交记录中显示文件的更改统计信息
- --patch 或 -p：显示每个提交记录的详细更改内容
- --abbrev-commit：仅显示部分提交哈希值，而不是完整的哈希值
- --no-merges：不显示合并提交
- --reverse：以相反的顺序显示提交记录，即从最旧到最新
- --pretty=`<format>`：使用指定的输出格式显示提交记录，例如 oneline、short、full 等。
  git reflog 则用于查看 Git 引用日志，它记录了仓库中所有的引用更改历史，包括分支、标签、HEAD 引用等的移动、删除、切换等操作。引用日志是 Git 用来记录引用（包括提交、分支、标签等）的变化历史，即使在提交被删除或分支被移动后，也可以通过引用日志找回丢失的提交或分支。

### 4.8  其它常用命令

#### 删除本地分支和远程分支

- 删除本地分支
  git branch -d `<branch>`
- 删除远程分支
  git push origin -delete `<branch>`

#### 关联远程仓库

- 如果还没有Git仓库，你需要
  git init
- 如果你想关联远程仓库
  git remote add `<name>` `<git-repo-url>`
  例如 git remote add origin https://github.com/xxxxxx # 是远程仓库的名称，通常为 origin
- 如果你想关联多个远程仓库
  git remote add `<name>` `<another-git-repo-url>`
  例如 git remote add coding https://coding.net/xxxxxx
- 忘了关联了哪些仓库或者地址
  git remote -v
  origin https://github.com/gzdaijie/koa-react-server-render-blog.git (fetch)
  origin https://github.com/gzdaijie/koa-react-server-render-blog.git (push)
- 如果远程有仓库，你需要clone到本地
  git clone `<git-repo-url>`
  关联的远程仓库将被命名为origin，这是默认的。
- 如果你想把别人仓库的地址改为自己的
  git remote set-url origin `<your-git-url>`

#### 切换分支

新建仓库后，默认生成了master分支

- 如果你想新建分支并切换
  git checkout -b `<new-branch-name>`
  例如 git checkout -b dev
  如果仅新建，不切换，则去掉参数 -b
- 看看当前有哪些分支
  git branch
- 看看当前本地&远程有哪些分支
  git branch -a
- 切换到现有的分支
  git checkout master
- 你想把dev分支合并到master分支
  git merge `<branch-name>`
- 你想把本地master分支推送到远程去
  git push origin master
- 远程分支被别人更新了，你需要更新代码
  git pull origin `<branch-name>`
- 本地有修改，能不能先git pull
  git stash # 工作区修改暂存
  git pull  # 更新分支
  git stash pop # 暂存修改恢复到工作区

#### 撤销操作

- 恢复暂存区文件到工作区
  git checkout `<file-name>`
- 恢复暂存区的所有文件到工作区
  git checkout .
- 重置暂存区的某文件，与上一次commit保持一致，但工作区不变
  git reset `<file-name>`
- 重置暂存区与工作区，与上一次commit保持一致
  git reset --hard `<file-name>`
  如果是回退版本(commit)，那么file，变成commit的hash码就好了。
- 去掉某个commit
  git revert `<commit-hash>`
  实质是新建了一个与原来完全相反的commit，抵消了原来commit的效果
- reset回退错误恢复
  git reflog #查看最近操作记录
  git reset --hard HEAD{5} #恢复到前五笔操作
  git pull origin backend-log #再次拉取代码

#### 版本回退与前进

- 查看历史版本
  git log
- 你可能觉得这样的log不好看，试试这个
  git log --graph --decorate --abbrev-commit --all
- 检出到任意版本
  git checkout a5d88ea
- 远程仓库的版本很新，但是你还是想用老版本覆盖
  git push origin master --force
- 觉得commit太多了? 多个commit合并为1个
  git rebase -i HEAD~4
  这个命令，将最近4个commit合并为1个，HEAD代表当前版本。将进入VIM界面，你可以修改提交信息。推送到远程分支的commit，不建议这样做，多人合作时，通常不建议修改历史。
- 想回退到某一个版本
  git reset --hard `<hash>`
  例如 git reset --hard a3hd73r
  --hard代表丢弃工作区的修改，让工作区与版本代码一模一样，与之对应，--soft参数代表保留工作区的修改。
- 想回退到上一个版本，有没有简便方法?
  git reset --hard HEAD^
- 回退到上上个版本呢?
  git reset --hard HEAD^^
  HEAD^^可以换作具体版本hash值。
- 回退错了，能不能前进呀
  git reflog
  这个命令保留了最近执行的操作及所处的版本，每条命令前的hash值，则是对应版本的hash值。使用上述的git checkout 或者 git reset命令 则可以检出或回退到对应版本。
- 刚才commit信息写错了，可以修改吗
  git commit --amend
- 看看当前状态吧
  git status

### 4.9 配置Git

- 看看当前的配置
  git config --list
- 估计你需要配置你的名字
  git config --global user.name "`<name>`"
  --global为可选参数，该参数表示配置全局信息
- 希望别人看到你的commit可以联系到你
  git config --global user.email "`<email address>`"
- 有些命令很长，能不能简化一下
  git config --global alias.logg "log --graph --decorate --abbrev-commit --all"

## 5. git模型
参照 [git模型](https://www.cnblogs.com/FLY_DREAM/p/17280256.html)

### 版本控制系统核心功能
共享、追溯、回滚、维护

### git的优势
- Git 可以在本地进行提交以支持离线工作；
- Git 可以在本地创建分支并且没有命名空间冲突的问题
- Git 可以让提交通过 Pull Request 的方式进行，不需要所有的开发者都有主仓库的写权限
- Git 在优化性能时选择了合并分支作为主要的性能衡量指标，将合并分支变成了成本非常低的操作以鼓励分支的使用
- Git 通过 SHA-1 哈希来保证仓库中数据的可靠性，通过 SHA-1 就可以对数据进行校验，抵御了来自攻击者的恶意篡改
### 版本管理的挑战
- 如何开始一个Feature的开发，而不影响别的Feature？
- 由于很容易创建新分支，分支多了如何管理，时间久了，如何知道每个分支是干什么的？
- 哪些分支已经合并回了主干？
- 如何进行Release的管理？开始一个Release的时候如何冻结Feature, 如何在Prepare Release的时候，开发人员可以继续开发新的功能？
- 线上代码出Bug了，如何快速修复？而且修复的代码要包含到开发人员的分支以及下一个Release?
### git分支模型
在使用Git管理代码以及多人协作的开发模式下，一个团队甚至一个公司对Git的使用有统一规范的工作流程尤为重要。开发团队遵循统一的规则执行功能开发，问题修复，分支合并，版本迭代及发布等操作，可以使团队合作变得平滑顺畅，项目有序向前推进，我们把组织内这样的工作流程（workflow）称为Git代码分支管理模型。
主流的git代码分支管理模型：
- Git flow
- GitHub flow
- GitLab flow
- TBD flow
#### Git flow
![git-flow](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/git-flow.png)
Git flow存在两个长期的独立分支：主分支master和开发分支develop，
- 主分支: 用于版本发布，主分支的每个版本都是质量稳定和功能齐全的发布版
- 开发分支: 用于日常开发工作，存放最新的开发版代码。当开发分支的代码达到稳定状态并可以发布版本时，代码需要被合并到 master 分支，然后标记上对应的版本标签（tag）
如果需要开发新的功能或者解决代码中的问题，则创建辅助分支来解决问题，辅助分支常用于：
- 功能开发（Feature）
- 版本发布（Release）
- 问题修复（Hotfix）
在辅助分支上的工作完成后，辅助分支将被删除。
Feature分支
目的是开发新模块或新功能以满足客户需求，从develop分支创建，开发结束后只需要合并回develop分支，并不需要合并回master主分支。
Release分支
是用于准备发布的版本分支，从develop分支创建，创建时已经包含了发布所需要的所有功能，所以在这个分支上不再开发新功能，仅对这个预发布版本进行修复问题，创建文档及其他与发布相关的工作，一切就绪后将Release分支合并回master主分支并打上相应的版本号标签（Tag），同时也合并回develop分支。
创建单独的Release分支可以避免在不同发布版本上的工作互相受影响，例如团队A准备发布版本1.0的同时，团队B正在进行版本1.1的功能开发，二者相互独立，不会互相影响。
Hotfix分支
通常用于紧急修复当前发布的版本中出现的严重问题，从发布版本的标签或master主分支创建，问题修复后合并回master主分支并打上新的版本号标签（Tag），同时也合并回develop分支或者正在进行中的Release分支。创建单独的Hotfix分支可以避免打断正在进行中的各项开发工作，客户也不需要等到下一个发布周期才能拿到修复。
优点&缺点
Git flow需要同时维护两个甚至更多分支，Hotfix分支从master创建，Release和Feature分支从develop创建，工作完成后又需要将代码合并回 develop 和 master。
在实际应用中，很多开发者会忘记合并回 develop 或者 master，并且各辅助分支之间互相独立，如果从master上pull代码不够及时，一方面可能造成某个分支长期使用已经过时或者错误的代码，另一方面如果与master相隔较远，合并分支时可能会有大量代码冲突，往往需要花费很多时间来消除代码冲突，并且非常容易出错，影响项目的持续集成。
Git flow的优点在于流程清晰，分支管理严格，适用于发布周期比较长的“版本发布”，发布周期可能是几周，几个月，甚至更长时间。由于保持两个长期分支同步的开销较大，所以Git flow并不适用于快速的“持续发布”，ThoughtWorks还专门将Git flow列为不被推荐的技术，建议彻底停止使用。
综合考虑了开发、测试、新功能开发、临时需求、热修复，理想很丰满，现实很骨干，这一套运行起来实在是太复杂了。
#### GitHub flow
![github-flow](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/github-flow.png)
GitHub flow是由Scott Chacon于2011年提出的代码分支管理模型，这是GitHub官方推荐的开发流程，以快速部署为目标，目前大部分开源项目都遵循这一流程。
Github flow最大的特点是只有一个长期分支，即主分支master，且主分支始终保持可发布状态。从master上创建新分支进行功能开发、问题修复等，这些分支通过pull request将代码合并到master。为了保证主分支的代码质量，master的权限只开放给一部分人。Pull request是请求别人pull你的代码库（repository），也就是把开发分支的代码经过代码评审并通过测试后，让有权限的管理员合并回master。
不过在实际情况中，代码评审不可能检查出提交的代码中的所有问题，所以对于每次提交的代码进行自动化测试，主分支代码的自动化部署尤其重要，自动化测试能在产品部署前及时发现一部分问题，如果产品部署之后发现严重问题，自动化部署可以在最短时间内把产品回滚到上一个版本。
优点&缺点
Github flow的优点在于流程简单灵活，不需要考虑及管理太多的分支，适用于需要快速集成及“持续发布”的项目，这类项目可能需要每天发布一个版本，甚至一天发布多个版本。但是对于应用场景比较复杂的情况，例如：多个环境下的产品部署，多个版本的发布或问题修复，只有一个master便会显得力不从心。
github flow这种方式，要保证高质量，对于贡献者的素质要求很高，换句话说，如果代码贡献者素质不那么高，质量就无法得到保证。
#### Gitlab flow
![gitlab-flow](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/gitlab-flow.png)
GitLab flow是由GitLab 的 CEO Sytse Sijbrandij 于 2014 年正式发布的代码分支管理模型，属于GitHub flow的演进版本。
与GitHub相同之处是也存在一个长期主分支master，从master上创建新分支进行功能开发、问题修复等，结束后合并回master。
与GitHub不同之处是GitLab flow又考虑多环境部署等现实因素，增加production产品分支用于在不同的环境下部署产品，或者从master的稳定版本创建release发布分支用于发布软件。
如果在产品分支或者发布分支发现问题，就从对应版本分支创建修复分支，修复完成之后，GitLab flow遵循 “上游优先” 的合并策略，也就是将代码先合并到 master，再合并到下游的production或release分支。
和Github flow类似，master的修改权限只开放给部分人，开发分支的工作完成后，代码通过merge request（类似于GitHub flow中的pull request）请求有权限的管理员把代码合并（merge）回主分支
#### TBD flow
![TBD-flow](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/TBD-flow.png)
TBD (Trunk-based Development) flow是由Paul Hammant于2013年提出的模型。
TBD flow最大的特点是所有开发都基于主干trunk，不再有长期的开发分支，要求所有的提交尽快回到主干，这样可以共享最新的代码，并且能尽可能地减少合并冲突。如果需要发布版本，可以基于trunk直接生成新的分支用于发布。
TBD flow没有pull或者push request，要求开发人员尽快把代码提交到主干分支，但是TBD flow缺乏严格的流程来保证每一份提交代码的质量，如果一些项目开发人员众多且水平不一，同时工作在主分支上可能会在产品发布时才发现不可预知的问题，
所以TBD flow更适用于需要快速迭代的产品，如果在主干分支上发现问题，可以快速进行修复再合并回主干分支。
#### TBD flow++
![TBD-flow++](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/TBD-flow++.png)
TBD++ flow是Arrus公司软件研发部门从2015年开始一直沿用的Git分支管理模型，产品项目的客户主要是电信级服务运营商，每个国家或地区的需求在主要功能上一致，但在客户定制化方面又存在不少差异，同时项目开发周期较长，整个周期一般在3个月到2年之间，软件产品在项目前期需要有快速的迭代，在项目后期需要有稳定的发布版本。（PS: 前面这些因素是选择该模型的重要考量因素，产品型开发，主线功能大体一致，维护客户多，发布周期固定且稍长）
TBD++ flow以敏捷开发为核心，同时吸收了以上几个主流模型的优点，主要特点如下
- 基于功能的主分支
只存在一个长期的独立分支，即主分支master，主分支上功能齐全，通过自动测试保证基本功能运行正常，因为自动测试覆盖不全面或者手动测试不及时，所以无法保证主分支的每个版本都是质量稳定的发布版，但是可以根据功能的完成程度直接从主分支上创建迭代版本用于针对不同客户或者不同时期的功能演示。基于master开发功能或者修复问题需要用到以下两个辅助分支：
  - Feature分支：为了开发新模块或新功能以满足客户需求，从主分支上创建Feature分支，但是并不要求Feature分支上所有的提交尽快回到主分支，开发完成并且通过代码评审及功能测试后才能合并回master主分支。为了共用主分支上的最新代码以及避免合并代码时解决代码冲突引起的额外开销，在功能开发过程中Feature分支需要始终与master保持同步。
  - Bugfix分支：基于主分支创建Bugfix分支修复主分支上发现的问题，修复完成并且通过代码评审后代码合并回master主分支。
基于主分支的Feature分支和Bugfix分支完成后，开发者直接将代码合并回主分支master，不需要像GitLab或GitHub那样依赖于少数几个有权限的管理员，这是因为如果一个项目中开发人员比较多的话，管理员没办法做到对每部分代码都熟悉或掌握，所以代码质量交由代码评审和功能测试来掌控，合并代码回主分支的操作由开发者自己完成。
**主分支上的新代码有时候可能因为评审或测试不全面而带来新问题，例如破坏其他功能模块，甚至影响整体功能。为了能尽早发现问题，主分支上的每次提交都会触发系统级自动化测试，并且周期性地对主分支进行人工测试。一旦发现问题，主分支的专职配置管理员（Software Configuration Manager，SCM）将根据问题的严重性和紧迫性决定是否需要直接回退引起问题的提交，或者基于master创建bugfix分支进行问题修复。**
- 基于发布的Release分支
Release分支负责对外发布软件产品，每个Release分支也会配备专职版本配置管理员SCM，SCM具有对Release分支的最高管理权限。当master上已经包含了某个发布所需要的所有功能，并且没有已知的严重问题，此时由SCM从主分支上创建Release分支准备系统集成测试，和Git flow相同，在此分支上不再进行新功能的开发，仅在这个分支上进行修复问题，创建文档，客户参数配置及其他与发布相关的工作，这些代码同时也需要合并回master以确保主分支功能的完整性。
在每个Release分支正式发布前可能还需要将主分支上的一部分关键问题的修复选择性地同步（Cherry-pick）到Release分支，这个操作也是由SCM完成。
Release分支上的工作一切就绪并通过系统集成测试后，SCM在Release分支上打上相应的版本号标签（Tag）进行发布，这点和Git flow在主分支上进行发布不同。
软件产品发布之后，如果发现紧急或者严重的问题，此时需要基于版本发布时的Release分支标签创建Hotfix分支来修复此类问题，问题修复后合并回该Release分支以及其他同样需要此修复的Release分支，并打上新的版本号标签（Tag）用于发布，同时代码也需要合并回master以确保主分支的健壮性。
### 选择合适的分支模型
Git代码分支管理模型各具特点，流程只是一个辅助工具，没有最好，只有最合适。
- 如果开发团队规模较小又比较分散，产品发布周期较短(例如:初创公司，或者开发的是一个网站或 Web 应用程序，在一天内可能需要发布多个版本)，可以选择GitHub flow或者GitLab flow；
- 如果开发团队规模较大，产品发布周期较长(例如:团队超过20人，采用了月度或季度发布周期，并且由一个团队负责并行开发多个项目)，可以选择Git flow，发布周期较短可以选择TBD flow；
- 如果开发团队规模大，产品发布周期长，同时对敏捷的要求比较高，可以考虑TBD++ flow。每个组织根据产品、项目、人员的特点找到最合适的模型才是共同的目标。对于某个长期产品的开发和客户版本维护场景，这种分支是比较推荐的。

### 小团队
![小团队分支管理](https://cdn.jsdelivr.net/gh/zysok2023/cloudImg/blogs/picture/小团队分支管理.jpg)
最少有三个长期分支
- master: 用于生产环境部署
- testing: 用于测试环境测试
- dev: 用于日常开发
有一些临时分支
- feature-xxx: 用于增加一个新功能
- hotfix-xxx: 用于修复一个紧急bug
#### 常见任务
增加一个新功能&修复一个紧急bug

```
git checkout -b feature-xxx            # 从dev建立特性分支
git add xxx
git commit -m 'commit comment'
git merge feature-xxx --no-ff
```
测试环境测试代码
```
git merge dev --no-ff             # 把dev分支合并到testing，然后在测试环境拉取并测试，配置管理人员操作
```

生产环境大版本上线
```
git merge testing --no-ff       # 把testing测试好的代码合并到master，运维人员操作
git tag -a v0.1 -m '部署包版本名' # 给大版本命名，打Tag
```




