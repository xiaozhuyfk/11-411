#!/usr/bin/perl

# Noah A. Smith
# 2/21/08
# Runs the Viterbi algorithm (no tricks other than logmath!), given an
# HMM, on sentences, and outputs the best state path.

# Usage:  viterbi.pl hmm-file < text > tags

# The hmm-file should include two kinds of lines.  One is a transition:
# trans Q R P
# where Q and R are whitespace-free state names ("from" and "to," 
# respectively) and P is a probability.  The other kind of line is an 
# emission:
# emit Q S P
# where Q is a whitespace-free state name, S is a whitespace-free
# emission symbol, and P is a probability.  It's up to you to make sure
# your HMM properly mentions the start state (named init by default),
# the final state (named final by default) and out-of-vocabulary
# symbols (named OOV by default).

# If the HMM fails to recognize a sequence, a blank line will be written.
# Change $verbose to 1 for more verbose output.

# special keywords:
#  $init_state   (an HMM state) is the single, silent start state
#  $final_state  (an HMM state) is the single, silent stop state
#  $OOV_symbol   (an HMM symbol) is the out-of-vocabulary word

use bytes;

$init_state = "init";
$final_state = "final";
$OOV_symbol = "OOV";

$verbose = 0;

# read in the HMM and store the probabilities as log probabilities

$hmmfile = shift;
open(HMM, "<$hmmfile") or die "could not open $hmmfile";
while(<HMM>) {
    if(($ppprev, $pprev, $prev, $p) = (m/trans\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/)) {
        $A{$ppprev}{$pprev}{$prev} = log($p);
        $States{$pprev} = 1;
        $States{$prev} = 1;
        $States{$ppprev} = 1;
    } elsif(($prev, $w, $p) = (m/emit\s+(\S+)\s+(\S+)\s+(\S+)/)) {
        $B{$prev}{$w} = log($p);
        $States{$prev} = 1;
        $Voc{$w} = 1;
    }
}
close(HMM);

while(<>) { # read in one sentence at a time
    chomp;
    @w = split;
    $n = scalar(@w);
    unshift @w, "";
    %V = ();
    %Backtrace_bi = ();
    $V{0}{$init_state}{$init_state} = 0.0;  # base case of the recurisve equations!

    for($i = 1; $i <= $n; ++$i) {     # work left to right ...
    # if a word isn't in the vocabulary, rename it with the OOV symbol
        unless(defined $Voc{$w[$i]}) {
            print STDERR "OOV:  $w[$i]\n" if($verbose);
            $w[$i] = $OOV_symbol;
        }
        foreach $prev (keys %States) { # consider each possible current state
            foreach $pprev (keys %States) { # each possible previous state
                foreach $ppprev (keys %States) {
                    if(defined $A{$ppprev}{$pprev}{$prev}  # only consider "non-zeros"
                           and defined $B{$q}{$w[$i]} 
                           and defined $V{$i - 1}{$ppprev}{$pprev}) 
                    {
                        $v = $V{$i - 1}{$ppprev}{$pprev} + $A{$ppprev}{$pprev}{$prev} + $B{$prev}{$w[$i]};
                        if(!(defined $V{$i}{$pprev}{$prev}) or $v > $V{$i}{$pprev}{$prev}) {
                            # if we found a better previous state, take note!
                            $V{$i}{$pprev}{$prev} = $v;  # Viterbi probability
                            $Backtrace_bi{$i}{$pprev}{$prev} = $ppprev; # best previous state
                        }
                    }
                }
            }
            print STDERR "V[$i, $q] = $V{$i}{$q} ($B{$i}{$q})\n" if($verbose);
        }
    }
    # this handles the last of the Viterbi equations, the one that brings
    # in the final state.
    $foundgoal = 0;
    $back_prev = 0;
    $back_pprev = 0;
    foreach $ppprev (keys %States) {
        foreach $pprev (keys %States) { # for each possible state for the last word
            if(defined $A{$pprev}{$final_state} and defined $V{$n}{$ppprev}{$pprev}) {
                $v = $V{$n}{$ppprev}{$pprev} + $A{$ppprev}{$pprev}{$final_state};
                if(!$foundgoal or $v > $goal) {
                    # we found a better path; remember it
                    $goal = $v;
                    $foundgoal = 1;
                    $back_prev = $pprev;
                    $back_pprev = $ppprev;
                }
            }
        }
    }
    
    # this is the backtracking step.
    if($foundgoal) {
        @t = ();
        for($i = $n; $i > 0; --$i) {
            unshift @t, $back_prev;
            $pprev = $Backtrace_bi{$i}{$back_pprev}{$back_prev};
            $back_prev = $back_pprev;
            $back_pprev = $pprev;
        }
    }
    print STDERR exp($goal), "\n" if($verbose);
    if($foundgoal) { print join " ", @t; }
    print "\n";
}
