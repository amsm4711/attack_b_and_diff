import gelius

#вспомогательные функции для реализации операций с матрицами текстов в поле
def transpose(p):
    c = []
    for i in range(len(p)):
        row = []
        for j in range(len(p[i])):
            row.append(p[j][i])
        c.append(row)
    return c

def multi_matr(A : list,B : list):
    C = [[0 for i in range(len(B[0]))] for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            C[i][j] = 0
            for k in range(len(A[0])):
                a = gelius.Gelius2pow8(A[i][k])
                b = gelius.Gelius2pow8(B[k][j])
                C[i][j] ^= a.mult(b)
    return C

def pow_matr(A,n):
    res = A
    for i in range(n-1): #возведение в степень
        res = multi_matr(res,A)
    return res

def skal_multi(A, l):
    res = []
    l0 = gelius.Gelius2pow8(l)
    for i in range(len(A)):
        row = []
        for j in range(len(A[i])):
            a = gelius.Gelius2pow8(A[i][j])
            row.append(a.mult(l0))
        res.append(row)
    return res

def xor_matr(*args):
    res = []
    for i in range(len(args[0])):
        row = []
        for j in range(len(args[0])):
            res_s = 0
            for arg in args:
                res_s ^= arg[i][j]
            row.append(res_s)
        res.append(row)
    return res

def one(k,l):
    e = []
    for i in range(4):
        row = []
        for j in range(4):
            if i == k and j == l:
                row.append(1)
            else:
                row.append(0)
        e.append(row)
    return e

def W(a, i, j):
    return xor_matr(skal_multi(one(0,j),a[0][i]), skal_multi(one(1,j),a[1][i]), skal_multi(one(2,j),a[2][i]), skal_multi(one(3,j),a[3][i]))

class gost:
    def __init__(self, key, col):
        self.key = key
        self.C = [[110, 162, 118, 114, 108, 72, 122, 184, 93, 39, 189, 16, 221, 132, 148, 1],
                  [220, 135, 236, 228, 216, 144, 244, 179, 186, 78, 185, 32, 121, 203, 235, 2],
                  [178, 37, 154, 150, 180, 216, 142, 11, 231, 105, 4, 48, 164, 79, 127, 3],
                  [123, 205, 27, 11, 115, 227, 43, 165, 183, 156, 177, 64, 242, 85, 21, 4],
                  [21, 111, 109, 121, 31, 171, 81, 29, 234, 187, 12, 80, 47, 209, 129, 5],
                  [167, 74, 247, 239, 171, 115, 223, 22, 13, 210, 8, 96, 139, 158, 254, 6],
                  [201, 232, 129, 157, 199, 59, 165, 174, 80, 245, 181, 112, 86, 26, 106, 7],
                  [246, 89, 54, 22, 230, 5, 86, 137, 173, 251, 161, 128, 39, 170, 42, 8],
                  [152, 251, 64, 100, 138, 77, 44, 49, 240, 220, 28, 144, 250, 46, 190, 9],
                  [42, 222, 218, 242, 62, 149, 162, 58, 23, 181, 24, 160, 94, 97, 193, 10],
                  [68, 124, 172, 128, 82, 221, 216, 130, 74, 146, 165, 176, 131, 229, 85, 11],
                  [141, 148, 45, 29, 149, 230, 125, 44, 26, 103, 16, 192, 213, 255, 63, 12],
                  [227, 54, 91, 111, 249, 174, 7, 148, 71, 64, 173, 208, 8, 123, 171, 13],
                  [81, 19, 193, 249, 77, 118, 137, 159, 160, 41, 169, 224, 172, 52, 212, 14],
                  [63, 177, 183, 139, 33, 62, 243, 39, 253, 14, 20, 240, 113, 176, 64, 15],
                  [47, 178, 108, 44, 15, 10, 172, 209, 153, 53, 129, 195, 78, 151, 84, 16],
                  [65, 16, 26, 94, 99, 66, 214, 105, 196, 18, 60, 211, 147, 19, 192, 17],
                  [243, 53, 128, 200, 215, 154, 88, 98, 35, 123, 56, 227, 55, 92, 191, 18],
                  [157, 151, 246, 186, 187, 210, 34, 218, 126, 92, 133, 243, 234, 216, 43, 19],
                  [84, 127, 119, 39, 124, 233, 135, 116, 46, 169, 48, 131, 188, 194, 65, 20],
                  [58, 221, 1, 85, 16, 161, 253, 204, 115, 142, 141, 147, 97, 70, 213, 21],
                  [136, 248, 155, 195, 164, 121, 115, 199, 148, 231, 137, 163, 197, 9, 170, 22],
                  [230, 90, 237, 177, 200, 49, 9, 127, 201, 192, 52, 179, 24, 141, 62, 23],
                  [217, 235, 90, 58, 233, 15, 250, 88, 52, 206, 32, 67, 105, 61, 126, 24],
                  [183, 73, 44, 72, 133, 71, 128, 224, 105, 233, 157, 83, 180, 185, 234, 25],
                  [5, 108, 182, 222, 49, 159, 14, 235, 142, 128, 153, 99, 16, 246, 149, 26],
                  [107, 206, 192, 172, 93, 215, 116, 83, 211, 167, 36, 115, 205, 114, 1, 27],
                  [162, 38, 65, 49, 154, 236, 209, 253, 131, 82, 145, 3, 155, 104, 107, 28],
                  [204, 132, 55, 67, 246, 164, 171, 69, 222, 117, 44, 19, 70, 236, 255, 29],
                  [126, 161, 173, 213, 66, 124, 37, 78, 57, 28, 40, 35, 226, 163, 128, 30],
                  [16, 3, 219, 167, 46, 52, 95, 246, 100, 59, 149, 51, 63, 39, 20, 31],
                  [94, 167, 216, 88, 30, 20, 155, 97, 241, 106, 193, 69, 156, 237, 168, 32]]
        #self.null_column(col)
        self.roundkey = [key[:4], key[4:]]
        self.roundkey = self.roundkey + self.keyschedule(self.roundkey)

    def null_column(self, k):
        for i in range(4):
            for j in range(len(self.key[i])):
                if j != k:
                    self.key[i][j] = 0

    def X(self, p, key):
        C = []
        for i in range(len(p)):
            row = []
            for j in range(len(p[i])):
                row.append(p[i][j] ^ key[i][j])
            C.append(row)
        return C

    def S(self, p):
        pi = [252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77, 233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79, 5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52, 44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135, 21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177, 50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87, 223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3, 224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74, 167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65, 173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59, 7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137, 225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133, 97, 32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166, 116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182]
        C = []
        for i in range(len(p)):
            row = []
            for j in range(len(p[i])):
                row.append(pi[p[i][j]])
            C.append(row)
        return C

    def S_inv(self, C):
        pi_inv =   [165, 45, 50, 143, 14, 48, 56, 192, 84, 230, 158, 57, 85, 126, 82, 145, 100, 3, 87, 90, 28, 96, 7,
                      24, 33, 114, 168, 209, 41, 198, 164, 63, 224, 39, 141, 12, 130, 234, 174, 180, 154, 99, 73, 229,
                      66, 228, 21, 183, 200, 6, 112, 157, 65, 117, 25, 201, 170, 252, 77, 191, 42, 115, 132, 213, 195,
                      175, 43, 134, 167, 177, 178, 91, 70, 211, 159, 253, 212, 15, 156, 47, 155, 67, 239, 217, 121, 182,
                      83, 127, 193, 240, 35, 231, 37, 94, 181, 30, 162, 223, 166, 254, 172, 34, 249, 226, 74, 188, 53,
                      202, 238, 120, 5, 107, 81, 225, 89, 163, 242, 113, 86, 17, 106, 137, 148, 101, 140, 187, 119, 60,
                      123, 40, 171, 210, 49, 222, 196, 95, 204, 207, 118, 44, 184, 216, 46, 54, 219, 105, 179, 20, 149,
                      190, 98, 161, 59, 22, 102, 233, 92, 108, 109, 173, 55, 97, 75, 185, 227, 186, 241, 160, 133, 131,
                      218, 71, 197, 176, 51, 250, 150, 111, 110, 194, 246, 80, 255, 93, 169, 142, 23, 27, 151, 125, 236,
                      88, 247, 31, 251, 124, 9, 13, 122, 103, 69, 135, 220, 232, 79, 29, 78, 4, 235, 248, 243, 62, 61,
                      189, 138, 136, 221, 205, 11, 19, 152, 2, 147, 128, 144, 208, 36, 52, 203, 237, 244, 206, 153, 16,
                      68, 64, 146, 58, 1, 38, 18, 26, 72, 104, 245, 129, 139, 199, 214, 32, 10, 8, 0, 76, 215, 116]
        p = []
        for i in range(len(C)):
            row = []
            for j in range(len(C[i])):
                row.append(pi_inv[C[i][j]])
            p.append(row)
        return p

    def LT(self, p):
        p = transpose(p)
        #определяем индексы блока для блочной матрицы
        L_block = [[[207, 152, 116, 191], [110, 32, 198, 218], [162, 200, 135, 112], [118, 51, 16, 12]],
         [[147, 142, 242, 243], [144, 72, 137, 156], [104, 67, 28, 43], [28, 17, 214, 106]],
         [[10, 191, 246, 169], [193, 100, 184, 45], [161, 99, 48, 107], [166, 215, 246, 73]],
         [[234, 142, 77, 110], [134, 68, 208, 162], [159, 48, 227, 118], [7, 20, 232, 114]],
         [[114, 242, 107, 202], [108, 118, 236, 12], [72, 213, 98, 23], [122, 230, 78, 26]],
         [[32, 235, 2, 164], [197, 188, 175, 110], [6, 45, 196, 231], [187, 46, 241, 190]],
         [[141, 212, 196, 1], [163, 225, 144, 88], [213, 235, 153, 120], [212, 175, 55, 177]],
         [[101, 221, 76, 108], [14, 2, 195, 72], [82, 245, 22, 122], [212, 42, 110, 184]],
         [[184, 73, 135, 20], [93, 212, 184, 47], [39, 159, 190, 104], [189, 149, 94, 48]],
         [[203, 141, 171, 73], [141, 18, 238, 246], [26, 124, 173, 201], [233, 96, 191, 16]],
         [[9, 108, 42, 1], [8, 84, 15, 243], [132, 47, 235, 254], [239, 57, 236, 145]],
         [[96, 142, 75, 93], [152, 200, 127, 39], [198, 72, 162, 189], [127, 72, 137, 16]],
         [[16, 233, 208, 217], [221, 153, 117, 202], [132, 45, 116, 150], [148, 32, 133, 16]],
         [[243, 148, 61, 175], [151, 68, 90, 224], [93, 119, 111, 222], [194, 192, 1, 251]],
         [[123, 255, 100, 145], [48, 166, 49, 211], [84, 180, 141, 209], [1, 192, 194, 16]],
         [[82, 248, 13, 221], [223, 72, 100, 132], [68, 60, 165, 148], [133, 32, 148, 1]]]
        c0 = []
        for i in range(4): #заполняем нулями матрицу шифртекста
            row = []
            for j in range(4):
                row.append(0)
            c0.append(row)

        for i in range(4):
            for j in range(4):
                c0 = xor_matr(c0,multi_matr(L_block[4*i+j],W(p,j,i)))
        c = []
        for i in range(4):
            row = []
            for j in range(4):
                row.append(c0[j][i])
            c.append(row)
        return c

    def LT_inv(self, p):
        p = transpose(p)
        #определяем индексы блока для блочной матрицы
        L_block = [[[1, 148, 32, 133], [148, 165, 60, 68], [132, 100, 72, 223], [221, 13, 248, 82]],
         [[16, 194, 192, 1], [209, 141, 180, 84], [211, 49, 166, 48], [145, 100, 255, 123]],
         [[251, 1, 192, 194], [222, 111, 119, 93], [224, 90, 68, 151], [175, 61, 148, 243]],
         [[16, 133, 32, 148], [150, 116, 45, 132], [202, 117, 153, 221], [217, 208, 233, 16]],
         [[16, 137, 72, 127], [189, 162, 72, 198], [39, 127, 200, 152], [93, 75, 142, 96]],
         [[145, 236, 57, 239], [254, 235, 47, 132], [243, 15, 84, 8], [1, 42, 108, 9]],
         [[16, 191, 96, 233], [201, 173, 124, 26], [246, 238, 18, 141], [73, 171, 141, 203]],
         [[48, 94, 149, 189], [104, 190, 159, 39], [47, 184, 212, 93], [20, 135, 73, 184]],
         [[184, 110, 42, 212], [122, 22, 245, 82], [72, 195, 2, 14], [108, 76, 221, 101]],
         [[177, 55, 175, 212], [120, 153, 235, 213], [88, 144, 225, 163], [1, 196, 212, 141]],
         [[190, 241, 46, 187], [231, 196, 45, 6], [110, 175, 188, 197], [164, 2, 235, 32]],
         [[26, 78, 230, 122], [23, 98, 213, 72], [12, 236, 118, 108], [202, 107, 242, 114]],
         [[114, 232, 20, 7], [118, 227, 48, 159], [162, 208, 68, 134], [110, 77, 142, 234]],
         [[73, 246, 215, 166], [107, 48, 99, 161], [45, 184, 100, 193], [169, 246, 191, 10]],
         [[106, 214, 17, 28], [43, 28, 67, 104], [156, 137, 72, 144], [243, 242, 142, 147]],
         [[12, 16, 51, 118], [112, 135, 200, 162], [218, 198, 32, 110], [191, 116, 152, 207]]]
        c0 = []
        for i in range(4): #заполняем нулями матрицу шифртекста
            row = []
            for j in range(4):
                row.append(0)
            c0.append(row)

        for i in range(4):
            for j in range(4):
                c0 = xor_matr(c0,multi_matr(L_block[4*i+j],W(p,j,i)))
        c = []
        for i in range(4):
            row = []
            for j in range(4):
                row.append(c0[j][i])
            c.append(row)
        return c

    def encrypt(self,p,n):
        c = p
        for i in range(n):
            c = self.X(c,self.roundkey[i])
            c = self.S(c)
            c = self.LT(c)
        if n > 2:
            c = self.X(c, self.roundkey[n])
        return c

    def decrypt(self,p,n):
        c = p
        for i in range(n,0,-1):
            c = self.X(c,self.roundkey[i])
            c = self.LT_inv(c)
            c = self.S_inv(c)
        if n > 2:
            c = self.X(c, self.roundkey[0])
        return c

    def ftransformation(self, k, a : list):
        tmp = self.X(k, a[0])
        tmp = self.S(tmp)
        tmp = self.LT(tmp)
        tmp = self.X(tmp, a[1])
        return [tmp, a[0]]

    def keyschedule(self, roundkey):
        roundkeys = []
        for i in range(4):
            for k in range(8):
                Cl = self.C[8*i+k]
                C_matr = []
                C_matr.append(Cl[0:4])
                C_matr.append(Cl[4:8])
                C_matr.append(Cl[8:12])
                C_matr.append(Cl[12:16])
                roundkey = self.ftransformation(C_matr, roundkey)
            roundkeys.append(roundkey[0])
            roundkeys.append(roundkey[1])
        return roundkeys






