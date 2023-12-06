# use-external-tutorial-jp

Japanese tutorial for using external files.

This repo is written in Japanese.

---

　**重要！**　このファイルに限らず、`README`という名前のファイルがあったらまず最初に開いて読む癖をつけましょう。
`README`にはユーザーに知ってほしいことを書くことになっています。これは世界共通ですので覚えておきましょう。

このファイルはマークダウンという形式のファイルです（拡張子".md"）。
マークダウンファイルは簡単な文体修飾機能をつけたテキストファイルの様なものです。
めちゃ簡単で、メモアプリからブログまで広く使われているので初めましての方は勉強だと思ってまずは以下のウェブサイトを開いて読んでみましょう。

[マークダウンの基本：https://tracpath.com/works/development/markdown_basics/](https://tracpath.com/works/development/markdown_basics/)


## はじめに

このリポジトリは、初心者を対象としています。

プログラミングを学習中に、外部ファイルに関連した操作でつまずくケースが意外と多いみたいです。

- ファイルの読み込み、書き込み
- 関数やクラスの呼び出し

そこで、外部ファイルを扱う際の基本的な操作をまとめました。

言語によって思想の違いはありますが、基本的な操作は共通しています。

その他にも個人的に便利だと思ったスニペットもいれています。


## 基本

### 環境依存の絶対パスの禁止

- 無目的な**絶対パスのハードコードは悪です。** ファイルを別の場所に移動するだけで全く動作しなくなります。

```python

# hoge.txtの場所を指定するときにこーゆーの書いたらダメ
# hoge.txtを移動したり、違うPCを使うとコードが動かない
file_pass = "C:\scripts\example_files\hoge.txt"

```

明確な理由がある場合を除いて

1. **スクリプト自身の絶対パスを動的に取得したうえで**
2. **相対パスを使って他ファイルを参照すること**（下記参照）。

繰り返すが、間違っても絶対パスをハードコードするな。

注意点

- 相対パスを使うためにはコードとともに、関連するファイルを全てひとつのプロジェクトフォルダーの中に格納して必ずフォルダーごと移動するようにしてください。
- パス区切り文字はWindows(バックスラッシュ：`\`)とUNIX系(スラッシュ：`/`)で異なるので注意してください。MATLABとRではOSに関わらず普通のスラッシュ(`/`)を、Pythonは互換性がないので`os.path.join`を使って下さい。
- 以下はプロジェクトディレクトリ内にある"hoge.txt"というファイルのパスを取得する場面を想定したプログラムの例をPython,MATLAB,Rで示したものです。

**重要**
ジュピターノートブックの場合はファイルのパスを取得する手段は無い。コーディングの際は他人にわかりやすいように十分に注意すること。Do NOT change directory in Jupyter notebook.


### 開発環境の再現性

最低限の環境の再現性を担保しましょう。

READMEの環境欄には最低限、必ず以下の情報を書きましょう。

|||
|-|-|
| OS | 例：Windows 10/MacOS 12/Ubuntu 22.04など |
| アーキテクチャ | 例：x86_64/ARM64/ARM32など |
| 言語のバージョン | 例：Python 3.10/R 4.2/MATLAB R2022bなど |
| ハードウェア要件 | 必要に応じて記載する、特に実験プログラムは詳細な記述が必要 |
| 開発環境の環境ファイル | 下記参照 |

- パッケージの依存関係(どのパッケージのどのバージョンが必要か)を人力で解決するのはヒューマンエラーのもとです。
- 特にPythonの場合は仮想環境を多用するので、開発環境の情報をひとつのファイルにしてすぐに他のマシンに環境のクローンを移植できるようになっています。このファイルを環境ファイルと言います。
- 環境ファイルもしくは開発環境の詳細を記載したファイルを作り、プロジェクトディレクトリの中のどこかに必ず添付したうえでREADMEに必ず明記しておきましょう。

**開発環境がシビアな場合はDockerコンテナの利用を！**


## Python

以下のファイルを参照してください。

**/python/example.ipynb**

- Pythonは環境ファイルを必ず出力しておくこと。
  - venv    : "requirements.txt"
  - Anaconda: "(環境名).yml"

```bash
# install jupyter notebook kernel
pip install ipykernel
```

```python
## python #####
import os

# 推奨される書き方
file_name = "hoge.txt"
home_dir  = os.path.dirname(__file__)         #この.pyファイルが存在するディレクトリのパスを取得
file_pass = os.path.join(home_dir, file_name) #hoge.txtのフルパス

# singleton false vs falsity
if not []:
   print("this will be printed")
if [] is False:
   print("this won't")

# ディレクトリ操作
curr_dir = os.getcwd() #カレントディレクトリ取得
os.chdir('..')        #一つ上のフォルダに移動

# 以下のように具体的にパスを書くのはダメ
file_pass = "C:\scripts\example_files\hoge.txt"
file_pass = "/scripts/example-files/hoge.txt"

```

## MATLAB/Octave

- MATLABは環境ファイルが無い。
- 関数`ver`を実行すると環境に関する情報の一覧が表示されるのでそれをtxtファイル等に保存しておくこと。

```matlab
%% MATLAB %%%%%
clear

% 推奨される書き方
fileName = "hoge.txt";
homeDir  = fileparts(mfilename('fullpath')); %この.mファイルが存在するディレクトリのパスを取得
filePass = fullfile(homeDir, fileName);      %hoge.txtのフルパス

% ディレクトリ操作
currDir = pwd; %カレントディレクトリ取得
cd ../         %一つ上のフォルダに移動

% 以下のように具体的にパスを書くのはダメ
filePass = "C:\scripts\example_files\hoge.txt"
filePass = "/scripts/example-files/hoge.txt"

```

## R

- Rは環境ファイルが無い。
- 関数`sessionInfo()`を実行すると環境に関する情報の一覧が表示されるのでそれをtxtファイル等に保存しておくこと。


```R
# install Rmarkdown package
install.packages("rmarkdown")
```

```R
## R #####
rm(list = ls())

# 推奨される書き方
file_name <- "hoge.txt"
if(rstudioapi::isAvailable()==TRUE){
    #この.Rファイルが存在するディレクトリのパスを取得
    home_dir <- dirmane(rstudioapi::getActiveDocumentContext()$path)
} else {
    home_dir <- getSrcDirectory()[1] #RStudioでない場合
}
file_pass <- c(home_dir, file_name)  #hoge.txtのフルパス

# ディレクトリ操作
curr_dir <- getwd() #カレントディレクトリ取得
setwd('../')        #一つ上のフォルダに移動

# 以下のように具体的にパスを書くのはダメ
file_pass <- "C:\scripts\example_files\hoge.txt"
file_pass <- "/scripts/example-files/hoge.txt"

```
