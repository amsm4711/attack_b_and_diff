class Gelius2pow8:
    def __init__(self, val : int):
        self.val = 0
        self.val = val

    def get(self):
        return self.val

    def add(self, *args): #сложение элементов поля
        res = self.val
        for arg in args:
            res ^= arg.val
        return res

    def get_lead_bit_num(self): #получаем номер лидирующего бита
        if self.val == 0:
            print("Старший бит числа 0 нулевой")
            return 0
        else:
            bitnum = 31
            cmp_val = 1 << bitnum
            while (self.val < cmp_val):
                cmp_val >>= 1
                bitnum -= 1
            return bitnum

    def mult(self, m2):
        if self.val == 0 or m2.val == 0:
            return 0
        m1_tmp = self.val
        m1_bit_num = 0
        poly_rez = 0
        while m1_tmp != 0:
            if (m1_tmp & 1) == 0:
                bit_m1 = 0
            else:
                bit_m1 = 1
            m1_tmp >>= 1
            m2_tmp = m2.get()
            m2_bit_num = 0
            while m2_tmp != 0:
                if (m2_tmp & 1) == 0:
                    bit_m2 = 0
                else:
                    bit_m2 = 1
                m2_tmp >>= 1
                if (bit_m1 != 0) and (bit_m2 != 0):
                    bit_num = int(m2_bit_num + m1_bit_num)
                    poly_rez ^= 1 << bit_num
                m2_bit_num += 1
            m1_bit_num += 1
        #конец перемножения, теперь ищем остаток
        tmp_divisor = 451
        tmp_divisor_lead_bit_n = Gelius2pow8(451).get_lead_bit_num()
        tmp_divident = poly_rez
        tmp_divident_lead_bit_num = Gelius2pow8(tmp_divident).get_lead_bit_num()
        while (tmp_divident_lead_bit_num >= tmp_divisor_lead_bit_n):
            TmpQuotient = tmp_divident_lead_bit_num - tmp_divisor_lead_bit_n
            TmpMult_bitNum = 0
            TmpMult_rez = 0
            while (tmp_divisor != 0):
                if tmp_divisor & 1 == 0:
                    bit_TmpMult = 0
                else:
                    bit_TmpMult = 1
                tmp_divisor  >>= 1
                TmpMult_rez ^= bit_TmpMult << int(TmpQuotient + TmpMult_bitNum)
                TmpMult_bitNum = TmpMult_bitNum + 1
            tmp_divident = tmp_divident ^ TmpMult_rez
            tmp_divisor = 451
            tmp_divident_lead_bit_num = Gelius2pow8(tmp_divident).get_lead_bit_num()
        return tmp_divident

    def inverse_elem(self):
        for m2 in range(1,256):
            if self.mult(Gelius2pow8(m2)) == 1:
                return m2
        return -1

    def derive(self, m2):
        if m2.val == 0:
            print("На нуль делить нельзя!!!")
        else:
            return self.mult(Gelius2pow8(m2.inverse_elem()))

A = Gelius2pow8(2)
B = Gelius2pow8(16)
print(1^1)