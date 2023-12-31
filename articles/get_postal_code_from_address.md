---
title: "住所から郵便番号を取得するサイトを作ってみた"
emoji: "😉"
type: "idea" # tech: 技術記事 / idea: アイデア
topics: [html, perl, cgi, mysql]
published: true
---
## はじめに
住所から郵便番号を調べられるサイトを作ってみたので自分用のメモを兼ねてここに紹介します。APIを使う方法でもできますが、すでにMariaDBをインストールしていたのでそちらを使う方法でやってみました。また、この記事はChatGPTを駆使して作成しています。記事作成だけでなくhtmlやperlも大半ChatGPTに作ってもらいました。
## MariaDBのインストール
MariaDBはMySQL互換のsqlサーバーです。Windowsにもインストールできると思いますが、Linuxにインストールしました。インストール方法はwebで "MariaDB" "インストール"で検索すれば出てくると思いますが、ChatGPTに聞いてみました。(インストール手順はDebianベースのLinuxです。) 以下はそのコピペです。

MariaDBをDebianベースのリナックスにインストールする手順は以下の通りです。

### システムをアップデート:
最初に、パッケージリストを最新の状態にアップデートします。

```shell
sudo apt update
sudo apt upgrade -y
```
### MariaDBのインストール:
MariaDBをインストールするために以下のコマンドを実行します。
```shell
sudo apt install mariadb-server -y
```
### セキュリティスクリプトの実行:
MariaDBをセキュアに設定するために、mysql_secure_installation スクリプトを実行してください。

```shell
sudo mysql_secure_installation
```
スクリプトを実行すると、以下のような質問が表示されます。

 - Enter current password for root (enter for none): （既存のルートパスワードを入力してください、初回のインストールではパスワードは設定されていないのでそのままEnter）
 - Set root password? [Y/n]: Y
 - New password: （新しいルートパスワードを設定）
 - Re-enter new password: （同じパスワードを再入力）
 - Remove anonymous users? [Y/n]: Y
 - Disallow root login remotely? [Y/n]: Y
 - Remove test database and access to it? [Y/n]: Y
 - Reload privilege tables now? [Y/n]: Y
### MariaDBにログイン:
インストールが完了したら、新しく設定したルートパスワードを使用してMariaDBにログインできます。
```shell
sudo mysql -u root -p
```
ここで、先ほど設定したルートパスワードを入力してログインします。

以上がChatGPTが教えてくれた手順ですが、rootではなく一般ユーザーでログインできるようにしておきましょう。以下、ChatGPTに教えてもらった手順です。

MariaDBにおいて、rootユーザーを使用せずに一般ユーザーを使用するためには、以下の手順で一般ユーザーにデータベースの権限を付与することができます。

### 一般ユーザーの作成:
まず、MariaDBにログインして、新しいユーザーを作成します。

```sql
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
```
### 必要な権限の付与:
新しく作成したユーザーに、データベースへのアクセス権限を付与します。例えば、すべてのデータベースへのフルアクセスを付与する場合は以下のようにします。

```sql
GRANT ALL PRIVILEGES ON *.* TO 'your_username'@'localhost' WITH GRANT OPTION;
```
この例では、すべてのデータベースとテーブルに対してフルアクセス権限を付与しています。必要に応じて、特定のデータベースやテーブルに対する権限のみを付与することも可能です。

### 権限の変更を反映:
権限の変更を反映させるために、次のコマンドを実行します。

```sql
FLUSH PRIVILEGES;
```
### ログアウト:
作業が完了したら、MariaDBからログアウトします。

```sql
EXIT;
```
これで、指定した一般ユーザー（your_usernameとして置き換えてください）はMariaDBにアクセスし、指定された権限でデータベースを操作できるようになります。ユーザー名やパスワード、権限の範囲は、実際のニーズに応じて適切に設定してください。


