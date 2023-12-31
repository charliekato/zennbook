#!/usr/bin/perl
use strict;
use warnings;
use DBI;
use CGI;

# データベース接続情報
my $db_name = 'zipcodedb';
my $db_user = 'username'; #mysqlのuser nameを適切に変更する事
my $db_password = 'password'; #passwordを適切に変更する事
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
    ($zipcode, $dummy) = @$ar_ref;
    $zipcode =~ s/^(\d{3})(\d{4})$/$1-$2/;
    print "$pref$city$street の郵便番号は、";
    print "$zipcode です。\n";
} else {
    print "見つかりません。";
}
print "</body></html>";

$select_sth->finish;
$dbh->disconnect;
