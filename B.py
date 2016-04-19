import nltk
import A
from collections import defaultdict
from nltk.align import AlignedSent
import math

class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)


    #highly referred to the source code of IBM Model 2 on http://www.nltk.org/_modules/nltk/align/ibm2.html
    #returns the alignment result for one sentence pair
    def align(self, align_sent):
	al = []
	words = align_sent.words
	mots = align_sent.mots
	total_w = len(words)
	total_m = len(mots)
	for i, w in enumerate(words):
	    max_align_prob = (self.t[(w, None)] * self.q[(0, i+1, total_w, total_m)], None)
	    for j, m in enumerate(mots):
		#compute max prob
		max_align_prob = max(max_align_prob, (self.t[(w, m)]*self.q[(j+1, i+1, total_w, total_m)], j))
	    if max_align_prob[1] is not None:
		al.append((i, max_align_prob[1]))

	#for i in range(total_w):
	#    w = words[i]
	#    currentmax = (self.t[(w, None)] * self.q[(0, i+1, total_w, total_m)], None)
	#    for j in range(total_m):
	#	m = mots[j]
	#	currentmax = max((self.t[(w, m)] * self.q[(j+1, i+1, total_w, total_m)],j), currentmax)
	 #   if not currentmax[1] is None:
	return AlignedSent(words, mots, al)




    #highly referred to the source code of IBM Model 2 on http://www.nltk.org/_modules/nltk/align/ibm2.html
    #returns the translation and alignment probability distributions trained by EM algorithm
    def train(self, aligned_sents, num_iters):

	#t and q the returned parameters dictionaries
	#tr and qr the reverse direction
	#use defaultdict to avoid key not exist error
        t = defaultdict(lambda: 0.0)
        q = defaultdict(lambda: 0.0)
	tr = defaultdict(lambda: 0.0)
	qr = defaultdict(lambda: 0.0)

	#the following sets and dictionaries are used to count words and compute initial values of q and t
	#word_s and mot_s, all the vocab of each language
	word_s = set()
	mot_s = set()
	for sent in aligned_sents:
	    ws = sent.words
	    ms = sent.mots
	    m_l = len(ms)
	    w_l = len(ws)
	    word_s.update(ws)
	    mot_s.update(ms)

	    #initialize q
	    for i in range(m_l + 1):
		for j in range(w_l+1):
		    if i !=0 or j != 0:
			q[(i,j,w_l,m_l)] = 1.0/(m_l+1)
			qr[(i,j,w_l,m_l)] = 1.0/(w_l+1)

	#initialize t, the uniform distribution over all vocab appear
	total_w = len(word_s)
	total_m = len(mot_s)
	for w in word_s:
	    t[(w,None)] = 1.0 / (total_w + 1)
	for m in mot_s:
	    tr[(None, m)] = 1.0 / (total_m + 1)
	for sent in aligned_sents:
	    for w in sent.words:
		for m in sent.mots:
		    t[(w,m)] = 1.0 / (total_w + 1)
		    tr[(w,m)] = 1.0 / (total_m + 1)


	#EM algorithm
	for i in range(num_iters):
	    
	    w_totals = defaultdict(float)
	    m_totals = defaultdict(float)
	    ct_pair = defaultdict(float)
	    ct_w = defaultdict(lambda: 0.0)
	    ct_m = defaultdict(lambda: 0.0)
	    align_ct = defaultdict(lambda: 0.0)
	    align_w = defaultdict(lambda: 0.0)
	    align_m = defaultdict(lambda: 0.0)

	    for sent in aligned_sents:
		ws = [None] + sent.words
		total_w = len(ws) - 1
		#words.append(None)
		ms = [None] + sent.mots
		total_m = len(ms) - 1
		#mots.append(None)

		#compute normalization
		for j in range(1, total_w+1):
		    w = ws[j]
		    w_totals[w] = 0
		    for k in range(total_m+1):
			m = ms[k]
			w_totals[w] += t[(w, m)] * q[(k,j,total_w, total_m)]
		for j in range(1, total_m+1):
		    m = ms[j]
		    m_totals[m] = 0
		    for k in range(total_w+1):
			w = ws[k]
			m_totals[m] += tr[(w,m)] * qr[(j,k,total_w, total_m)]

		#collect counts
		for j in range(total_w+1):
		    w = ws[j]
		    for k in range(total_m+1):
			if k == 0 and j == 0:
			    continue
			m = ms[k]

			p1 = 0 if w_totals[w] == 0 else t[(w, m)] * q[(k,j,total_w, total_m)]/w_totals[w]
			p2 = 0 if m_totals[m] == 0 else tr[(w,m)] * qr[(k,j,total_w, total_m)]/m_totals[m]
			#take average of the two directions
			p = math.sqrt(p1 * p2)
		
			ct_pair[(w, m)] +=p
			ct_w[w] +=p
			ct_m[m] +=p
			align_ct[(k,j,total_w,total_m)] += p
			align_w[(j, total_w, total_m)] += p
			align_m[(k, total_w, total_m)] += p

	    #estimate probabilities
	    t = defaultdict(lambda: 0.0)
	    tr = defaultdict(lambda: 0.0)
	    q = defaultdict(lambda: 0.0)
	    qr = defaultdict(lambda: 0.0)
	
	    for sent in aligned_sents:
	        ws = [None] + sent.words
		total_w = len(ws) - 1
		#words.append(None)
		ms = [None] + sent.mots
		total_m = len(ms) - 1
		#mots.append(None)
			
		lp = 1.0

		for j in range(total_m + 1):
		    for k in range(1, total_w + 1):
			v = align_ct[(j, k, total_w, total_m)]
			if 0 < v < lp:
			    lp = v
		lp *= 0.5
		for j in range(total_m+1):
		    for k in range(1, total_w + 1):
			align_ct[(j, k, total_w, total_m)] += lp
		for j in range(1, total_w + 1):
		    align_w[(j, total_w, total_m)] += lp * total_w
		for j in range(1, total_m + 1):
		    align_m[(j, total_w, total_m)] += lp * total_m
	    for w in word_s:
		for m in mot_s:
		    c = ct_pair[(w, m)]	
		    if c > 0 and not ct_m[m] == 0:
			t[(w, m)] = c * 1.0 / ct_m[m]
		    if c > 0 and not ct_w[w] == 0:
			tr[(w, m)] = c * 1.0 / ct_w[w]
		#debugged to here


	    for sent in aligned_sents:
		words = [None] + sent.words
		total_w = len(words) - 1
		#words.append(None)
		mots = [None] + sent.mots
		total_m = len(mots) - 1
		#mots.append(None)
		for j in range(total_m + 1):
		    for k in range(total_w + 1):
			p = align_ct[(j, k, total_w, total_m)]
			if p > 0 and not align_w[(k, total_w, total_m)] == 0:
			    q[(j, k, total_w, total_m)] = p * 1.0 / align_w[(k, total_w, total_m)]
			if p > 0 and not align_m[(j, total_w, total_m)] == 0:
			    qr[(j, k, total_w, total_m)] = p * 1.0 / align_m[(j, total_w, total_m)]

        return (t,q)

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
