# Contributing Guide

Language: [中文](CONTRIBUTING.md) | English

Thank you for your interest in contributing to this project! By reading this document, you will learn of what you can do to contribute, how to make contributions and other things you need to know before contributing.

This project needs your help in these aspects:

* Check all documents for spelling and grammar mistakes, wrong or missing information, and things to improve.
* Check if there is any code that needs improvement or has bugs.
* Suggest new features.
* Try resolving issues in [Issues](https://github.com/shniubobo/text2beep/issues).

## How to contribute

If you find any problem about this project, you may open a new issue in [Issues](https://github.com/shniubobo/text2beep/issues) and:

* Before doing so, search all existing issues, open or closed, to see if anyone else has already pointed out the same issue.
* Describe the problem you've found in detail (see below).
* If you are able to solve the issue, or if you have some ideas about it, you may also describe the solution in you issue or make a pull request after opening the issue.

### How to report a bug

Please include at least the information below when creating an issue:

* What did you do?
* What did you expect to see?
* What happened actually?
* The version of the program you are using (to get it, type `text2beep --version`).
* The version of Python you are using and your operating system.

### How to suggest a new feature

First you need to know that this project is just a simple CLI tool, far less featured than a professional music-making software or synthesizer. But if you think the feature you are suggesting is within this project's reach, please:

* Describe the feature in detail.
* Explain why this feature needs to be added.

### How to make a pull request

Before making a pull request, it is recommended that you open an issue to describe the problem in detail, which makes it easier to track issues and prevents duplicate contribution.

To make a pull request, you need to:

1. Click the "Fork" button at the top right corner of the page to create a fork of the repository.

2. Download the repository you just forked:

   ```
   git clone url_of_your_repo
   ```

   To get the URL of your repository, click the green "Code" button on the webpage and copy the URL it displays.

3. Enter the repository you've downloaded, install the development requirements, and create a new branch:

   ```
   cd text2beep
   pip install -e .[dev] -U
   git checkout -b name_of_the_branch
   ```

4. Then make your modifications and:

   ```
   git add files_to_commit
   git commit
   ```

   Then type your commit message in the editor that pops up. **As for the commit message, see below for details**.

5. Then push the commits you made to the repository you've forked:

   ```
   git push -u origin name_of_the_branch
   ```

6. Enter the Github page of your repository, and you will find that a section in yellow reminds you to make a PR. Do as instructed to merge your commits into this project's `master` branch, and describe briefly the modifications you've made. If there is any related issue, please also reference it using `#issue_number`.

And I'll be able to see your PR and respond to it. Thank you for your contribution!

## Other things you need to know

Before contributing to this project, you also need to know these things.

### Commit message

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). All commits that don't follow it will be rejected.

This project uses the following types:

* `fix`: When bugs in the code are fixed.
* `feat`: When new features are added.
* `refactor`: When modifications to the code don't change the actual behavior of it.
* `style`: When modifications to the code affect only code style without changing the code's meaning.
* `test`: When tests are added or modified.
* `ci`: When modifications about CI/CD are made.
* `docs`: When only modifications to documents are made.
* `chore`: When modifications belonging to none of the types above are made.

This project uses the following scopes (optional):

* The name of each module. For example, `core`, `version`, etc.

Please make the commit title's first letter capital. For example, `fix: Fix xxx`.

When making breaking changes (i.e. backward-incompatible modifications that affect the program's usage), please add an exclamation mark after the type, say, `feat!:`, and specify `BREAKING CHANGE:` in the commit body.

If your commits fix an issue, please close the related issues with [keywords](https://docs.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword). For example, `Fix #1`.

### Miscellanea

* When in question, feel free to communicate by commenting in issues and pull requests, or opening a new issue.

Finally, thanks again for your willingness of contributing to the project!