## 郵便番号databaseの作成
MariaDBをインストールしたら次には郵便番号データベースの作成です。これはまず郵便局のサイトから郵便番号のcsvをダウンロードしてきます。これもWebで"郵便番号" "CSV" "ダウンロード"で検索すればすぐに出てきます。もし出てこないのでしたら[こちら](https://www.post.japanpost.jp/zipcode/dl/utf-zip.html)です。wgetを使ってダウンロードするのでしたら、
```bash
wget https://www.post.japanpost.jp/zipcode/dl/utf/zip/utf_ken_all.zip
```
次にダウンロードしてきたcsvを読込データベースを作成します。これについてもWeb で"郵便番号" "mysql""データベース"で検索すればでてきます。出てこない場合は、[ここ](https://qiita.com/kesuzuki/items/6d6c89a876d7b8ea820c)を見てください。
以下は上のQittaの記事からコピペして作ったコードです。
```sql
create database zipcodedb default character set utf8;
use zipcodedb;

create table zipcode (
 id int unsigned not null auto_increment,
 jiscode varchar(255),
 zipcode_old varchar(255),
 zipcode varchar(255),
 pref_kana varchar(255),
 city_kana varchar(255),
 street_kana varchar(255),
 pref varchar(255),
 city varchar(255),
 street varchar(255),
 flag1 tinyint,
 flag2 tinyint,
 flag3 tinyint,
 flag4 tinyint,
 flag5 tinyint,
 flag6 tinyint,
 primary key (id),
 key zipcode (zipcode)
);

LOAD DATA LOCAL INFILE '/home/your_id/utf_ken_all.csv'
INTO TABLE zipcode
FIELDS
    TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '"'
    ESCAPED BY ''
LINES
    STARTING BY ''
    TERMINATED BY '\r\n'
(
 jiscode,
 zipcode_old,
 zipcode,
 pref_kana,
 city_kana,
 street_kana,
 pref,
 city,
 street,
 flag1,
 flag2,
 flag3,
 flag4,
 flag5,
 flag6
);
```

ここで　/home/your_id/utf_ken_all.csv はダウンロードしてきたファイルの保存場所をフルパスで指定します。このファイルを適当な名前(とりあえずgen_zipdb.sqlにしておきます)を付けて保存し、mysqlにログインします。
```shell
mysql -u yourid -p
```
そこで先ほど作ったgen_zipdb.sqlを読み込みます。
```
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 736
Server version: 10.3.39-MariaDB-0+deb10u1 Raspbian 10

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> source gen_zipdb.sql
```

これでデータベースの作成は完了です。
次にweb serverの導入です。これもChatGPTに聞いてみます。
## Apacheのインストール
以下はDebianベースのインストール手順です。
### パッケージリストを更新:

```bash
sudo apt update
```
### Apache2 パッケージをインストール:

```bash
sudo apt install apache2
```
### Apache サービスのステータスを確認:

```bash
sudo systemctl status apache2
```
### Apache サービスを起動:

```bash
sudo systemctl start apache2
```
### ブート時に Apache サービスを自動起動するように設定:

```bash
sudo systemctl enable apache2
```
インストールが完了したら、ウェブブラウザを開き、http://your_server_ip または http://localhost にアクセスして、Apache のデフォルトのウェルカムページが表示されることを確認してください。

注意: セキュリティの観点から、公開サーバーで Apache を設定する場合は、必要に応じて追加のセキュリティ対策や設定の変更が必要です。

次にcgiをenableにする手順です。これもChatGPTに聞いてみました。
## ApacheでCGIを有効にする

Apache で CGI を有効にするための手順は、Apache の設定ファイルを適切に編集することで行います。

### CGI モジュールを有効にする:

```bash
sudo a2enmod cgi
```
### Apache サービスを再起動:

```bash
sudo systemctl restart apache2
```
### 設定のテスト:
以下のような基本的な CGI スクリプトを作成して、Apache のドキュメントルート（通常は /usr/lib/cgi-bin）に保存します。

```bash
echo -e '#!/bin/bash\necho "Content-type: text/plain"\necho\necho "Hello, CGI!"' | sudo tee /usr/lib/cgi-bin/test.cgi
sudo chmod +x /usr/lib/cgi-bin/test.cgi
```
ウェブブラウザで http://your_server_ip/test.cgi にアクセスします。ページに「Hello, CGI!」と表示されれば、CGI が正しく動作しています。

## Perlのスクリプトを作成
次にperlでcgiのスクリプトを作ります。通常linuxにはperlはinstallされていると思いますが、installされてない場合はaptでインストールできます。
```bash
sudo apt install perl
```
さてperl cgiのコードですが、以下の通りです。

```perl
#!/usr/bin/perl
use strict;
use warnings;
use DBI;
use CGI;

# データベース接続情報
my $db_name = 'zipcodedb';
my $db_user = 'username';   #sqlのusername 適切に変更する事
my $db_password = 'password'; #パスワード適切に変更する事
my $db_host = 'localhost';
my $table_name = 'zipcode';

my $cgi = CGI->new;



my $pref = $cgi->param('pref');
my $city = $cgi->param('city');
my $street = $cgi->param('street');
my $zipcode = "";

# データベースに接続
my $dbh = DBI->connect("DBI:mysql:$db_name:$db_host", $db_user, $db_password)
    or die "Unable to connect to database: $DBI::errstr";

$dbh->do("set names utf8");
my $select_sql = "SELECT zipcode FROM $table_name WHERE pref = '$pref' AND city = '$city' AND street = '$street'";
my $select_sth = $dbh->prepare($select_sql);
my $dummy;
$select_sth->execute();

print "Content-Type: text/html\n\n";
print "<html><head><meta charset=\"UTF-8\"";
print "</head><body><p>";
# SQLクエリの準備と実行
if (my $ar_ref = $select_sth->fetchrow_arrayref) {
    ($zipcode) = @$ar_ref;
    $zipcode =~ s/^(\d{3})(\d{4})$/$1-$2/;
    print "$pref$city$street の郵便番号は、";
    print "$zipcode です。\n";
} else {
    print "見つかりません。";
}
print "</body></html>";

$select_sth->finish;
$dbh->disconnect;

```
これを /usr/lib/cgi-bin/zipcode/get_zipcode.plとして保存します。

## html 本体
上で作成したperlのscriptを呼ぶhtmlの本体を作ります。以下のようになります。

```html

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
<title>郵便番号検索</title>
</head>
<body>
    <h1>住所から郵便番号を調べる</h1>
    <form name="myform" action="/cgi-bin/zipcode/get_zipcode.pl"  method="post">
	<table> <tr><td class="sidet">
	    <label for="pref">県名：</label>
	</td><td>
	    <input type="text" name="pref" required>
	</td></tr>
	<tr><td>
	    <label for="city">市：</label>
	</td> <td>
	    <input type="text" name="city" required>
	</td></tr>
	<tr><td>
	    <label for="street">町名：</label>
	</td> <td>
	    <input type="text" name="street" required> 
	</td></tr>
		</table>
	        <input type="submit" id="submit" value="検索" >
    </form>

</body>
</html>

```
これを　/var/www/html/zipcode/index.html として保存すれば完成です。
web browserで urlを http://(サーバーのアドレス)/zipcode/index.htmlにアクセスすれば、次のような画面が出るはずです。
![](/images/postal/get_zipcode.jpg =250x)
私のサイトで公開していますので確認してみてください。[ここ](http://takuma.ddns.net/zipcode/index.html)です。Web serverにraspberry pi を使っているのでちょっと非力ですが。
