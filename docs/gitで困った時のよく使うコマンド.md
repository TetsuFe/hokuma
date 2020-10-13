この記事はあまり網羅的ではないです。実際に自分がよく使うコマンドに絞っています

網羅的なコマンド集を見たい人は以下のサイトがいいと思います（特に、レポジトリ新規作成についてはやったことあると思うので書きません）

「**いまさらだけどGitを基本から分かりやすくまとめてみた」**
2018年08月14日に投稿 2018年10月02日 更新 

[https://qiita.com/gold-kou/items/7f6a3b46e2781b0dd4a0](https://qiita.com/gold-kou/items/7f6a3b46e2781b0dd4a0)

# 目次

- ショートカット
- ターミナルにブランチ名を表示する（mac)
- 個人的によく使うパターン
    - 自分がブランチAで作業中に、ブランチBのレビューを頼まれる
    - コミットしたくないファイルをaddしてしまった
- 0. 基本コマンド
- 1. ブランチ名変える
- 2. ブランチ間を移動したい時
- 3. やり直したいとき
- 4. git stash：一番使うかも
- おまけ（間違ってるかも）
    - 5. git rebaseとcherry-pick
    - 6. その他の戻す系

## ショートカット（~/.gitconfig)

割と自己流多いので、もっといいショートカットあったら教えてください

    [push]
    	default = matching
    [alias]
    	co = checkout
        c = commit -m
        br = branch
        bl = branch --sort committerdate
        ss = status
        cob = checkout -b
        p = !git push origin `git rev-parse --abbrev-ref HEAD`
        pf = !git push -f origin `git rev-parse --abbrev-ref HEAD`
        dc = diff --cached
        d = diff
        rh = reset HEAD
        pl = pull origin 
        plre = pull --rebase
        comemp = commit --allow-empty -m
        logg = log --stat --decorate=short --pretty=format:'%C(yellow)%h %Cgreen%cr %Cblue%cn%Cred%d %Creset%s %C(cyan)%b'
    [user]
    	name = ***
    	email = ***
    [core]
    	excludesfile = /Users/***/.gitignore_global
      quotepath = false
    [difftool "sourcetree"]
    	cmd = opendiff \\"$LOCAL\\" \\"$REMOTE\\"
    	path = 
    [mergetool "sourcetree"]
    	cmd = /Applications/SourceTree.app/Contents/Resources/opendiff-w.sh \\"$LOCAL\\" \\"$REMOTE\\" -ancestor \\"$BASE\\" -merge \\"$MERGED\\"
    	trustExitCode = true
    [commit]
    	template = /Users/***/.stCommitMsg
    [filter "lfs"]
    	clean = git-lfs clean -- %f
    	smudge = git-lfs smudge -- %f
    	process = git-lfs filter-process
    	required = true

## ターミナルにブランチ名を表示する（mac)

あるいは、ブランチ名をtabで補完する方法。

    source /usr/local/etc/bash_completion.d/git-prompt.sh
    source /usr/local/etc/bash_completion.d/git-completion.bash
    GIT_PS1_SHOWDIRTYSTATE=true
    PS1='[\\u@\\h \\W\\[\\e[0;35m\\]$(__git_ps1 " (%s)")\\[\\e[0m\\]]\\$ '

こんな感じで表示されます

[tetsu@satoshinoMacBook-puro hokudai_furima (master)]$

# 個人的によく使うパターン

## 自分がブランチAで作業中に、ブランチBのレビューを頼まれる

- step 1. ブランチBをfetch（ローカルにブランチを取得）
    - コマンド: $ git fetch
- step 2. ブランチを移動できるようにする
    - 一旦自分のブランチのコミットしてないかつtrackedな変更を全てstash（退避）
        - コマンド: git stash
    - 自分のブランチのコミットしてないかつtrackedな変更を全てコミット
        - コマンド: git status # コミットしてないかつtrackedな変更を見つける
        - コマンド: git add ファイル名
        - コマンド: git commit -m "メッセージ"
- step 3. ブランチ移動
    - コマンド: git checkout ブランチB
- step 4. レビュー
- step 5. 元の作業中ブランチに戻る
    - コマンド: git checkout ブランチA（元の作業中ブランチ）
    - コマンド: git stash pop

## コミットしたくないファイルをaddしてしまった

気づくには: $ git push する前に $ git statusする癖をつけよう

- step 1 $ git status
- step 2 $ git reset HEAD #全addの取り消し
- step 3 add, コミットやり直し

# 0. 基本コマンド

$ git status # addされているファイル・変更されているが見れます（意図したファイルが変更されてないか？の確認にも使います）

$ git add -A #またはgit add ファイル名

$ git commit -m "コミットメッセージ"

$ git push origin ***

$ git pull —rebase origin ***

# 1. ブランチ名変える

$ git branch -m 元の名前 新しい名前

カレントブランチの名前を変える場合は以下でもOK

$ git branch -m 新しい名前

# 2. ブランチ間を移動したい時

## 2.1. ブランチを探す

$ git fetch # リモートのブランチを全て取得

$ git branch # ブランチの一覧を表示

$ git branch --sort committerdate # 新しいものが下になるように一覧を表示

## 2.2. 別ブランチに移動する

$ git checkout ブランチ名

ここでエラーがでたら、大体はコミットしていないファイルがある。

$ git stash # 過去に一度でもaddしたことがあって(trackedで）コミットしていないファイルの差分を一時的に退避しておく。$ git stash popや$ git stash list からの $ git stash pop *** から差分を復活できる。

