# CHaser-Server 高速版

## ソース
chsr_ex.rb

実行方法の例
```sh
bundle exec ruby chsr_ex.rb
```
もしくは
```sh
ruby chsr_ex.rb
```
詳しくは[起動時のパラメータ]を参照してください。


## 変更内容
**Add 2024/7/27 Takashi Ikura**

結果だけを表示するように修正しました。
Waitのパラメタは無効化しています。

## 内容
**CHaser Server on Ruby (unofficial)**

「CHaser」のサーバープログラムです。

Windowsのコマンドプロンプト、Macのコンソールなどで、Rubyがインストールされている環境で動作します。

大元は、https://github.com/t-akisato/CHaser-Server のソースです。

等リポジトリのサーバプログラムは、大元のサーバプログラムに修正を加えたもので、非公式なものです。大会で使用していないと思うので、テストなど個人的に使用してください。クライアントの最終的なプログラムのチェックは大会でも使用するサーバプログラムで行ってください。

## 起動時の注意
bundle install でツールをセットアップしたので、chsr_ex.rb を実行する場合は、以下のように実行する必要があります。

```sh
bundle exec ruby chsr_ex.rb
```

## 起動時のパラメタ

```sh
bundle exec ruby chsr_ex.rb -h
```

で簡単なヘルプが表示されます。

```sh
bundle exec ruby chsr_ex.rb
```

で map_simple.map というマップファイルを読み込んで起動します。マップファイルを指定するには 

```sh
bundle exec ruby chsr_ex.rb -m ファイル名
```

とします。

```sh
bundle exec ruby chsr_ex.rb -w 数字
```

**※wパラメタは無効となっています**

画面表示のウェイトを指定できます（単位は秒）。デフォルトは 0.5 です。

```sh
bundle exec ruby chsr_ex.rb -p [数字]
```

でポーズモードで起動します。指定したターンごとにEnterの入力を待ちます。数字を省略すると1ターン毎になります。

```sh
bundle exec ruby chsr_ex.rb -z
```

で全角モードで起動します。Windowsのコマンドプロンプト以外では表示が崩れるようです。

起動後、ポート2009(COOL)、2010(HOT)にクライアントプログラムを接続して、エンターキーでゲーム開始になります。

## ライセンスなど
公式のサーバーと同一の動作を保証するものではありません。

This software is released under the MIT License, see LICENSE.

（このソフトウェアは、MITライセンスのもとで公開されています。LICENSEを見てください。） 

## 大元のリポジトリ
https://github.com/t-akisato/CHaser-Server

## U-16プログラミングコンテスト上越妙高
http://joetsu.u16procon.org

## 資料ダウンロード・リンク集
http://joetsu.u16procon.org/links

## その他

- コミットのコメントの初期値設定
```sh
git config commit.template commit_temp.txt
```

- Emailとユーザ名の設定(全体に有効)
```sh
git config --global user.name "あなたの名前"
git config --global user.email "あなたのメールアドレス"
```

- Emailとユーザ名の設定(ローカルに有効)
```sh
git config --local user.name "あなたの名前"
git config --local user.email "あなたのメールアドレス"
```

- wingetとは
windows用のパッケージ管理ツールです。
ソフトを簡単にインストールするためのツールです。

- wingetでパッケージの調査

```sh
winget search ruby
``` 

以下のように表示されるので、ID列の名前をinstallの後に続けて記入する
```sh
名前                ID                                   バージョン    一致      ソース
----------------------------------------------------------------------------------------
Ruby Formatter      9NN0RJL0D2NK                         Unknown                 msstore
InstantRuby         9WZDNCRDC1W3                         Unknown                 msstore
EditPlus            ES-Computing.EditPlus                5.7           Tag: ruby winget
RubyMine            JetBrains.RubyMine                   2024.1.4      Tag: ruby winget
RubyMine (EAP)      JetBrains.RubyMine.EAP               242.20224.102 Tag: ruby winget
Laragon             LeNgocKhoa.Laragon                   6.0.0         Tag: ruby winget
MAMP & MAMP PRO     MAMP.MAMP                            5.0.5         Tag: ruby winget
Ruby 2.6            RubyInstallerTeam.Ruby.2.6           2.6.10-1      Tag: ruby winget
Ruby 2.7            RubyInstallerTeam.Ruby.2.7           2.7.6-1       Tag: ruby winget
Ruby 3.0            RubyInstallerTeam.Ruby.3.0           3.0.4-1       Tag: ruby winget
Ruby 3.1            RubyInstallerTeam.Ruby.3.1           3.1.2-1       Tag: ruby winget
Ruby 3.2            RubyInstallerTeam.Ruby.3.2           3.2.1-1       Tag: ruby winget
Ruby 2.6 with MSYS2 RubyInstallerTeam.RubyWithDevKit.2.6 2.6.10-1      Tag: ruby winget
Ruby 2.7 with MSYS2 RubyInstallerTeam.RubyWithDevKit.2.7 2.7.6-1       Tag: ruby winget
Ruby 3.0 with MSYS2 RubyInstallerTeam.RubyWithDevKit.3.0 3.0.4-1       Tag: ruby winget
Ruby 3.1 with MSYS2 RubyInstallerTeam.RubyWithDevKit.3.1 3.1.2-1       Tag: ruby winget
Ruby 3.2 with MSYS2 RubyInstallerTeam.RubyWithDevKit.3.2 3.2.2-1       Tag: ruby winget
```

- wingetでpythonのインストール
```sh
winget install Python.Python.3
```

- wingetでRubyのインストール
```sh
winget install  RubyInstallerTeam.Ruby.3.2
```
## サーバソフトが起動しているけれど、クライアントプログラムで接続できない場合
コマンドラインで以下のコマンドを実行する
```
netstat -ano | findstr :2009
```
実行すると以下のような結果が表示される場合がある
```
  TCP         0.0.0.0:2009           0.0.0.0:0              LISTENING       9184
  TCP         [::]:2009              [::]:0                 LISTENING       9184
```
以下の部分は、IPv6のIPアドレスに対して2009のポートが開いていることになる

※WindowsでIPv6を無効にしても以下のように表示される。。。なぜ！？
```
[::]:2009
```
これだとクライアントから接続ができない。
コマンドラインで以下のコマンドを実行し、自分のPCのIPv4のIPアドレスを調べて、クライアントでそのIPアドレスを指定する
```
ipconfig
```
実行結果の例
```
Windows IP 構成


Wireless LAN adapter ローカル エリア接続* 9:

   メディアの状態. . . . . . . . . . . .: メディアは接続されていません
   接続固有の DNS サフィックス . . . . .:

Wireless LAN adapter ローカル エリア接続* 10:

   メディアの状態. . . . . . . . . . . .: メディアは接続されていません
   接続固有の DNS サフィックス . . . . .:

イーサネット アダプター イーサネット:

   接続固有の DNS サフィックス . . . . .:
   IPv4 アドレス . . . . . . . . . . . .: 192.168.3.16
   サブネット マスク . . . . . . . . . .: 255.255.255.0
   デフォルト ゲートウェイ . . . . . . .: 192.168.3.1
```
IPv4アドレスとして表示されているIPが対象のIPアドレス（192.168.3.16）
このIPアドレスはPCによって異なります。
サーバソフトだと、ローカルIPのところに「169.254.232.254」などと表示されているかもしれないが、これは正しくない。サーバソフトのプログラムに記載されている初期値かもしれない。