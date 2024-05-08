# GIT

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
