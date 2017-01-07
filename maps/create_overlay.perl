#!/bin/perl

open(IN,"airport_range_ring.list") || die "cannot open file airport_range_ring.list\n";

while(<IN>) {
    @line = split();
    if($line[0] eq "ICON") {
	$lat = $line[2];
	$lon = $line[3];
	$airport = $line[6];
	system("/rap/bin/OverlayCreate -clat $lat -clon $lon -crad 92.6 -cnpts 36 >> airport_range_rings.map");
	open(OUT,">>airport_range_rings.map") || die "cannot open file airport_range_rings.map for writing\n";
	print OUT "\n";
	close(OUT);
    }
}
close(IN);
exit;
