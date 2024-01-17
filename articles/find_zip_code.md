---
title: "郵便番号検索ツールをc#で作ってみた"
emoji: "😸"
type: "idea" # tech: 技術記事 / idea: アイデア
topics: [csharp, ADO]
published: true
---
# はじめに
郵便番号検索サイトを作ってみたのですがオフラインでも動くデスクトップアプリを作ってみたくなったのでVisual Studioを使いC#でプログラムを作ってみました。Visual Studioのソースコードはgithubに入れてあります。[こちら](https://github.com/charliekato/findZipCode)です。郵便番号のデータはエクセルにしています。
エクセルファイルは必要ですが、Microsoftのエクセルアプリがなくてもプログラムは動くと思います。
![](/images/findZipCode/findZipCodeScreenShot.jpg =600x)
*スクリーンショット*
# データベース作成
## 郵便番号csvのダウンロード
データベースにはaccess, sqlserverや、mysqlなどありますが、エクセルならたいていの方が持っているのでエクセルにしました。エクセルなら比較的簡単にデータベースを作れると思います。データベースを作るのも面倒もしくは、エクセルアプリそのものをお持ちでない方は[こちらのgithub](https://github.com/charliekato/zennbook/tree/main/articles/findZipCode/zipcode.xlsx)からダウンロードしてお使いください。
データは郵便局のホームページからutf_ken_all.csv をダウンロードしてきます。「郵便番号データダウンロード」でググってもらえばすぐに出てくるはずです。住所の郵便番号（1レコード1行、UTF-8形式）（CSV形式）のところをクリックしてzip形式のファイルをダウンロードします。
ファイルはUTF-8なのでsjisに変換する必要があります。windowsでutf-8をsjisに変換する方法はChatGPTに聞いてみてください。以下は私が聞いた結果です。(注意: 私自身はこの方法ではやっていませんので)
## UTF-8をsjisに変換
WindowsでUTF-8のテキストファイルをShift_JIS（sjis）に変換するには、いくつかの方法があります。以下にいくつかの方法を示します。

1. PowerShellを使用する方法
PowerShellを使用してファイルを変換することができます。以下はその一例です。

```powershell
# ファイルの内容を読み取り、Shift_JISに変換して新しいファイルに保存します。
Get-Content -Path "C:\path\to\your\utf8file.txt" -Encoding UTF8 | Out-File -FilePath "C:\path\to\your\sjisfile.txt" -Encoding SJIS
```
2. コマンドプロンプトとiconvを使用する方法
iconvはテキストのエンコーディング変換を行うユーティリティです。Windowsでiconvを使用するには、多くの場合、CygwinやMinGW、Windows Subsystem for Linux（WSL）などのツールをインストールする必要があります。

例えば、Cygwinがインストールされている場合、以下のようにしてUTF-8からShift_JISに変換できます：

```bash
iconv -f UTF-8 -t SHIFT_JIS "C:\path\to\your\utf8file.txt" > "C:\path\to\your\sjisfile.txt"
```
3. エディタを使用する方法
多くのテキストエディタ（例：Notepad++、Visual Studio Codeなど）は、ファイルのエンコーディングを変更する機能を提供しています。エディタを開き、ファイルをShift_JISエンコーディングで保存するオプションを選択することで変換できます。

この方法の具体的な手順は、使用しているエディタによって異なりますので、エディタの公式ドキュメントやヘルプを参照してください。

これらの方法の中から、状況や好みに応じて最適な方法を選択してください。

## エクセルに取り込み
エクセルに取り込むのは変換してできてたcsv をダブルクリックすればできます。シートの名前はzipcodeにしておいてください。不必要なカラムはすべて削除し、7桁の郵便番号と県名、都市名、町名の4つのカラムだけのこし、先頭行に見出し(ヘッダー)を挿入します。
![](/images/findZipCode/zipcodexlsx.jpg =360x)
上の図のように7桁の郵便番号は zipcode 県名は pref 都市名は city 町名は streetにします。
エクセルにはもう一枚シートを作ります。このシートには県名と県番号の対応表を作ります。これも「県番号」でググったら出てきますのでそれを使って下の図のように作ります。見出し行は県名を pref 県番号を　prefNo　としておいてください。(エクセルのシート名とヘッダー行の記述が違うとプログラムは正しく動作しませんので注意してください。)
![](/images/findZipCode/prefNo.jpg =360x)
出来たexcelファイルはzipcode.xlsxという名前で実行ファイル(findZipCode.exe)とおなじフォルダーに入れておく必要があります。
# プログラム本体
データベースができたのでプログラムです。プログラムはvisual studioで作りました。visual studioのプロジェクトファイルやビルドに必要なソースファイル類は[こちらのgithub](https://github.com/charliekato/findZipCode)からダウンロードできます。以下にもコード(自分でコーディングしたもののみ。つまりvisual studioが自動的に生成したコードは割愛します。)を載せます。またプログラムの説明は割愛させていただきます。実行ファイルが必要な方は[こちら](https://github.com/charliekato/zennbook/tree/main/articles/findZipCode/findZipCode.exe)からダウンロードしてください。
```c#:Form1.cs
using System;
using System.IO;
using System.Windows.Forms;
using System.Data.OleDb;

namespace findZipCode
{
    public partial class Form1 : Form
    {
        private const string magicWord = "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=";
        private const string magicTail = ";Extended Properties='Excel 12.0; HDR=Yes'";
        public const string excelFile = "zipcode.xlsx";
        public string city;
        public string pref;
        public string street;
         public Form1()
        {
            InitializeComponent();
            get_pref_list();
            myinit();
        }

        private void myinit()
        {
            lbxCity.SelectionMode = SelectionMode.One;
            lbxPref.SelectionMode = SelectionMode.One;
            lbxStreet.SelectionMode = SelectionMode.One;
            lblPostalCode.Text = string.Empty;
            this.Width = 800;
        }
        public void get_pref_list()
        {
            String connectionString = magicWord + excelFile + magicTail;
            using (OleDbConnection conn = new OleDbConnection(connectionString))
            {
                string query = "SELECT prefNo, pref from [pref$] order by prefNo;";
                OleDbCommand comm = new OleDbCommand(query, conn);
                conn.Open();
                using (var dr = comm.ExecuteReader())
                {
                    while (dr.Read())
                    {
                        this.lbxPref.Items.Add(Convert.ToString(dr["pref"]));
                    }
                }
            }
        }

        private void lbxPref_SelectedIndexChanged(object sender, EventArgs e)
        {
            String connectionString = magicWord + excelFile + magicTail;
            this.lbxCity.Items.Clear();
            pref = Convert.ToString(lbxPref.SelectedItem);
            using (OleDbConnection conn = new OleDbConnection(connectionString))
            {
                string query = "SELECT DISTINCT city from [zipcode$] where pref = \"" + pref + "\";";
                OleDbCommand comm = new OleDbCommand(query, conn);
                conn.Open();
                using (var dr = comm.ExecuteReader())
                {
                    while (dr.Read())
                    {
                        this.lbxCity.Items.Add(Convert.ToString(dr["city"]));
                    }
                }
            }
        }



        private void lbxCity_SelectedIndexChanged(object sender, EventArgs e)
        {
            String connectionString = magicWord + excelFile + magicTail;
            const string others = "以下に掲載がない場合";
            this.lbxStreet.Items.Clear();
            city = Convert.ToString(lbxCity.SelectedItem);
            this.lbxStreet.Items.Add(others);
            using (OleDbConnection conn = new OleDbConnection(connectionString))
            {
                string query = "SELECT DISTINCT street from [zipcode$] where pref = \""+
                    pref + "\" AND city = \"" + city + "\";";
                OleDbCommand comm = new OleDbCommand(query, conn);
                conn.Open();
                using (var dr = comm.ExecuteReader())
                {
                    while (dr.Read())
                    {
                        street = Convert.ToString(dr["street"]);
                        if (street != others)
                        this.lbxStreet.Items.Add(street);
                    }
                }
            }

        }

        private void lbxStreet_SelectedIndexChanged(object sender, EventArgs e)
        {
            String connectionString = magicWord + excelFile + magicTail;
            street = Convert.ToString(lbxStreet.SelectedItem);
            using (OleDbConnection conn = new OleDbConnection(connectionString))
            {
                string query = "SELECT zipcode from [zipcode$] where pref = \"" + 
                    pref+ "\" AND city = \"" + city + 
                    "\" AND street = \"" + street + "\";";
                OleDbCommand comm = new OleDbCommand(query, conn);
                conn.Open();
                using (var dr = comm.ExecuteReader())
                {
                    while (dr.Read())
                    {
                        string postalNumber = Convert.ToString(dr["zipcode"]);
                        string postalCode = postalNumber.Insert(3, "-");
                        this.lblPostalCode.Text = pref+city+street+ "の郵便番号は " + postalCode;
                    }
                }
            }
        }

    }

}

```
プログラム本体とデータを別のファイルにしているので郵便番号に追加変更があった場合はエクセルファイルをアップデートすればそのまま使えます。
