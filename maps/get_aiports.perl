#!/bin/perl

open(VOR,"airports_list") || die "cannot open file airports_list\n";
open(OUT,">labeled_airports.map");

$count=0;
while(<VOR>) {
    @line = split();
    open(LVO,"awc_labeled_airports.map") || die "Cannot open file awc_labeled\n";
    while(<LVO>) {
	@ln = split();
	$lat = substr($ln[2],0,2);
	$lng = substr($ln[3],0,4);
	if($lat == $line[0] && $lng == $line[1]) {
	    print OUT "$_";
	}
    }
    close(LVO);
}
close(OUT);
exit;
