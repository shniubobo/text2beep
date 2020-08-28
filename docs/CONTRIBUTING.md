# 贡献指南

Language: 中文 | [English](CONTRIBUTING_en.md)

非常感谢你愿意为本项目做出贡献！通过阅读本文档，你将会了解到你可以在哪些方面做出贡献，以及做出贡献的方法与注意事项。

本项目在这些方面需要你的帮助：

* 检查所有文档是否有拼写与语法错误，是否有错误或遗漏的信息，是否有需要改进之处。
* 检查代码是否有需要改进之处，是否存在 bug。
* 为项目提出新的特性。
* 尝试解决 [Issues](https://github.com/shniubobo/text2beep/issues) 页面中的问题。

## 如何贡献

如果发现本项目存在任何问题，你可以在 [Issues](https://github.com/shniubobo/text2beep/issues) 页面中创建一个新 issue，并且：

* 在此之前搜索所有开放和已关闭的 issue，看看是否有人已经提出了这一问题。
* 详细地描述你发现的问题（详见下文）。
* 如果你可以解决这一问题，或有一些想法，你可以在 issue 中同时描述解决方法，或在提出问题后发起一个 pull request（有关如何发起 PR， 详见下文）。

### 如何报告 bug

请在创建 issue 时至少包含这些信息：

1. 你做了什么？
2. 你希望得到什么结果？
3. 但实际发生了什么？
4. 你使用的程序版本（通过 `text2beep --version` 获得）。
5. 你使用的 Python 版本以及操作系统。

### 如何请求新的特性

首先要了解到本项目只是一个简单的 CLI 工具，远不及专业的音乐制作软件与合成器来得功能丰富，但如果你认为你想要的功能在本项目力所能及的范围内，请：

1. 详细描述这一功能。
2. 解释为什么需要添加这一功能。

### 如何发起 pull request

在发起 pull request 前，推荐先发起一个 issue，详细描述问题。这样可以方便追踪问题，并防止两个人的贡献撞车。

要发起 PR，你需要：

1. 点击页面右上角的 Fork 按钮，创建一个本仓库的 fork。

2. 下载你刚刚 fork 好的仓库：

   ```
   git clone url_of_your_repo
   ```

   要获取你仓库的 URL，点击那个页面上那个绿色的 Code 按钮，然后复制其中显示的 URL。

3. 进入你下载好的仓库，安装开发所需的依赖，然后创建一个新分支：

   ```
   cd text2beep
   pip install -e .[dev] -U
   git checkout -b name_of_the_branch
   ```

4. 然后完成所有更改，并：

   ```
   git add files_to_commit
   git commit
   ```

   然后在自动打开的编辑器里输入提交信息。**有关提交信息，详见下文**。

5. 然后把你刚刚的提交 push 到你 fork 的仓库：

   ```
   git push -u origin name_of_the_branch
   ```

6. 再进入到你的仓库的 Github 页面，你会发现页面上有一栏黄色的字提示你发起 PR。按照提示操作，将你的提交合并进本项目 `master` 分支，并简要地描述你所做的更改。如果有相关的 issue，也请通过 `#issue编号` 的方式引用一下。

然后我就能看到你发起的 PR 并作出回应。感谢你的贡献！

## 注意事项

在为本项目贡献前还需了解以下注意事项。

### 提交信息

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

本项目遵循[约定式提交](https://www.conventionalcommits.org/zh-hans/v1.0.0-beta.4/)，所有不符合要求的提交都会被拒绝合并进 `master` 分支。

本项目使用以下类型：

* `fix`：当修复了代码中的 bug 时。
* `feat`：当增加了新特性时。
* `refactor`：当对代码的修改并没有改变代码的实际行为时。
* `style`：当对代码的修改仅仅影响代码风格，而不影响代码含义时。
* `test`：当新增或修改了测试代码时。
* `ci`：当做出了 CI/CD 方面的更改时。
* `docs`：当仅对文档做出了修改时。
* `chore`：当做出不属于以上任意一类的修改时。

本项目使用以下作用域（非强制添加）：

* 各个模块的名称，如 `core`、`version` 等。

请在提交标题的第一个单词中使用大写，如 `fix: Fix xxx`。

在做出破坏性更改（即产生了向后不兼容且影响用户使用的更改）时，请在类型后添加感叹号，如 `feat!:`，并在提交正文中注明 `BREAKING CHANGE:`。

如果提交修复了一个 issue，请在脚注中通过[关键字](https://docs.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)关闭对应的 issue，如：`Fix #1`。

### 其他注意事项

* 在 Github 上使用的语言随意，但在填写提交信息与为程序写注释时请使用英文。这样可以保证不会中文的人也能看懂你写了什么。如果无法用英语写注释，请用中文写，我会帮你改为英文。另外，如果可以的话，请尽量在 issue 中也添加一些英文翻译，或直接使用英文，这样可以方便问题的追踪。
* 如果在任何方面有问题，都欢迎在 issue 或 pull request 中发 comment 进行交流，或者新开一个 issue。



最后，再次感谢你愿意为本项目做出贡献！
