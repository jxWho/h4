import nltk
import A
from collections import defaultdict
import math

class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # TODO: Computes the alignments for align_sent, using this model's parameters. Return
    #       an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
        pass

    # TODO: Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
        t = {}
        q = {}

        DE_PROB = 1.0e-12
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

            for i in range(word_length + 1):
                for j in range(mot_length+1):
                    q[(j, i, mot_length, word_length)] = 1.0 / (mot_length + 1)
                    qr[(i, j, word_length, mot_length)] = 1.0 / (word_length + 1)
        word_cnt = len(words)
        mot_cnt = len(mots)
        # initialize t(e, f)
        for s in aligned_sents:
            for w in s.words:
                for m in s.mots:
                    t[(w, m)] = 1.0 / (word_cnt + 1.0)
                    tr[(m, w)] = 1.0 / (mot_cnt + 1.0)
        # the None combination
        for word in words:
            t[(word, None)] = 1.0 / (word_cnt + 1.0)
        for word in mots:
            tr[(word, None)] = 1.0 / (mot_cnt + 1.0)

        # Iteration for EM
        for _ in range(num_iters):
            c_ef = defaultdict(lambda: 0.0)
            c_e = defaultdict(lambda: 0.0)
            c_jilm = defaultdict(lambda: 0.0)
            c_ilm = defaultdict(lambda: 0.0)

            c_ef2 = defaultdict(lambda: 0.0)
            c_e2 = defaultdict(lambda: 0.0)
            c_jilm2 = defaultdict(lambda: 0.0)
            c_ilm2 = defaultdict(lambda: 0.0)

            for s in aligned_sents:
                total_cnt = defaultdict(float)
                total_cnt2 = defaultdict(float)
                m = len(s.words)
                # french
                new_words = [None] + s.words
                l = len(s.mots)
                # English
                new_mots = [None] + s.mots

            # normalization
                # model words -> mots
                for i in range(1, m + 1):
                    from_word = new_words[i]
                    total_cnt[from_word] = 0
                    for j in range(mot_length + 1):
                        to_word = new_mots[j]
                        count = t[(from_word, to_word)] * q[(j,i,l,m)]
                        total_cnt[from_word] += count

                # model mots -> words
                for i in range()

            # collect counts
                for i in range(1, m + 1):
                    f = new_words[i]
                    for j in range(0, l + 1):
                        e = new_mots[j]
                        temp = q[(j, i, l, m)] * t[(f, e)]
                        temp /= total_cnt[f]
                        c_ef[(e, f)] += temp
                        c_e[e] += temp
                        c_jilm[(j, i, l, m)] += temp
                        c_ilm[(i, l, m)] += temp

            # update parameters
            for f in words:
                for e in [None] + mots:
                    temp = c_ef[(e, f)] / c_e[e]
                    t[(e, f)] = max(temp, DE_PROB)

            for s in aligned_sents:
                l = len(s.mots)
                m = len(s.words)
                for i in range(1, m+1):
                    for j in range(l+1):
                        temp = c_jilm[(j, i, l, m)] * 1.0 / (1.0 * c_ilm(i, l, m))
                        q[(j, i, l, m)] = max(temp, DE_PROB)



        return (t,q)

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
