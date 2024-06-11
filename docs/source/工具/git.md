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

  feat：一项新功能
  fix：错误修复
  docs：仅更改文档
  style：不影响代码含义的更改（空格、格式、缺少分号等）
  defactor：既不修复错误也不添加功能的代码更改
  perf：提高性能的代码更改
  test：添加缺少的测试
  build：对构建/编译/打包过程或辅助工具（例如文档生成）的更改
  ci：持续集成/交付设置的变化

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
### 已提交,未推送
执行完commit之后，会在仓库中生成一个版本号(hash值)，标志这次提交。之后任何时候，都可以借助这个hash值回退到这次提交。
git diff <branch-name1> <branch-name2> # 比较2个分支之间的差异
git diff master origin/master # 查看本地仓库与本地远程仓库的差异
git reset --hard origin/master # 回退与本地远程仓库一致
git reset --hard HEAD^ # 回退到本地仓库上一个版本
git reset --hard <hash code> # 回退到任意版本
git reset --soft/git reset # 回退且回到已修改状态，修改仍保留在工作区中。
### 已推送到远程
git push -f orgin master # 强制覆盖远程分支
git push -f # 如果之前已经用 -u 关联过，则可省略分支名
## 4.3  其它常用命令
### 关联远程仓库
- 如果还没有Git仓库，你需要
git init
- 如果你想关联远程仓库
git remote add <name> <git-repo-url>
例如 git remote add origin https://github.com/xxxxxx # 是远程仓库的名称，通常为 origin
- 如果你想关联多个远程仓库
git remote add <name> <another-git-repo-url>
例如 git remote add coding https://coding.net/xxxxxx
- 忘了关联了哪些仓库或者地址
git remote -v
origin https://github.com/gzdaijie/koa-react-server-render-blog.git (fetch)
origin https://github.com/gzdaijie/koa-react-server-render-blog.git (push)
- 如果远程有仓库，你需要clone到本地
git clone <git-repo-url>
关联的远程仓库将被命名为origin，这是默认的。
- 如果你想把别人仓库的地址改为自己的
git remote set-url origin <your-git-url>
### 切换分支
新建仓库后，默认生成了master分支
- 如果你想新建分支并切换
git checkout -b <new-branch-name>
例如 git checkout -b dev
如果仅新建，不切换，则去掉参数 -b
- 看看当前有哪些分支
git branch
- 看看当前本地&远程有哪些分支
git branch -a
- 切换到现有的分支
git checkout master
- 你想把dev分支合并到master分支
git merge <branch-name>
- 你想把本地master分支推送到远程去
git push origin master
- 远程分支被别人更新了，你需要更新代码
git pull origin <branch-name>
- 本地有修改，能不能先git pull
git stash # 工作区修改暂存
git pull  # 更新分支
git stash pop # 暂存修改恢复到工作区
### 撤销操作
- 恢复暂存区文件到工作区
git checkout <file-name>
- 恢复暂存区的所有文件到工作区
git checkout .
- 重置暂存区的某文件，与上一次commit保持一致，但工作区不变
git reset <file-name>
- 重置暂存区与工作区，与上一次commit保持一致
git reset --hard <file-name>
如果是回退版本(commit)，那么file，变成commit的hash码就好了。
- 去掉某个commit
git revert <commit-hash>
实质是新建了一个与原来完全相反的commit，抵消了原来commit的效果
- reset回退错误恢复
git reflog #查看最近操作记录
git reset --hard HEAD{5} #恢复到前五笔操作
git pull origin backend-log #再次拉取代码
### 版本回退与前进
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
git reset --hard <hash>
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
## 4.4 配置Git
- 看看当前的配置
git config --list
- 估计你需要配置你的名字
git config --global user.name "<name>"
--global为可选参数，该参数表示配置全局信息
- 希望别人看到你的commit可以联系到你
git config --global user.email "<email address>"
- 有些命令很长，能不能简化一下
git config --global alias.logg "log --graph --decorate --abbrev-commit --all"
