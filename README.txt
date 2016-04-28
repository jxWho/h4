JIAXIANG HU (jh3648)
Run time : around 4 mins

Part A :
3)
AER :
IBM Model 1
---------------------------
Average AER: 0.665

IBM Model 2
---------------------------
Average AER: 0.650

Ex :

[u'Ich', u'bitte', u'Sie', u',', u'sich', u'zu', u'einer', u'Schweigeminute', u'zu', u'erheben', u'.']
[u'Please', u'rise', u',', u'then', u',', u'for', u'this', u'minute', u"'", u's', u'silence', u'.']

The alignment for IBM1 is:
0-1 1-1 2-1 3-4 4-10 5-10 6-10 7-10 8-10 9-1
The alignment for IBM2 is:
0-0 1-1 2-0 3-2 4-10 5-10 6-10 7-7 8-10 9-0
while the correct alignment should be:
0-0 1-0 2-0 10-11 5-5 6-6 4-1 7-7 7-8 8-10 9-10 7-10 3-4 7-9

For the alignments of first three words, the performance of IBM2 is over IBM1.
The reason is that 'Ich' and 'Sie' are both aligned to the uncommon words, which
makes the probability of languge model low (t). However, IBM2 also takes account
into the location, where 0->0 and 2->0 are high. Hence, IBM2 works better
in this part.

4)
IBMM1 : 0.626
IBMM2 : 0.642

IBMM1 :
The reasonable number of iterations which provides the lower bound for IBMM1
is 6. With the increase of iterations, the AER decreases to reach a local
minimal, then AER increases. And it repeats the previous process.
Results for this are as follow:
1 - > 19
Average AER: 0.873
Average AER: 0.684
Average AER: 0.641
Average AER: 0.630
Average AER: 0.626
Average AER: 0.629
Average AER: 0.631
Average AER: 0.628
Average AER: 0.665
Average AER: 0.666
Average AER: 0.666
Average AER: 0.666
Average AER: 0.665
Average AER: 0.665
Average AER: 0.665
Average AER: 0.662
Average AER: 0.661
Average AER: 0.661


IBMM2 :
The reasonable number of iterations which provides the lower bound for IBMM1
is 4. The AER of IBM2 tends to drecrease, increase and then decrease to a
stable point.

Results:(1-19)
Average AER: 0.646
Average AER: 0.644
Average AER: 0.644
Average AER: 0.642
Average AER: 0.644
Average AER: 0.647
Average AER: 0.646
Average AER: 0.649
Average AER: 0.649
Average AER: 0.650
Average AER: 0.649
Average AER: 0.650
Average AER: 0.652
Average AER: 0.652
Average AER: 0.650
Average AER: 0.650
Average AER: 0.651
Average AER: 0.651
Average AER: 0.651

Part B
4)
AER : 0.551

Ex. :
[u'All', u'dies', u'entspricht', u'den', u'Grunds\xe4tzen', u',', u'die', u'wir', u'stets', u'verteidigt', u'haben', u'.']
[u'This', u'is', u'all', u'in', u'accordance', u'with', u'the', u'principles', u'that', u'we', u'have', u'always', u'upheld', u'.']

BerkeleyAligner:
0-0 1-4 2-2 3-3 4-7 5-8 6-6 7-9 8-11 9-12 10-10 11-13
Ibmm2 :
0-12 1-4 2-7 3-4 4-12 5-10 6-10 7-9 8-7 9-12 10-7
Correct :
0-2 1-0 2-3 3-6 4-7 5-8 6-8 7-9 8-11 9-12 10-10 11-13 2-1 2-4 2-5

Word #4 u'Grunds\xe4tzen' is aligned to u'upheld', which means the language
model t and 4->12 have high probabilities. However, if we consider the reverse
version, it may be true that 12 -> 4 has pretty low probability, which makes
BerkeleyAligner does pick this as the answer. And then, BerkeleyAligner makes
a better decision.
Similary, for the case case where ibmm2 aligns 10->7, actullay, it is not that
common u'principles' is translated into u'haben'. However, ibmm2 could not
use this information since it's single direction.


