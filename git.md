---
title: Git Cheatsheet
created: 2017-02-13
updated: 2023-04-18
---

## Fork 仓库的同步与更新

> - https://help.github.com/articles/syncing-a-fork/
> - https://stackoverflow.com/questions/7244321/how-do-i-update-a-github-forked-repository

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

- https://blessing.studio/splitting-a-subfolder-out-into-a-new-git-repository/
- https://help.github.com/articles/splitting-a-subfolder-out-into-a-new-repository/

注意这两种方式都会使得根部目录变换到该文件夹下.

### method 2 (多文件夹)

- https://stackoverflow.com/questions/2982055/detach-many-subdirectories-into-a-new-separate-git-repository?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

```sh
git filter-branch --index-filter 'git rm --cached -qr --ignore-unmatch -- . && git reset -q $GIT_COMMIT -- DIR_A DIR_B' --prune-empty -- --all
```

## 为不同的目录下的仓库 (Repos) 设置不同的 gitconfig

经常会遇到需要为不同的 Git 项目设置不同的 `user` 和 `email`。在 `Git 2.13` 以后
的版本中引入了 `conditional includes`。

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

1. use `gitdir/i` for case-insensitive mode or when you're using
   case-insensitive file sytems (eg. Windows).
2. the last `/` of `/path/to/directory/` can't be missing.
3. For pathname, `~/` is expanded to the value of `$HOME`, and `~user/` to the
   specified user’s home directory. No `env` available.

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

An alternative is to correctly configure your author settings in git config
--global author.(name|email) and then use

    git commit --amend --reset-author --no-edit

If you need to change all of history, see the man page for git filter-branch.

Ref:
https://github.com/k88hudson/git-flight-rules#i-committed-with-the-wrong-name-and-email-configured

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

Refs:

- https://stackoverflow.com/questions/38454532/remove-duplicate-commits-introduced-after-bad-rebases/38457832

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

Use `--single-branch` option to **only clone history leading to tip of the
tag**. This saves a lot of unnecessary code from being cloned.

`--[no-]single-branch`

Clone only the history leading to the tip of a single branch, either specified
by the `--branch` option or the primary branch remote’s `HEAD` points at.
Further fetches into the resulting repository will only update the
remote-tracking branch for the branch this option was used for the initial
cloning. If the `HEAD` at the remote did not point at any branch when
`--single-branch` clone was made, no remote-tracking branch is created.

`--depth <depth>`

Create a **shallow** clone with a history truncated to the specified number of
commits. Implies `--single-branch` unless `--no-single-branch` is given to fetch
the histories near the tips of all branches. If you want to clone submodules
shallowly, also pass `--shallow-submodules`.

Refs:

