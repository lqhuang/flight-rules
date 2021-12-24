---
title: Git cheatsheet
created: 2017-02-13 20:15
---

记录一些常用的相关操作。

## Fork 仓库的同步与更新

> https://help.github.com/articles/syncing-a-fork/ > https://stackoverflow.com/questions/7244321/how-do-i-update-a-github-forked-repository

    In your local clone of your forked repository, you can add the original GitHub repository as a "remote". ("Remotes" are like nicknames for the URLs of repositories - origin is one, for example.) Then you can fetch all the branches from that upstream repository, and rebase your work to continue working on the upstream version. In terms of commands that might look like:

    # Add the remote, call it "upstream":

    git remote add upstream https://github.com/whoever/whatever.git

    # Fetch all the branches of that remote into remote-tracking branches,
    # such as upstream/master:

    git fetch upstream

    # Make sure that you're on your master branch:

    git checkout master

    # Rewrite your master branch so that any commits of yours that
    # aren't already in upstream/master are replayed on top of that
    # other branch:

    git rebase upstream/master
    If you don't want to rewrite the history of your master branch, (for example because other people may have cloned it) then you should replace the last command with git merge upstream/master. However, for making further pull requests that are as clean as possible, it's probably better to rebase.

    If you've rebased your branch onto upstream/master you may need to force the push in order to push it to your own forked repository on GitHub. You'd do that with:

    git push -f origin master
    You only need to use the -f the first time after you've rebased.

## 分离单独文件夹出来成为独立的仓库

### method 1

https://blessing.studio/splitting-a-subfolder-out-into-a-new-git-repository/

https://help.github.com/articles/splitting-a-subfolder-out-into-a-new-repository/

注意这两种方式都会使得根部目录变换到该文件夹下.

### method 2 (多文件夹)

https://stackoverflow.com/questions/2982055/detach-many-subdirectories-into-a-new-separate-git-repository?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

    git filter-branch --index-filter 'git rm --cached -qr --ignore-unmatch -- . && git reset -q $GIT_COMMIT -- DIR_A DIR_B' --prune-empty -- --all

## 为不同的目录下的仓库 (Repos) 设置不同的 gitconfig

经常会遇到需要为不同的 Git 项目设置不同的 `user` 和 `email`。在 `Git 2.13` 以后的版本中引入了 `conditional includes`。

在 `~/.gitconfig` 中添加

```
; include if $GIT_DIR is /path/to/foo/.git
[includeIf "gitdir:/path/to/foo/.git"]
	path = /path/to/foo.inc

; include for all repositories inside /path/to/group
[includeIf "gitdir:/path/to/group/"]
	path = /path/to/foo.inc

; include for all repositories inside $HOME/to/group
[includeIf "gitdir:~/to/group/"]
	path = /path/to/foo.inc

; relative paths are always relative to the including
; file (if the condition is true); their location is not
; affected by the condition
[includeIf "gitdir:/path/to/group/"]
	path = foo.inc

; include only if we are in a worktree where foo-branch is
; currently checked out
[includeIf "onbranch:foo-branch"]
	path = foo.inc
```

You can check that that it works recursively by running `git config --list`.

Hints:

1. use `gitdir/i` for case-insensitive mode or when you're using case-insensitive file sytems (eg. Windows).
2. the last `/` of `/path/to/directory/` can't be missing.
3. For pathname, `~/` is expanded to the value of `$HOME`, and `~user/` to the specified user’s home directory. No `env` available.

Refs:

1. [Can I specify multiple users for myself in .gitconfig?](https://stackoverflow.com/questions/4220416/can-i-specify-multiple-users-for-myself-in-gitconfig)
2. [Conditional includes](https://git-scm.com/docs/git-config#_conditional_includes)

## 修改 commits 里的用户和邮箱

### 最近一次 commit

如果这只是单个提交(commit)，修改它：

    git commit --amend --author "New Authorname <authoremail@mydomain.com>"

如果你需要修改所有历史, 参考 'git filter-branch'的指南页.

If it's a single commit, amend it

    git commit --amend --no-edit --author "New Authorname <authoremail@mydomain.com>"

An alternative is to correctly configure your author settings in git config --global author.(name|email) and then use

    git commit --amend --reset-author --no-edit

If you need to change all of history, see the man page for git filter-branch.

Ref: https://github.com/k88hudson/git-flight-rules#i-committed-with-the-wrong-name-and-email-configured

### 历史提交记录中的 commit

Refs:

1. https://segmentfault.com/q/1010000006999861
2. https://stackoverflow.com/questions/750172/how-to-change-the-author-and-committer-name-and-e-mail-of-multiple-commits-in-gi

## 查看哪些历史提交过文件占用空间较大, 重写 commit，删除大文件

List objects disk usage

```bash
git rev-list --objects --all \
| git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
| awk '/^blob/ {print substr($0,6)}' \
| sort --numeric-sort --key=2 \
| cut --complement --characters=13-40 \
| numfmt --field=2 --to=iec-i --suffix=B --padding=7 --round=nearest
```

Remove file or folder in history commit:

```
git filter-branch -f --index-filter "git rm -rf --cached --ignore-unmatch FOLDERNAME" -- --all
```

Clean up:

```
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --aggressive --prune=now
```

finally, `git push -f` to upload to remote repo.

Refs:

1. https://stackoverflow.com/questions/2100907/how-to-remove-delete-a-large-file-from-commit-history-in-git-repository
2. https://stackoverflow.com/questions/10622179/how-to-find-identify-large-commits-in-git-history/
3. https://www.hollischuang.com/archives/1708

## 重复的 commits

不知道为啥产生的重复 commits

Refs: https://stackoverflow.com/questions/38454532/remove-duplicate-commits-introduced-after-bad-rebases/38457832

## Removing sensitive data from a repository

    bfg --replace-text passwords.txt

Refs:

1. https://help.github.com/en/articles/removing-sensitive-data-from-a-repository
2. https://help.github.com/en/articles/removing-files-from-a-repositorys-history
3. https://rtyley.github.io/bfg-repo-cleaner/

## Fetch a remote branch into a new local branch

Refs:

1. [git-fetch-remote-branch](https://stackoverflow.com/questions/9537392/git-fetch-remote-branch)
2. [git remote](https://www.ruanyifeng.com/blog/2014/06/git_remote.html)

## Git clone specific branch / tags

```shell
git clone <repo_url> --branch <tag_name> [--single-branch] [--depth 1]
```

Use `--single-branch` option to **only clone history leading to tip of the tag**. This saves a lot of unnecessary code from being cloned.

`--[no-]single-branch`

Clone only the history leading to the tip of a single branch, either specified by the `--branch` option or the primary branch remote’s `HEAD` points at. Further fetches into the resulting repository will only update the remote-tracking branch for the branch this option was used for the initial cloning. If the `HEAD` at the remote did not point at any branch when `--single-branch` clone was made, no remote-tracking branch is created.

`--depth <depth>`

Create a **shallow** clone with a history truncated to the specified number of commits. Implies `--single-branch` unless `--no-single-branch` is given to fetch the histories near the tips of all branches. If you want to clone submodules shallowly, also pass `--shallow-submodules`.

Refs:

1. [how-to-git-clone-a-specific-tag](https://stackoverflow.com/questions/20280726/how-to-git-clone-a-specific-tag)
2. [git-clone](https://git-scm.com/docs/git-clone)

