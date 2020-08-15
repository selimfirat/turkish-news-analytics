import numpy as np
from scipy.sparse import coo_matrix
def shingling(text, n):
    l = len(text) if type(text) is str else 0
    return set([text[i:i+n] for i in range(l - n + 1)])


def matrix_representation(S):
    nS = set()
    for s in S:
        nS |= s

    rows = []
    cols = []
    data = []

    i = 0
    ei = {}
    for si in range(len(S)):
        s = S[si]
        for el in s:
            if el not in ei:
                ei[el] = i
                i += 1

            ind = ei[el]
            rows.append(ind)
            cols.append(si)
            data.append(1)

    M = coo_matrix((data, (rows, cols)), shape=[len(nS), len(S)])

    return M

def iterative_hash_matrix(M, n):
    """
    :param M: matrix representation of sets
    :param n: number of hash functions
    :return: signature matrix
    """

    l = M.shape[0]
    P = np.arange(l)

    H = np.zeros([l, n], dtype=np.uint32)  # np.full([l, n], np.inf)

    dh = np.vectorize(lambda x: x + 7)
    H[:, 0] = dh(P) % l

    i = np.arange(1, n)
    dhp = dh(P).reshape((-1, 1))
    H[:, i] = np.add(H[:, i - 1], np.tile(dhp, n-1)) % l

    return H

def signature_matrix(M, H):
    G = np.full(H.T.shape, np.inf)
    for r in M:
        r
        idxs = np.nonzero(r)
        for idx in idxs:
            G[:, idx] = np.min(G[:, idx], H.T[:, idx])

    return G