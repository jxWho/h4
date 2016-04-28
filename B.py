import nltk
import A
from collections import defaultdict
from nltk.align import AlignedSent
from nltk.align import Alignment
import math

class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    def align(self, align_sent):
        MIN_PROB = 1.0e-12
        best_alignment = []

        l = len(align_sent.mots)
        m = len(align_sent.words)

        for j, trg_word in enumerate(align_sent.words):
            # Initialize trg_word to align with the NULL token
            best_prob = (self.t[trg_word][None] * self.q[0][j + 1][l][m])
            best_prob = max(best_prob, MIN_PROB)
            best_alignment_point = 0
            for i, src_word in enumerate(align_sent.mots):
                align_prob = (self.t[trg_word][src_word] * self.q[i + 1][j + 1][l][m])
                if align_prob >= best_prob:
                    best_prob = align_prob
                    best_alignment_point = i
            best_alignment.append((j, best_alignment_point))

        new_sent = AlignedSent(align_sent.words,
                                align_sent.mots,
                                Alignment(best_alignment))
        return new_sent



    def train(self, aligned_sents, num_iters):
        DEFAULT_PROB = 1.0e-12
        #tr and qr for mots -> words
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
                ms = [None] + sent.mots
                total_m = len(ms) - 1

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

                        if w_totals[w] == 0:
                            p1 = DEFAULT_PROB
                        else:
                            p1 = \
                            t[(w, m)] * q[(k,j,total_w, total_m)]/w_totals[w]

                        if m_totals[m] == 0:
                            p2 = DEFAULT_PROB
                        else:
                            p2 = \
                            tr[(w,m)] * qr[(k,j,total_w, total_m)]/m_totals[m]
                        #take average of the two directions
                        p = math.sqrt(p1 * p2)
                        #p = 0.5 * p1 + 0.5 * p2

                        ct_pair[(w, m)] +=p
                        ct_w[w] +=p
                        ct_m[m] +=p
                        align_ct[(k,j,total_w,total_m)] += p
                        align_w[(j, total_w, total_m)] += p
                        align_m[(k, total_w, total_m)] += p

            # update parameters
            for sent in aligned_sents:
                ws = [None] + sent.words
            total_w = len(ws) - 1
            ms = [None] + sent.mots
            total_m = len(ms) - 1

            for w in word_s:
                for m in mot_s:
                    c = ct_pair[(w, m)]
                    if c > 0 and not ct_m[m] == 0:
                        t[(w, m)] = c * 1.0 / ct_m[m]
                    if c > 0 and not ct_w[w] == 0:
                        tr[(w, m)] = c * 1.0 / ct_w[w]

            for sent in aligned_sents:
                words = [None] + sent.words
                total_w = len(words) - 1
                mots = [None] + sent.mots
                total_m = len(mots) - 1

                for j in range(total_m + 1):
                    for k in range(total_w + 1):
                        p = align_ct[(j, k, total_w, total_m)]
                        if p > 0 and not align_w[(k, total_w, total_m)] == 0:
                            q[(j, k, total_w, total_m)] = p * 1.0 / align_w[(k, total_w, total_m)]
                        if p > 0 and not align_m[(j, total_w, total_m)] == 0:
                            qr[(j, k, total_w, total_m)] = p * 1.0 / align_m[(j, total_w, total_m)]

        # change the format of t and q
        # so that we can use the default alignment method
        # from nltk
        new_t = defaultdict(lambda: defaultdict(lambda: DEFAULT_PROB ))
        new_q = defaultdict(
                lambda: defaultdict(lambda: defaultdict(
                    lambda:defaultdict(lambda: DEFAULT_PROB ))))
        for w, m in t.keys():
           new_t[w][m] = t[(w,m)]
        for i, j, lw, lm in q.keys():
            new_q[i][j][lm][lw] = q[(i, j, lw, lm)]

        t = new_t
        q = new_q
        return (t,q)

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
