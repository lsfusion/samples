#!/usr/bin/perl -w
# Reference: https://www.perl.org/books/library.html
use warnings;
use strict;
use utf8;

# Prepare repo of translated sourcecodes
# Checkout to commit of the translation snapshot
# The proper commit was selected using git log command
# git checkout e01a12260ec65ed4cc2f17801ac7e5d2d582ee4d
# Create new branch for further commit of the translation
# git switch -c translation
# Now the chancges in the files can be commited into the repo
# don"t forget to merge later on with the changes, made during the translation

# Run from parent folder
my $targetsdir = ("samples");
my @workingdir = ("crowdout");

# Connect directories with data extraction
my $crowdindir = "crowdin";

# Connect directories with data translation
my $crowdoutdir = "crowdout";

# Type - comment or string
my $linetype;

# Early return
my $runFlag = 1;

# Translate single file
# With taking care of indexes
sub translate_file {
    my ($tr,$crw,$indx,$target) = @_;
    
	open EXCHANGEFILE, "$tr" or die $!;
	my @translations = <EXCHANGEFILE>;
	close(EXCHANGEFILE) || die "close failed: $!";
	
	open EXCHANGEFILE, "$crw" or die $!;
	my @crowdins = <EXCHANGEFILE>;
	close(EXCHANGEFILE) || die "close failed: $!";
	
	open EXCHANGEFILE, "$indx" or die $!;
	my @indexes = <EXCHANGEFILE>;
	close(EXCHANGEFILE) || die "close failed: $!";
	
	open EXCHANGEFILE, "$target" or die $!;
	my @sources = <EXCHANGEFILE>;
	close(EXCHANGEFILE) || die "close failed: $!";
	
    print "\nIn $target of Category $linetype - Number of lines: ",scalar(@sources),"; Number of occurances: ",scalar(@translations),"\n\n";
	
	my $linenum = 0; # line in initial file
	my $indxnum = 0; # line in shadow file
	foreach (@translations) {
		$indxnum++;
		
		# Find index of associated target line
		foreach (@indexes) {
            /(.*)\:(.*)/;
            if ($2 == $indxnum) {
                $linenum = $1;
            }
		}
		
		# Masks of comments and strings are different
		if ($linetype eq "comment") {
            # Check if the source contains the comment
            if ($sources[$linenum-1] =~ m!//(.*)!) {
                print "[OK] $sources[$linenum-1]";
                print " <- $crowdins[$indxnum-1] -> $translations[$indxnum-1]";
                # Clean the translation from the EOL symbols
                $translations[$indxnum-1] =~ /(.*)\n/;
                my $translationstring = $1;
                $sources[$linenum-1] =~ s!//.*!//$translationstring!;
            }
            else {
                print "[EE] No comment in line $linenum: $sources[$linenum-1] with translated source index $indxnum found: $crowdins[$indxnum-1]";
            }
		}
		else {
            # Check if the source contains the string
            if ($sources[$linenum-1] =~ /'|"(.*)'|"/) {
                print "[OK] $sources[$linenum-1]";
                print " <- $crowdins[$indxnum-1] -> $translations[$indxnum-1]";
                # Clean the translation from the EOL symbols
                $translations[$indxnum-1] =~ /(.*)\n/;
                my $translationstring = $1;
                $sources[$linenum-1] =~ s/('|").*('|")/$1$translationstring$2/;
            }
            else {
                print "[EE] No string in line $linenum: $sources[$linenum-1] with translated source index $indxnum found: $crowdins[$indxnum-1]";
            }
		}
	}
	
	# Replacement
	open EXCHANGEFILE, ">$target" or die $!;
	print EXCHANGEFILE @sources;
	close(EXCHANGEFILE) || warn "close failed: $!";
}

# Process all files in subdirs
# Read list of files
# Read indexes for each files (optionally, the original text)
# Run replacement in target with care of indexes
sub extract_translate {
    my ($translate) = @_;
    my @trfiles = glob("$translate/*lsf");
    foreach my $trffile (@trfiles)
    {
        my $srcfile = $trffile =~ s/$crowdoutdir/$crowdindir/r;
        unless(-e $srcfile) {
            die "Sorce file was not found for: $trffile";
        }
        
        my $indexfile = "$srcfile.index";
        unless(-e $indexfile) {
            die "Index file was not found for: $srcfile";
        }
        
        my $targetfile = $trffile =~ s/$crowdoutdir\/comment|$crowdoutdir\/strings/$targetsdir/r;
        unless(-e $targetfile) {
            die "Target file was not found for: $srcfile";
        }
        
        translate_file($trffile,$srcfile,$indexfile,$targetfile);
        
        #$runFlag = 0;
    }
}


# Recursion through the translation
# Connecting indexes and target subdirs
# Reference: https://www.opennet.ru/tips/947_perl_hash.shtml
my $currentdir;
my $diritem;
my $srcitem;
my $targetd;
while ($currentdir = shift(@workingdir)) {
	opendir CDIR, $currentdir or die "Couldn't open the current directory: $!";
	while ($_ = readdir(CDIR)) {
		next if $_ eq "." or $_ eq ".." or m/\.git/i;
		$diritem = "$currentdir/$_";
		if(-d $diritem and $runFlag) {
			unshift(@workingdir,$diritem);
			# non-destructive replacement with modifier r
			# https://perldoc.perl.org/perlrequick
			
			# connect index sources
			$srcitem = $diritem =~ s/$crowdoutdir/$crowdindir/r;
			
			# connect target
			$targetd = $diritem =~ s!$crowdoutdir/comment|$crowdoutdir/strings!$targetsdir!r;
			if ($diritem =~ m!$crowdoutdir/comment!) {
                $linetype = "comment";
			}
			else {
                $linetype = "strings";
            }
			
            unless(-e "$diritem" or -e "$srcitem" or -e "$targetd") {
                die "Some of sources do not exist";
            }
			
			if(glob("$diritem/*lsf")) {
                print "$diritem (sources: $srcitem) -> $targetd - translated files:\n";
			}
			
            extract_translate($diritem);
			
		}
	}
	closedir CDIR;
}
