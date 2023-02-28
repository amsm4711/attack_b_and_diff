import cipher_gost
import itertools

#программа вскрывает нулевой столбец раундового ключа ГОСТ Кузнечик
key = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 54, 0,15], [25, 0, 1, 1],
                               [0, 0, 0, 0], [0, 0, 0, 3], [0, 32, 0, 12], [25, 0, 1, 1]]

cipher = cipher_gost.gost(key=key, col = 3)

#частичный ключ
def simple_swap(x0, x1): #функция обмена
    x_r = x1
    for i in range(len(x0)):
        for j in range(len(x0[i])):
            if x0[i][j] != x1[i][j]:
                x_r[i][j] = x0[i][j]
                return x_r

def summ_matr(A : list,B : list):
    C = [[0 for i in range(len(B[0]))] for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            C[i][j] = A[i][j] ^ B[i][j]
    return C

def get_indexes_keys(n_round, k2):
    k=[]
    j=[]
    l=[]
    for i in range(256):
        #третий столбец
        p0 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        p1 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        p0[0][3] = i
        p1[2][3] = 1
        p1[0][3] = 1 ^ i
        if n_round == 1:
            succ_atack = summ_matr(cipher.encrypt(p0, 1), cipher.encrypt(p1, 1))
        else:
            pp0 = cipher.X(cipher.S_inv(cipher.LT_inv(p0)), k2)
            pp1 = cipher.X(cipher.S_inv(cipher.LT_inv(p1)), k2)
            succ_atack = summ_matr(cipher.encrypt(pp0, 2), cipher.encrypt(pp1, 2))
        if succ_atack[3][3] == 0:
            k.append(i)
        #первый столбец
        p0 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        p1 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        p0[1][1] = i
        p1[2][1] = 1
        p1[1][1] = 1 ^ i
        if n_round == 1:
            succ_atack = summ_matr(cipher.encrypt(p0, 1), cipher.encrypt(p1, 1))
        else:
            pp0 = cipher.X(cipher.S_inv(cipher.LT_inv(p0)), k2)
            pp1 = cipher.X(cipher.S_inv(cipher.LT_inv(p1)), k2)
            succ_atack = summ_matr(cipher.encrypt(pp0, 2), cipher.encrypt(pp1, 2))
        if succ_atack[3][3] == 0:
            j.append(i)
        #нулевой столбец
        p0 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        p1 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        p0[2][0] = i
        p1[3][0] = 1
        p1[2][0] = 1 ^ i
        if n_round == 1:
            succ_atack = summ_matr(cipher.encrypt(p0,1),cipher.encrypt(p1,1))
        else:
            pp0 = cipher.X(cipher.S_inv(cipher.LT_inv(p0)), k2)
            pp1 = cipher.X(cipher.S_inv(cipher.LT_inv(p1)), k2)
            succ_atack = summ_matr(cipher.encrypt(pp0, 2), cipher.encrypt(pp1, 2))
        #print("suc",succ_atack)
        if succ_atack[1][3] == 0: #берем последнюю, т, к. находится в последней строке и последнем столбце
            l.append(i)
    return (k, j, l)


def str_from_list(lst):
    s = ""
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            s += " " + str(lst[i][j])
    return s

def attack_1r():
    ind = 0
    count_0 = 0
    count_1 = 0
    count_3 = 0
    triple = get_indexes_keys(1, [])
    print(triple)
    for i in triple[2]:
        print(i)
        S = []
        p0 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        p1 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        p0[2][0] = i
        p1[3][0] = 1
        p1[2][0] = 1 ^ i
        succ_atack = summ_matr(cipher.encrypt(p0,1),cipher.encrypt(p1,1))
        #print("suc",succ_atack)
        #S = [([[0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]), ([[133, 76, 100, 1], [213, 89, 213, 177], [170, 11, 188, 118], [53, 94, 58, 117]], [[133, 76, 41, 142], [54, 130, 34, 96], [142, 234, 47, 189], [119, 135, 149, 39]]), ([[108, 92, 62, 95], [209, 9, 44, 198], [140, 236, 236, 211], [88, 198, 214, 139]], [[108, 92, 124, 83], [182, 150, 67, 133], [71, 149, 185, 153], [64, 180, 175, 188]]), ([[5, 28, 42, 173], [216, 111, 111, 82], [57, 208, 118, 156], [150, 5, 144, 238]], [[5, 28, 21, 236], [230, 140, 55, 209], [37, 48, 238, 207], [111, 224, 89, 148]]), ([[71, 242, 197, 68], [18, 125, 161, 147], [0, 134, 199, 129], [148, 167, 76, 194]], [[71, 242, 83, 14], [95, 45, 16, 182], [107, 142, 32, 230], [239, 194, 13, 208]])]
        count = 0
        if succ_atack[1][3] == 0 and i == 25:
            c0 = cipher.encrypt(p0,9)
            c1 = cipher.encrypt(p1,9)
            S.append((p0,p1,succ_atack))
            #S = [([[0, 0, 0, 0], [0, 0, 0, 0], [25, 0, 0, 0], [0, 0, 0, 0]],
            #  [[0, 0, 0, 0], [0, 0, 0, 0], [24, 0, 0, 0], [1, 0, 0, 0]],
            #  [[208, 112, 242, 102], [27, 41, 10, 0], [215, 184, 213, 184], [64, 252, 85, 105]]), (
            # [[199, 249, 172, 244], [89, 6, 225, 144], [14, 222, 59, 133], [186, 233, 41, 253]],
            # [[199, 249, 90, 138], [153, 23, 6, 4], [196, 15, 25, 197], [119, 162, 178, 96]],
            # [[217, 14, 129, 121], [238, 147, 114, 0], [244, 100, 132, 190], [66, 17, 112, 112]]), (
            # [[136, 108, 192, 141], [164, 17, 121, 2], [245, 203, 161, 126], [114, 181, 164, 251]],
            # [[136, 108, 247, 205], [14, 174, 222, 108], [95, 136, 37, 165], [137, 115, 7, 195]],
            # [[131, 31, 195, 118], [220, 113, 56, 0], [122, 137, 28, 66], [165, 73, 75, 14]]), (
            # [[215, 123, 194, 101], [1, 200, 102, 6], [213, 62, 84, 13], [40, 54, 87, 105]],
            # [[215, 123, 100, 188], [230, 16, 85, 136], [188, 184, 164, 141], [209, 101, 232, 30]],
            # [[42, 115, 13, 150], [230, 254, 202, 0], [108, 225, 242, 101], [215, 17, 93, 41]]), (
            # [[166, 215, 81, 157], [5, 151, 54, 194], [24, 119, 149, 36], [110, 4, 254, 88]],
            # [[166, 215, 142, 154], [84, 141, 202, 209], [120, 93, 59, 75], [9, 110, 111, 54]],
            # [[42, 47, 166, 118], [144, 143, 204, 0], [30, 64, 29, 127], [244, 163, 165, 93]])]
            while len(S) < 5 and i == 25:
                c0 = cipher.encrypt(p0, 9)
                c1 = cipher.encrypt(p1, 9)
                c0_r = simple_swap(c0, c1)
                c1_r = simple_swap(c1, c0)
                p0_r = cipher.decrypt(c0_r, 9)
                p1_r = cipher.decrypt(c1_r, 9)
                p0 = simple_swap(p0_r, p1_r)
                p1 = simple_swap(p1_r, p0_r)
                c0 = cipher.encrypt(p0,9)
                c1 = cipher.encrypt(p1,9)
                count += 1
                succ_atack = summ_matr(cipher.encrypt(p0,1),cipher.encrypt(p1,1))
                if succ_atack[1][3] == 0:
                    S.append((p0, p1, succ_atack))
                    print(S)
                    print(count)
            k_elems = range(256)
            keys = itertools.product(k_elems,repeat=3)
            ind = 0
            if i == 25:
                for var in keys:
                    ind = 0
                    ost_k_elems = range(256)
                    test_bytes = itertools.product(ost_k_elems,repeat=10)
                    for o_var in test_bytes:
                        pr_key = [[var[0], o_var[0], o_var[3], o_var[6]], [var[1], o_var[1], o_var[4], o_var[7]], [var[2], o_var[1]^54, o_var[5], o_var[6]^15], [var[2]^i, o_var[2], o_var[8], o_var[9]]]
                        print(pr_key)
                        succ_atack = []
                        for elem in S:
                            succ_atack = cipher.LT(summ_matr(cipher.S(summ_matr(elem[0], pr_key)), cipher.S(summ_matr(elem[1], pr_key))))
                            if succ_atack[1][3] != 0:
                                ind = -1
                            else:
                                ind = 1
                            if ind == -1:
                                break
                        #print(succ_atack[3][3])
                        if ind == 1:
                            print(pr_key)
                            for byte in range(256):
                                pr_key[0][0] = byte
                                print(pr_key)
                                cipher.roundkey[0] = pr_key
                                succ_atack = summ_matr(cipher.encrypt(S[1][0], 1), cipher.encrypt(S[1][1], 1))
                                if succ_atack == S[1][2]:
                                    return pr_key
                if ind == 1:
                    break

def attack_2r(k1):
    ind = 0
    count_0 = 0
    count_1 = 0
    count_3 = 0
    triple = get_indexes_keys(2,k1)
    print(triple)
    for i in triple[2]:
        print(i)
        S = []
        p0 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        p1 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        p0[2][0] = i
        p1[3][0] = 1
        p1[2][0] = 1 ^ i
        pp0 = cipher.X(cipher.S_inv(cipher.LT_inv(p0)), k)
        pp1 = cipher.X(cipher.S_inv(cipher.LT_inv(p1)), k)
        succ_atack = summ_matr(cipher.encrypt(pp0,2),cipher.encrypt(pp1,2))
        #print("suc",succ_atack)
        #S = [([[0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]), ([[133, 76, 100, 1], [213, 89, 213, 177], [170, 11, 188, 118], [53, 94, 58, 117]], [[133, 76, 41, 142], [54, 130, 34, 96], [142, 234, 47, 189], [119, 135, 149, 39]]), ([[108, 92, 62, 95], [209, 9, 44, 198], [140, 236, 236, 211], [88, 198, 214, 139]], [[108, 92, 124, 83], [182, 150, 67, 133], [71, 149, 185, 153], [64, 180, 175, 188]]), ([[5, 28, 42, 173], [216, 111, 111, 82], [57, 208, 118, 156], [150, 5, 144, 238]], [[5, 28, 21, 236], [230, 140, 55, 209], [37, 48, 238, 207], [111, 224, 89, 148]]), ([[71, 242, 197, 68], [18, 125, 161, 147], [0, 134, 199, 129], [148, 167, 76, 194]], [[71, 242, 83, 14], [95, 45, 16, 182], [107, 142, 32, 230], [239, 194, 13, 208]])]
        count = 0
        if succ_atack[1][3] == 0 and i == 25:
            print(pp0, pp1)
            c0 = cipher.encrypt(pp0,9)
            c1 = cipher.encrypt(pp1,9)
            S.append((p0,p1,succ_atack))
            S=[([[0, 0, 0, 0], [0, 0, 0, 0], [25, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [24, 0, 0, 0], [1, 0, 0, 0]], [[208, 112, 242, 102], [27, 41, 10, 0], [215, 184, 213, 184], [64, 252, 85, 105]]), ([[61, 230, 85, 169], [254, 203, 13, 43], [84, 76, 132, 122], [234, 211, 139, 23]], [[218, 81, 177, 155], [3, 50, 249, 2], [225, 20, 190, 98], [139, 110, 192, 120]], [[233, 58, 203, 48], [191, 187, 71, 0], [86, 39, 32, 113], [188, 235, 37, 239]]), ([[54, 133, 50, 52], [181, 147, 98, 19], [146, 174, 128, 252], [218, 219, 118, 35]], [[15, 232, 192, 232], [220, 145, 198, 38], [194, 144, 31, 40], [6, 188, 118, 4]], [[254, 33, 24, 222], [117, 120, 145, 0], [147, 76, 13, 74], [62, 130, 143, 118]]), ([[50, 86, 251, 195], [245, 137, 179, 83], [143, 204, 112, 112], [45, 202, 52, 56]], [[69, 225, 157, 98], [94, 111, 145, 146], [23, 12, 225, 136], [184, 64, 209, 164]], [[165, 87, 42, 60], [122, 148, 43, 0], [172, 186, 170, 149], [210, 216, 82, 251]]), ([[79, 110, 253, 57], [115, 175, 62, 34], [212, 154, 1, 129], [0, 13, 42, 34]], [[149, 251, 144, 234], [9, 74, 39, 254], [100, 73, 204, 114], [25, 97, 122, 148]], [[25, 238, 185, 53], [170, 52, 104, 0], [34, 64, 173, 133], [111, 180, 52, 13]])]
            while len(S) < 5 and i == 25:
                c0 = cipher.encrypt(pp0, 9)
                c1 = cipher.encrypt(pp1, 9)
                c0_r = simple_swap(c0, c1)
                c1_r = simple_swap(c1, c0)
                p0_r = cipher.decrypt(c0_r, 9)
                p1_r = cipher.decrypt(c1_r, 9)
                pp0 = simple_swap(p0_r, p1_r)
                pp1 = simple_swap(p1_r, p0_r)
                c0 = cipher.encrypt(pp0,9)
                c1 = cipher.encrypt(pp1,9)
                count += 1
                succ_atack = summ_matr(cipher.encrypt(pp0,2),cipher.encrypt(pp1,2))
                if succ_atack[1][3] == 0:
                    S.append((cipher.encrypt(pp0,1), cipher.encrypt(pp1,1), succ_atack))
                    print(S)
                    print(count)
            k_elems = range(256)
            keys = itertools.product(k_elems,repeat=3)
            ind = 0
            if i == 25:
                for var in keys:
                    ind = 0
                    ost_k_elems = range(256)
                    test_bytes = itertools.product(ost_k_elems,repeat=10)
                    for o_var in test_bytes:
                        pr_key = [[var[0], o_var[0], o_var[3], o_var[6]], [var[1], o_var[1], o_var[4], o_var[7]], [var[2], o_var[1]^32, o_var[5], o_var[6]^12], [var[2]^i, o_var[2], o_var[8], o_var[9]]]
                        print(pr_key)
                        succ_atack = []
                        for elem in S:
                            succ_atack = cipher.LT(summ_matr(cipher.S(summ_matr(elem[0], pr_key)), cipher.S(summ_matr(elem[1], pr_key))))
                            if succ_atack[1][3] != 0:
                                ind = -1
                            else:
                                ind = 1
                            if ind == -1:
                                break
                        #print(succ_atack[3][3])
                        if ind == 1:
                            print(pr_key)
                            for byte in range(256):
                                pr_key[0][0] = byte
                                print(pr_key)
                                succ_atack = summ_matr(cipher.LT(cipher.S(cipher.X(S[1][0],pr_key))),cipher.LT(cipher.S(cipher.X(S[1][1],pr_key))))
                                if succ_atack == S[1][2]:
                                    return pr_key
                if ind == 1:
                    break




if __name__ == '__main__':
    c1 = cipher.LT([[38, 105, 39, 171], [99, 196, 138, 238], [139, 33, 16, 72], [26, 190, 248, 255]])
    #c2 = cipher.LT([[38, 105, 39, 171], [0,0,0,0], [0,0,0,0], [0,0,0,0]])
    #k = attack_1r()
    k = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 54, 0, 15], [25, 0, 1, 1]]
    print("k1=",k)
    k2 = attack_2r(k)
    print("k2=",k2)
