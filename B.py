import nltk
from collections import defaultdict
from nltk.align import AlignedSent
from nltk.align import Alignment
import math
import A

class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # TODO: Computes the alignments for align_sent, using this model's parameters. Return
    #       an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
        LOWER_PROB = 1.0e-12
        best_alignment = []

        words = align_set.words
        mots = align_set.mots
        m_len = len(align_set.mots)
        w_len = len(align_sent.words)

        for i, w in enumerate(words):
            maxAlignProb = (self.t[(w, None)] * self.q[(0, i+1, w_len, m_len)], None)
            for j, m in enumerate(mots):
                maxAlignProb = max(maxAlignProb, (self.t[(w, m)]*self.q[(j+1, i+1, total_w, total_m)], j) )

            if maxLaignProb[1] is not None:
                best_alignment.append((i, maxLaignProb[1]))


        return AlignedSent(words, mots, best_alignment)



    # TODO: Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
        t = {}
        q = {}
        # words -> mots
        t = defaultdict(lambda: 0.0)
        q = defaultdict(lambda: 0.0)
        # mots -> words
        tr = defaultdict(lambda: 0.0)
        qr = defaultdict(lambda: 0.0)

        words = set()
        mots = set()
        # intialize q(i, j, l, m)
        for s in aligned_sents:
            words.update(s.words)
            mots.update(s.mots)
            word_length = len(s.words)
            mot_length = len(s.mots)

            for j in range(word_length + 1):
                for i in range(mot_length+1):
                    q[(i, j, word_length, mot_length)] = 1.0 / (mot_length + 1)
                    qr[(i, j, word_length, mot_length)] = 1.0 / (word_length + 1)
        word_cnt = len(words)
        mot_cnt = len(mots)
        # initialize t(e, f)
        for s in aligned_sents:
            for w in s.words:
                for m in s.mots:
                    t[(w, m)] = 1.0 / (word_cnt + 1.0)
                    tr[(w, m)] = 1.0 / (mot_cnt + 1.0)
        # the None combination
        for word in words:
            t[(word, None)] = 1.0 / (word_cnt + 1.0)
        for word in mots:
            tr[(None, word)] = 1.0 / (mot_cnt + 1.0)

        # Iteration for EM
        for _ in range(num_iters):
            w_cnt = default(float)
            m_cnt = default(float)

            c_ef = defaultdict(lambda: 0.0)
            c_e = defaultdict(lambda: 0.0)
            c_f = defaultdict(lambda: 0.0)
            c_jilm = defaultdict(lambda: 0.0)
            c_ilm_w = defaultdict(lambda: 0.0)
            c_ilm_m = defaultdict(lambda: 0.0)

            for s in aligned_sents:
                word_len = len(s.words)
                # french
                new_words = [None] + s.words
                mot_len  = len(s.mots)
                # English
                new_mots = [None] + s.mots

            # normalization
                # model words -> mots
                for i in range(1,  word_len + 1):
                    from_word = new_words[i]
                    w_cnt[from_word] = 0
                    for j in range(mot_len + 1):
                        to_word = new_mots[j]
                        count = t[(from_word, to_word)] * q[(j,i,word_len,mot_len)]
                        w_cnt[from_word] += count
                # model mots -> words
                for j in range(1, mot_len + 1):
                    from_word = new_mots[j]
                    m_cnt[from_word] = 0
                    for i in range(word_len + 1):
                        to_word = new_words[i]
                        count = tr[(to_word, from_word)] * qr[(j, i, word_len, mot_len)]
                        m_cnt[from_word] += count


                for i in range(word_len + 1):
                    w = new_words[i]
                    for j in range(mot_len + 1):
                        if i == 0 and j == 0:
                            # no aligenment for (None, None)
                            continue
                        m = new_mots[j]
                        if w_cnt[w] == 0:
                            p1 = 0
                        else:
                            p1 = t[(w, m)] * q[(j, i, word_len, mot_len)]
                            p1 /= w_cnt[w]

                        if m_cnt[m] == 0:
                            p2 = 0
                        else:
                            p2 = tr[(w, m)] * q[(j, i, word_len, mot_len)]
                            p2 /= m_cnt[m]

                        # take average
                        p = math.sqrt(p1 * p2)

                        c_ef[(w, m)] += p
                        c_e[m] += p
                        c_f[w] += p
                        c_jilm[(j,i,word_len, mot_len)] += p
                        c_ilm_w[(i, word_len, mot_len)] += p
                        c_ilm_m[(j, word_len, mot_len)] += p


            # update parameters
            for w in words:
                for m in mots:
                    temp = c_ef[(e, f)]
                    if temp > 0 and c_e[m] != 0:
                        t[(w, m)] = temp * 1.0 / c_e[m]
                    if temp > 0 and c_f[w] != 0:
                        tr[(w, m)] = temp * 1.0 / c_f[w]

            for s in aligned_sents:
                words = [None] + s.words
                w_len = len(words) - 1
                mots = [None] + s.mots
                m_len = len(mots) - 1

                for j in range(m_len+1):
                    for i in range(w_len+1):
                        temp = f_jilm[(j, i, w_len, m_len)]
                        if temp > 0 and c_ilm_w[(i, w_len, m_len)] != 0:
                            q[(j, i, w_len, m_len)] = temp * 1.0 / c_ilm_w[(i, w_len, m_len)]
                        if temp > 0 and c_ilm_m[(j, w_len, m_len)] != 0:
                            qr[(j, i, w_len, m_len)] = temp * 1.0 / c_ilm_m[(j, w_len, m_len)]

        return (t,q)

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
