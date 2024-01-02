#!/usr/bin/env perl
use Encode qw/ from_to /;

open (INFILE, "<$ARGV[0]");
open (OUTFILE, ">$ARGV[1]");
while (<INFILE>) {
    print OUTFILE &convert($_);
}

exit 1;

sub convert
{
    my $file = $_[0];
    from_to( $file, 'utf8', 'shiftjis' );
    return ($file);
}

__END__
