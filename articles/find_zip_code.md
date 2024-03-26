---
title: "郵便番号検索ツールをc#で作ってみた"
emoji: "😸"
type: "idea" # tech: 技術記事 / idea: アイデア
topics: [csharp, ADO]
published: true
---
# はじめに
郵便番号検索サイトを作ってみたのですがオフラインでも動くデスクトップアプリを作ってみたくなったのでVisual Studioを使いC#でプログラムを作ってみました。Visual Studioのソースコードはgithubに入れてあります。[こちら](https://github.com/charliekato/findZipCode)です。Visual Studioでの開発の手順についても簡単に説明を付けておきますので、自分で手を動かして開発の手順を体験してみてください。また、郵便番号のデータはエクセルにしています。
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
# プログラム本体の開発
データベースができたのでプログラムです。プログラムはvisual studioで作りました。visual studioでの開発の手順を以下に説明しますので、ぜひ自分で手を動かして簡単なプログラムの開発を体験してみてください。開発の体験などどうでもいいからプログラムが欲しいという方は、visual studioのプロジェクトファイルやビルドに必要なソースファイル類は[こちらのgithub](https://github.com/charliekato/findZipCode)からダウンロードできますのでそれをご利用ください。もしくは、実行ファイルがあればいいという方は、[こちら](https://github.com/charliekato/zennbook/tree/main/articles/findZipCode/findZipCode.exe)からダウンロードできます。
## Visual Studioを立ち上げる
Visual Studioは個人の利用なら無償で利用できるのでMicrosoftのweb pageなどからダウンロードしてインストールしてください。Visual Studioを起動し最初の画面で、「新しいプロジェクトの作成(N)」をクリックします。(下の図を参照)。なお、筆者はVersion 2022を使っています。
![](/images/findZipCode/VS_start.jpg =250x)
    プロジェクトのテンプレートを選択する画面が出てくるので言語をc#にOSをWindows にアプリの種類をデスクトップにして
    (図の楕円で囲った部分) Windows フォームアプリケーション(.NET Framework) を選び(矢印のところ) 「次へ(N)」 をクリックします。
![](/images/findZipCode/projSetup.jpg =780x)

次のような画面になるのでここでProjectの名前や保存する場所を設定します。Projectの名前はなんでもいいのですが、
下のようにfindZipCodeにしておきます。場所はデフォルトのままで構いませんが自分の好きなところにするのがいいと思います。ソリューションとプロジェクトを同じディレクトリに配置する(D)のところはチェックをつけてもつけなくてもどちらでも問題ありませんが、チェックを外すとディレクトリが一段深くなりちょっと面倒になると思います。 フレームワーク(F) は最新のものを選んでおくのが無難でしょう。
以上設定ができたら「作成(C)」ボタンをクリックします。
![](/images/findZipCode/projSetup2.jpg =760x)
しばらくするとVisual Studioが立ち上がります。インストール後初めて立ち上げたときにどのような画面だったか記憶していないのですが、今の私の場合は下の様になりました。
![](/images/findZipCode/vsScreen.jpg =800x)
ここで上のメニューの「表示」-> 「ソリューションエクスプローラー(P)」を選択しソリューションエクスプローラーを表示させます。下のような画面が立ち上がります。
![](/images/findZipCode/solutionExplorer.jpg =300x)
これを見ると Form1.cs やProgram.cs などが自動で作られているのがわかります。Program.csは修正せずにそのまま使います。 Fomr1.csを変更するのですが、次の手順でやります。ソリューションエクスプローラーのForm1.csを右クリックします。 下のようにポップアップが現れます。
![](/images/findZipCode/dispCode.jpg =350x)
ここで「コードの表示(D)」を選びForm1.csの編集画面を表示させます。この20行のコードをすべて削除し、下のコードを削除した後にコピペします。
ここで注意するのはプロジェクトの名前をfindZipCodeにしていない人はこの6行目のnamespace findZipCode のfindZipCodeをプロジェクトの名前と同じにすることです。

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

次にソリューションエクスプローラーのForm1.csの左側の三角マークをクリックしてForm1.csを展開します。すると下の図のようにForm1.Designer.cs が現れるのでこれをダブルクリックして編集画面を表示させます。下に様な画面になります。
![](/images/findZipCode/designer.cs.jpg =900x)
このForm1.Designer.csというのは最初の画面に出ていた Form1.cs[デザイン](Windows フォームデザイナーと呼ばれています) のフォームにツールボックスの部品を並べてGUIのフォームを作ると自動でできるものですが、今回はできているものをコピペします。ですのででてきたコードはすべて削除し、そのあとに以下のコードを貼り付けます。

```

namespace findZipCode
{
    partial class Form1
    {
        /// <summary>
        /// 必要なデザイナー変数です。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 使用中のリソースをすべてクリーンアップします。
        /// </summary>
        /// <param name="disposing">マネージド リソースを破棄する場合は true を指定し、その他の場合は false を指定します。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows フォーム デザイナーで生成されたコード

        /// <summary>
        /// デザイナー サポートに必要なメソッドです。このメソッドの内容を
        /// コード エディターで変更しないでください。
        /// </summary>
        private void InitializeComponent()
        {
            this.lbxPref = new System.Windows.Forms.ListBox();
            this.lbxCity = new System.Windows.Forms.ListBox();
            this.lbxStreet = new System.Windows.Forms.ListBox();
            this.lblPref = new System.Windows.Forms.Label();
            this.lblCity = new System.Windows.Forms.Label();
            this.lblStreet = new System.Windows.Forms.Label();
            this.lblPostalCode = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // lbxPref
            // 
            this.lbxPref.Font = new System.Drawing.Font("MS UI Gothic", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.lbxPref.FormattingEnabled = true;
            this.lbxPref.ItemHeight = 33;
            this.lbxPref.Location = new System.Drawing.Point(133, 40);
            this.lbxPref.Name = "lbxPref";
            this.lbxPref.Size = new System.Drawing.Size(207, 763);
            this.lbxPref.TabIndex = 0;
            this.lbxPref.SelectedIndexChanged += new System.EventHandler(this.lbxPref_SelectedIndexChanged);
            // 
            // lbxCity
            // 
            this.lbxCity.Font = new System.Drawing.Font("MS UI Gothic", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.lbxCity.FormattingEnabled = true;
            this.lbxCity.ItemHeight = 33;
            this.lbxCity.Location = new System.Drawing.Point(454, 40);
            this.lbxCity.Name = "lbxCity";
            this.lbxCity.Size = new System.Drawing.Size(302, 763);
            this.lbxCity.TabIndex = 1;
            this.lbxCity.SelectedIndexChanged += new System.EventHandler(this.lbxCity_SelectedIndexChanged);
            // 
            // lbxStreet
            // 
            this.lbxStreet.Font = new System.Drawing.Font("MS UI Gothic", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.lbxStreet.FormattingEnabled = true;
            this.lbxStreet.ItemHeight = 33;
            this.lbxStreet.Location = new System.Drawing.Point(874, 40);
            this.lbxStreet.Name = "lbxStreet";
            this.lbxStreet.Size = new System.Drawing.Size(645, 763);
            this.lbxStreet.TabIndex = 2;
            this.lbxStreet.SelectedIndexChanged += new System.EventHandler(this.lbxStreet_SelectedIndexChanged);
            // 
            // lblPref
            // 
            this.lblPref.AutoSize = true;
            this.lblPref.Font = new System.Drawing.Font("MS UI Gothic", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.lblPref.Location = new System.Drawing.Point(51, 40);
            this.lblPref.Name = "lblPref";
            this.lblPref.Size = new System.Drawing.Size(47, 33);
            this.lblPref.TabIndex = 3;
            this.lblPref.Text = "県";
            // 
            // lblCity
            // 
            this.lblCity.AutoSize = true;
            this.lblCity.Font = new System.Drawing.Font("MS UI Gothic", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.lblCity.Location = new System.Drawing.Point(383, 40);
            this.lblCity.Name = "lblCity";
            this.lblCity.Size = new System.Drawing.Size(47, 33);
            this.lblCity.TabIndex = 4;
            this.lblCity.Text = "市";
            // 
            // lblStreet
            // 
            this.lblStreet.AutoSize = true;
            this.lblStreet.Font = new System.Drawing.Font("MS UI Gothic", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.lblStreet.Location = new System.Drawing.Point(801, 40);
            this.lblStreet.Name = "lblStreet";
            this.lblStreet.Size = new System.Drawing.Size(47, 33);
            this.lblStreet.TabIndex = 5;
            this.lblStreet.Text = "町";
            // 
            // lblPostalCode
            // 
            this.lblPostalCode.AutoSize = true;
            this.lblPostalCode.Font = new System.Drawing.Font("MS UI Gothic", 15F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.lblPostalCode.Location = new System.Drawing.Point(257, 824);
            this.lblPostalCode.Name = "lblPostalCode";
            this.lblPostalCode.Size = new System.Drawing.Size(0, 40);
            this.lblPostalCode.TabIndex = 6;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(13F, 24F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1974, 929);
            this.Controls.Add(this.lblPostalCode);
            this.Controls.Add(this.lblStreet);
            this.Controls.Add(this.lblCity);
            this.Controls.Add(this.lblPref);
            this.Controls.Add(this.lbxStreet);
            this.Controls.Add(this.lbxCity);
            this.Controls.Add(this.lbxPref);
            this.Name = "Form1";
            this.Text = "郵便番号検索";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ListBox lbxPref;
        private System.Windows.Forms.ListBox lbxCity;
        private System.Windows.Forms.ListBox lbxStreet;
        private System.Windows.Forms.Label lblPref;
        private System.Windows.Forms.Label lblCity;
        private System.Windows.Forms.Label lblStreet;
        private System.Windows.Forms.Label lblPostalCode;
    }
}

```

以上で完成ですが、念のため本来手でGUI部品(ボタンとかラベルなど)を配置して作っていくフォームがどうなっているか見てみます。ソリューションエクスプローラーのForm1.csを右クリックして今度はデザイナーの表示(D)を選び(下の図参照)フォームデザイナーを表示させます。
![](/images/findZipCode/formDesigner.jpg =300x)
ここで下の様になっていれば以上の操作がうまくいったということです。
![](/images/findZipCode/form1.jpg =900x)
プログラムはできたのでコンパイルをします。うえのメニューから「ビルド」-> 「ソリューションのビルド」を選びます。下の図参照。

![](/images/findZipCode/build.jpg =400x)

ここでVisual Studioの左下の部分に注目します。しばらくしてそこに下の図のように「ビルド正常終了」とでていれば成功です。
![](/images/findZipCode/buildSuccess.jpg =120x)
ビルドしたものが保存されている場所をエクスプローラーで見てみます。その前にVisual Studioの上の方のメニューのビルド(B)の下あたりが以下の図のように"Debug" "Any CPU" になっていることを確認しておきます。これが別のもの例えばAny CPUがx64などになっていたらビルドされてできたexeファイルが保存される場所が変わります。
ここでまたソリューションエクスプローラーの上の方の findZipCodeのところを右クリックします。下の図のようになるのでここで「エクスプローラーでフォルダーを開く」選びます。
![](/images/findZipCode/explorer1.jpg =500x)
ここで、bin をダブルクリックし、さらにDebugをダブルクリックすると下の図のようにビルドで生成されたファイルが保存されているフォルダーが表示されます。

![](/images/findZipCode/explorer2.jpg =500x)
実行形式のファイルexeファイルができているが分かります。このフォルダーに上で作ったデーターベースが入っているexcelファイルを入れておいてください。エクセルファイルをここに入れたらfindZipCode.exeをダブルクリックしても動きますし、Visual Studioの「Any CPU」の右側にある「開始」をクリックしてもプログラムを開始することができます。
プログラム本体とデータを別のファイルにしているので郵便番号に追加変更があった場合はエクセルファイルをアップデートすればそのまま使えます。
