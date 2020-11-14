#!/usr/bin/perl -w
# Reference: https://www.perl.org/books/library.html
use warnings;
use strict;

# Run from parent folder
my @workingdir = ("samples");

# Create directories for data extraction
my $crowdindir = "crowdin";
my $commentdir = "$crowdindir/comment/";
my $stringsdir = "$crowdindir/strings/";
unless(-e $crowdindir or mkdir $crowdindir) {
	die "Unable to create $crowdindir\n";
}
unless(-e $commentdir or mkdir $commentdir) {
	die "Unable to create $commentdir\n";
}
unless(-e $stringsdir or mkdir $stringsdir) {
	die "Unable to create $stringsdir\n";
}

($_) = "$commentdir/@workingdir";
unless(-e $_ or mkdir $_) {
	die "Unable to create $_\n";
}
($_) = "$stringsdir/@workingdir";
unless(-e $_ or mkdir $_) {
	die "Unable to create $_\n";
}

# Searching for comments:
# Copy all the comments into a shadow file
# Populate indeces
# Reference: https://habr.com/ru/company/regru/blog/232933/
sub copy_comment($) {
	my ($filename) = @_;
	my $outptfile = "$commentdir$filename";
	my $indexfile = "$commentdir$filename.index";
	
	open LSFFILE, "$filename" or die $!;
	open CRWFILE, ">>$outptfile" or die $!;
	open INDFILE, ">>$indexfile" or die $!;
	
	my $linenum = 0; # line in initial file
	my $indxnum = 0; # line in shadow file
	while(<LSFFILE>) {
		$linenum++;
		if(m!//(.*)! && !(m!//#!))
		{
			$indxnum++;
			print CRWFILE "$1\n";
			print INDFILE "$linenum:$indxnum\n";
		}
	}
	close(CRWFILE) || warn "close failed: $!";
	close(INDFILE) || warn "close failed: $!";
}

# Searching for strings:
# Copy all the comments into a shadow file
# Populate indeces
# Reference: http://citforum.ru/internet/perl/regexp/
sub copy_strings($) {
	my ($filename) = @_;
	my $outptfile = "$stringsdir$filename";
	my $indexfile = "$stringsdir$filename.index";
	
	open LSFFILE, "$filename" or die $!;
	open CRWFILE, ">>$outptfile" or die $!;
	open INDFILE, ">>$indexfile" or die $!;
	
	my $linenum = 0; # line in initial file
	my $indxnum = 0; # line in shadow file
	while(<LSFFILE>) {
		$linenum++;
		if(/('|")(.*)('|")/) # single or double quotes, with backtracking
		{
			$indxnum++;
			print CRWFILE "$2\n";
			print INDFILE "$linenum:$indxnum\n";
		}
	}
	close(CRWFILE) || warn "close failed: $!";
	close(INDFILE) || warn "close failed: $!";
}

# Read the next directory
# Create shadow directories
# Run parser for every LSF file in the directory
# Reference: https://docs.google.com/viewer?url=https%3A%2F%2Fblob.perl.org%2Fbooks%2Fbeginning-perl%2F3145_Chap06.pdf
sub process_dir($) {
	my ($dirname) = @_;
    unless(-e "$commentdir$dirname" or mkdir "$commentdir$dirname") {
        die "Unable to create $commentdir$dirname\n";
    }
    unless(-e "$stringsdir$dirname" or mkdir "$stringsdir$dirname") {
        die "Unable to create $stringsdir$dirname\n";
    }
	my @lsffiles = glob("$dirname/*lsf");
	foreach my $lsffile (@lsffiles)
	{
		print "$lsffile\n";
		copy_comment("$lsffile");
		copy_strings("$lsffile");
	} 
}

# Recursion through the repository
# Reference: https://www.opennet.ru/tips/947_perl_hash.shtml
my $currentdir;
my $diritem;
while ($currentdir = shift(@workingdir)) {
	opendir CDIR, $currentdir or die "Couldn't open the current directory: $!";
	while ($_ = readdir(CDIR)) {
		next if $_ eq "." or $_ eq ".." or m/\.git/i;
		$diritem = "$currentdir/$_";
		if(-d $diritem) {
			unshift(@workingdir,$diritem);
			print "$diritem\n";
			process_dir($diritem);
		}
	}
	closedir CDIR;
}

# Further clean up
# In system command line:
# find -type f -empty | xargs rm # remove empty files
# find -type d -empty | xargs rm -r # remove empty dirs

# Before distribution make copy of the folder and clean up index files out there:
# find -name "*.index" | xargs rm # use with care in duplicate folder only
