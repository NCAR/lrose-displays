#!/bin/perl

open(VOR,"vortacs.gis") || die "cannot open file vortacs.gis\n";
open(LVO,"awc_labeled_vortacs.map") || die "Cannot open file awc_labeled\n";
open(OUT,">labeled_high_vortacs.map");
$count=0;
while(<VOR>) {
    @line = split();
    if($line[5] eq "H") {
	$save[$i] = $count;
	$i++;
    }
    $count++;
}

$count =0;
$i=2;
while(<LVO>) {
    if($count == $save[$i]) {
	print OUT "$_";
	$i++;
    }
    $count++;
}
close(OUT);
exit;