1. [how-to-git-clone-a-specific-tag](https://stackoverflow.com/questions/20280726/how-to-git-clone-a-specific-tag)
2. [git-clone](https://git-scm.com/docs/git-clone)

## Store username and password in Git

Refs:

1. https://git-scm.com/docs/git-credential-store
2. https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage
3. https://stackoverflow.com/questions/35942754/how-can-i-save-username-and-password-in-git

## Ignore already modified files

```sh
git update-index --assume-unchanged
```

How to ignore changed files (temporarily)

In order to ignore changed files to being listed as modified, you can use the
following git command:

```sh
git update-index --assume-unchanged
```

To revert that ignorance use the following command:

```sh
git update-index --no-assume-unchanged
```

Refs:

1. https://stackoverflow.com/questions/655243/ignore-modified-but-not-committed-files-in-git
2. https://stackoverflow.com/questions/9750606/git-still-shows-files-as-modified-after-adding-to-gitignore

## Only use proxy for certain urls or domains.

Update your `.gitconfig` file:

```
[http "http://my.internalgitserver.com/"]
    proxy = "http://proxy-server"
```

References:

1. [Only use a proxy for certain git urls/domains?](https://stackoverflow.com/questions/16067534/only-use-a-proxy-for-certain-git-urls-domains)
2. [Git Configuration](https://git-scm.com/docs/git-config#Documentation/git-config.txt-httplturlgt)

## Leased force push after rebase

If you safely rebased your branch, but found you were rejuected since commit
tree has been changed.

No need to push forcely with `--force`, just try:

```
git push --force-with-lease
```

References:

1. [Git push rejected after feature branch rebase](https://stackoverflow.com/questions/8939977/git-push-rejected-after-feature-branch-rebase)

## Skip CI after pushing

1. https://docs.gitlab.com/ee/user/project/push_options.html
2. https://devops.stackexchange.com/questions/6809/is-there-a-ci-skip-option-in-gitlab-ci

## Fixup any history commit

在 `gitconfig` 中添加 `fixup` 的 alias

```gitconfig
[alias]
    fixup = "!f() { TARGET=$(git rev-parse \"$1\"); shift; git commit --fixup=$TARGET ${@} && GIT_EDITOR=true git rebase -i --autostash --autosquash $TARGET^; }; f"
```

有了这个 fixup 之后，我们可以非常方便的修改任意提交. 操作步骤：

1. 做修改
2. `git add -u1`
3. git fixup 需要修改的 `commit id`

> **warning**
>
> 所有在 `$TARGET` 之后（当然包括 `$TARGET` 本身）的 commit id 都将被重写.

Refs:

1. [超实用的 Git fixup 神技 – 一键修复任意 commit](https://ttys3.dev/post/git-fixup-amend-for-any-older-commits-quickly/)
2. [GIT FIXUP: --AMEND FOR OLDER COMMITS](https://words.filippo.io/git-fixup-amending-an-older-commit/)

## Serach all related pattern in history

- https://stackoverflow.com/questions/4468361/search-all-of-git-history-for-a-string

## Locally clean up squash-merge

- https://adamj.eu/tech/2022/10/30/git-how-to-clean-up-squash-merged-branches/

## Add an empty commit with forced push to trigger CI jobs.

Sometimes, CI on GitHub or GitLab may stuck in unknown stale status, what you
can do is to forcely push an empty commit to the branch of the PR, which will
re-trigger all the checks you have in CI.

    git commit --amend --no-edit
    git push -f

- [Github pull request - Waiting for status to be reported](https://stackoverflow.com/questions/52200096/github-pull-request-waiting-for-status-to-be-reported)

## Custom git log display

Add your custom alias in `.gitconfig`:

```
[alias]
    sl = log --pretty=tformat:'* %C(auto)%h%C(auto)%d %s%Creset %C(auto,blue)(%an)%Creset - %C(auto)%ad'
```

Inspired by:

- [Tweet status from @goinggodotnet](https://twitter.com/goinggodotnet/status/1594214358623850496)

## Old-school style git cooperation: by email!

> Git ships with built-in tools for collaborating over email. With this guide,
> you'll be contributing to email-driven projects like the Linux kernel,
> PostgreSQL, or even git itself in no time.

- [email + git = <3](https://git-send-email.io/)
- [How to submit a patch by email, 2023 edition](https://peter.eisentraut.org/blog/2023/05/09/how-to-submit-a-patch-by-email-2023-edition)

## Permanently remove files and folders from Git repo

Sometimes you want to remove entire directory from git repo even from history,
try:

```sh
git filter-branch --tree-filter 'rm -rf your-dir' HEAD
```

This will rewrite all history commits, so you need to push forcely

```sh
git push origin --force --all
git push origin --force --tags
```

Refs:

1. [Permanently remove files and folders from Git repo](https://dalibornasevic.com/posts/2-permanently-remove-files-and-folders-from-a-git-repository)

### Remove all your local branches which are remotely deleted

While you're listing your branches by using `git branch -a` or `git show-ref`,
you may find some branches are already deleted on remote, but still exist in
local repo.

From git 1.8.5+, you can use `git fetch --prune` (`git fetch -p`) to remove all
your local branches which are remotely deleted.

You cloud also set this automatically by:

```sh
git config fetch.prune true
# or
git config --global fetch.prune true
```

Ref:

1. [How do you remove an invalid remote branch reference from Git?](https://stackoverflow.com/a/8255687)
