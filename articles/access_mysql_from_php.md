---
title: "PHPからMysqlへアクセス"
emoji: "🦁"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: [php, mysql]
published: false
---
# はじめに
PHPからMysqlへのアクセス方法がわかったので自分用メモを兼ねここに概要を残します。
UBUNTUとWindows11でcliでの動作を確認しています。
# Mysqlのインストール
MysqlはMariaDBをインストールしました。手順については、[こちら](https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-20-04-ja) が参考になります。
私もこの手順でインストールと設定をしています。
# php-mysqlのインストール
次にphpのmysqlのインストールです。ubuntuでは簡単で、aptでインストールします。

```bash
sudo apt install php-mysql
```
Windowsではphp.iniファイルを編集します。私の場合は、C:\PHPに php.iniがありました。このファイルに次の行を追加します。
```
extensiondir = "C:\PHP"
extension=php_mbstring.dll
extension=php_mysqli.dll
```

# PHPコード例
testdb というデータベースのsampletableというテーブルのitem1とitem2を単にプリントするだけのコード。

```php
 <?php
    $host = 'hostnamehere';
    $user = 'user';
    $password = 'password';
    $dbname = 'testdb';
    $link = mysqli_connect($host, $user, $password );
    $db_selected = mysqli_select_db($link, $dbname );
    $result = mysqli_query($link, 'SELECT item1, item2 FROM sampletable');
    while ( $row = mysqli_fetch_assoc($result)) {
	print( $row['item1']. ",  ". $row['item2']."\n");
    }

    mysqli_close($link);
?>

```