git stashについては [https://qiita.com/fukajun/items/41288806e4733cb9c342](https://qiita.com/fukajun/items/41288806e4733cb9c342) がまあまあよい

基本的に$ git stashをすればcheckoutできるようになる

# 3. やり直したいとき

$ git reset —hard は使わないこと。これをしなければ全てやり直すことができる（でも、使っても大丈夫かもしれない。気になる人は詳しい人に聞いてください）

## add・commitしていない(＝untracked）変更を消す

あんまり使ったことない。$ git stash -u でも代用できる

$ git chekcout . # ファイルを指定することも可
[http://www-creators.com/archives/1290#_add](http://www-creators.com/archives/1290#_add)

## addを取り消す（これよく使う）

$ git reset HEAD ファイル名 # git reset HEAD で全部add取り消し
--softとしなくてもファイルは消えないので安心！（参考：[https://qiita.com/nabezokodaikon/items/7ee4900d28d8d863978e）](https://qiita.com/nabezokodaikon/items/7ee4900d28d8d863978e%EF%BC%89)

## 過去のcommitを削除せず打ち消す

あんまり使ったことないので間違ってるかも。

[http://blog.yukarien.com/tech/post-1502/](http://blog.yukarien.com/tech/post-1502/)

$ git revert コミットID
そのコミットを打ち消すコミットを付け加える（それまでの記録は残る）

## commitを打ち消す

$ git reset --soft コミットID #ファイルはそのままで、ログをコミットIDの状態に戻す

よくある使い方として、

$ git add -A

$ git commit -m "aaa"

間違った！やり直したい

$ git reset —soft HEAD^ # ログはさっきのコミットの前の状態に戻るが、ファイルは変更されたまま

ファイル編集、コミット

また、ログだけでなく、ファイルも以前の状態に戻したい場合は「$ git reset —hard コミットID」 もあるが、これは今までの作業が全部無に帰す可能性があるので自分は禁止している（他人のレポジトリをforkして使ってみたりするときは雑にこれを使うこともある）

# 4. git stash：一番使うかも

一時的に **コミットしていないファイル** を退避させておきたい時、git stashを使います。

これ見てください。

[https://qiita.com/fukajun/items/41288806e4733cb9c342](https://qiita.com/fukajun/items/41288806e4733cb9c342)

ちなみに、untrackedなファイルも退避させたいときは、

$ git stash -u

# おまけ

# 5. git rebaseとcherry-pick

最近あんまり使ってないです。間違ってるかも

cherry-pick: [https://qiita.com/ta__ho/items/8204a22a53b02ee0817e](https://qiita.com/ta__ho/items/8204a22a53b02ee0817e)

rebase: [https://liginc.co.jp/web/tool/79390#m3](https://liginc.co.jp/web/tool/79390#m3)

## コミットを入れ替えたい・別ブランチから一部だけ取り込みたい

$ git co -b 新しいブランチ（一時的な名前）
適当にコミット
$ git cherry-pick develop~番号..develop # 古いブランチ名~遡りたい数..古いブランチ名
$ git br -D 古いブランチ
$ git br -m 新しいブランチ（一時的な名前） 新しいブランチ

## コミットを入れ替える

$ git rebase -i <commit>

## 別のブランチからコミットを取り出す

$ git cherry-pick コミットID

問題なければすぐマージされる

## マージコミットのマージ

$ git cherry-pick -m 1 D

# 6. その他の戻す系

この辺も雑になります

## git resetを取り消す・そのコミットに戻る

[http://yanor.net/wiki/?Git%2Fgit](http://yanor.net/wiki/?Git%2Fgit) reflog （git resetを取り消す）

## ある１ファイルだけ過去のコミットに戻す

$ git checkout [コミット番号] [ファイルパス]

$ git reflog や logでコミットIDを見る
$ git reset --soft コミットID

# git stash dropしたファイルを戻す

$ git fsck --unreachable | awk '/commit/ {print $3}' | xargs git log --merges --no-walk --grep=WIP --all-match
$ git checkout -b コミットID
ブランチ名などをみて、どのブランチから派生したものか確認すると良い

# git stash popできないとき

git merge "stash@{0}"[https://qiita.com/panghea@github/items/42715a87f681802883bc](https://qiita.com/panghea@github/items/42715a87f681802883bc)

## コミットメッセージを変える

$ git commit --amend -m "新しいメッセージ"

## n回前のメッセージを変える

[https://nnsnodnb.hatenablog.jp/entry/how-to-git-rebase](https://nnsnodnb.hatenablog.jp/entry/how-to-git-rebase)

## amendを取り消す

[https://weblike-curtaincall.ssl-lolipop.jp/blog/?p=1435](https://weblike-curtaincall.ssl-lolipop.jp/blog/?p=1435)
$ git reset --soft HEAD@{1}

## コミットの順番を変える

$ git rebase -i HEAD~6

## rebaseを戻す

[https://gist.github.com/naokazuterada/9e45a937f7574ebf91a7](https://gist.github.com/naokazuterada/9e45a937f7574ebf91a7)
$ git reflog
$ git reset --hard 'HEAD@{4}'

## 追跡外のファイルを一括で削除

addしていないファイルを全部やっぱり消したい時に使う

$ git clean -n

git clean の「予行演習」を行うコマンドです。このコマンドを実行すると削除されるファイルを表示しますが、実際の削除は行われません。

$ git clean -f

追跡対象外のファイルをカレントディレクトリから削除するコマンドです。設定オプション clean.requireForce がfalse にセットされていない場合 (このオプションはデフォルトでは true です) は、-f (force) フラグは必須です。このコマンドでは、追跡対象外のフォルダーやファイルであっても .gitignore. で指定したものは削除しません。

## マージでコンフリクトしたからやっぱやめる

$ git merge --abort