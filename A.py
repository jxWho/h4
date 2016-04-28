import nltk
import os

# TODO: Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
    ibm = nltk.IBMModel1(aligned_sents, 10)
    return ibm

# TODO: Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
    ibm = nltk.IBMModel2(aligned_sents, 10)
    return ibm

# TODO: Compute the average AER for the first n sentences
#       in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
    result = 0.0
    for i in range(n):
        x = aligned_sents[i]
        result += x.alignment_error_rate(model.align(x))
    return result / n

# TODO: Computes the alignments for the first 20 sentences in
#       aligned_sents and saves the sentences and their alignments
#       to file_name. Use the format specified in the assignment.
def save_model_output(aligned_sents, model, file_name):
    path = file_name
    with open(path, "w") as f:
        for i in range(20):
            x = model.align(aligned_sents[i])
            print >> f, x.words
            print >> f, x.mots
            print >> f, x.alignment
            print >> f, ''

def main(aligned_sents):
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)

    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
