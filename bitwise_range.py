from __future__ import print_function

import json


''''
1000 <= tcp_dst <= 1999

0000001111101000
0000011111001111

0000001111101xxx
000000111111xxxx
0000010xxxxxxxxx
00000110xxxxxxxx
000001110xxxxxxx
0000011110xxxxxx
000001111100xxxx

tcp,tp_src=0x03e8/0xfff8
tcp,tp_src=0x03f0/0xfff0
tcp,tp_src=0x0400/0xfe00
tcp,tp_src=0x0600/0xff00
tcp,tp_src=0x0700/0xff80
tcp,tp_src=0x0780/0xffc0
tcp,tp_src=0x07c0/0xfff0
'''



class BitwiseRange(object):
    """
    """

    def __init__(self, A, B, bits):
        self.A = A
        self.B = B
        self.total_bits = bits
        self.sA = self._str(A)  # '0000001111101000'
        self.sB = self._str(B)  # '0000011111001111'

        self.res_list = []

        self._handle()


    def _handle(self):
        # A > B
        if self.A > self.B:
            return

        # A == B
        if self.A == self.B:
            self._append_res(self.A, 0)
            return

        for i in range(0, self.total_bits):
            if self.sA[i] != self.sB[i]:
                self.first_diff_index = i
                break

        # only the last (lowest) bit is different. 2 result: A, B
        if self.first_diff_index == self.total_bits - 1:
            self._append_res(self.A, 0)
            self._append_res(self.B, 0)
            return

        # from first_diff_index, A all 0 and B all 1, a big result
        if '1' not in self.sA[self.first_diff_index:] and \
            '0' not in self.sB[self.first_diff_index:]:
            self._append_res(self.A, self.total_bits - self.first_diff_index)
            return

        # 2 parts, a_top: all bits after first_diff_index is 1
        #self.a_top = 2 ** (self.total_bits - self.first_diff_index - 1) - 1  # 0000001111111111
        sa_top = self.sA[0:self.first_diff_index+1] + '1' * (self.total_bits - self.first_diff_index - 1)
        self.a_top = int(sa_top, base=2)
        self.b_bottom = self.a_top + 1                                       # 0000010000000000

        self._part1()
        self._part2()


    def _str(self, n):
        return "{0:0{1}b}".format(n, self.total_bits)


    # temp
    '''
    def _append_res(self, numStr, freeBits):
        """
        '0000001111101000'  len: 16
        3
        """

        s = numStr[0:(self.total_bits-freeBits)] + 'x' * freeBits
        self.res_list.append(s)
    '''
    def _append_res(self, num, freeBits):
        self.res_list.append((num, freeBits))


    def _part1(self):
        a = self.A
        s = self._str(a)


        # special: A == 0, cannot do rindex('1')
        if a == 0:
            freeBits = self.total_bits - self.first_diff_index - 1
            self._append_res(a, freeBits)
            return  # end


        # TODO: in common way
        if s.endswith('1'):
            self._append_res(a, 0)
            a += 1
            s = self._str(a)


        while True:
            if a > self.a_top:
                break

            # find tail '0's
            i = s.rfind('1')
            if (i < 0) or (i < self.first_diff_index):
                i = self.first_diff_index

            freeBits = self.total_bits - i - 1
            self._append_res(a, freeBits)
            a += 2 ** freeBits
            s = self._str(a)


    def _part2(self):
        b = self.b_bottom  # 0000010000000000
        s = self._str(b)

        # '0000010000000000'
        # '0000011111001111'

        index = self.first_diff_index + 1

        while True:
            if index >= self.total_bits:
                break

            # special: from here, B all 1, all free bits
            if '0' not in self.sB[index:self.total_bits]:
                self._append_res(b, self.total_bits - index)
                break  # end

            # special: from here, B all 0, only one result
            if '1' not in self.sB[index:self.total_bits]:
                self._append_res(b, 0)
                break  # end

            # common
            if self.sB[index] == '1':
                self._append_res(b, self.total_bits - index - 1)
                b += 2 ** (self.total_bits - index - 1)
                s = self._str(b)
                index += 1
            else:  # sB[index] is '0'
                index += 1


    def print_result(self):
        for i in self.res_list:
            print(i)


    def print_result_x(self):
        for (num, freeBits) in self.res_list:
            s = self._str(num)[0:(self.total_bits-freeBits)] + 'x' * freeBits
            print(s)


    def print_result_hex(self):
        #if self.total_bits % 4 != 0:
        #    raise Exception("total_bits % 4 != 0")

        #chars = self.total_bits / 4

        for (num, freeBits) in self.res_list:
            maskStr = '1' * (self.total_bits - freeBits) + '0' * freeBits
            mask = int(maskStr, base=2)
            num = num & mask
            print("{}/{}".format(hex(num), hex(mask)))







class BitwiseIPv4Range(BitwiseRange):
    """
    """

    def __init__(self, ipA, ipB):
        self.A = self._ipv4_to_int(ipA)
        self.B = self._ipv4_to_int(ipB)
        self.total_bits = 32
        self.sA = self._str(self.A)  # '0000001111101000'
        self.sB = self._str(self.B)  # '0000011111001111'

        #print(self.A)
        #print(self.B)
        #print(self.sA)
        #print(self.sB)

        self.res_list = []

        self._handle()


    def _ipv4_to_int(self, s):
        l = s.split('.')
        num = (int(l[0]) << 24) + \
              (int(l[1]) << 16) + \
              (int(l[2]) << 8) + \
              (int(l[3]))

        return num


    def print_result_ipv4(self):
        #if self.total_bits != 32:
        #    raise Exception("total_bits != 32")

        for (num, freeBits) in self.res_list:
            maskStr = '1' * (self.total_bits - freeBits) + '0' * freeBits
            mask = int(maskStr, base=2)
            num = num & mask

            ip4 = num & 0xff
            ip3 = (num >> 8) & 0xff
            ip2 = (num >> 16) & 0xff
            ip1 = (num >> 24) & 0xff

            print("{}.{}.{}.{}/{}".format(ip1, ip2, ip3, ip4, self.total_bits - freeBits))




def test():
    #print(_ipv4_to_int("0.0.0.1"))

    #r = BitwiseRange(1000, 1999, 16)

    #r = BitwiseRange(1000, 1001, 16)
    r = BitwiseRange(0b000,
                     0b111, 3)

    #r.print_result_x()
    #r.print_result_hex()

    r = BitwiseIPv4Range("0.0.0.0", "0.0.255.255")
    r.print_result_ipv4()


if __name__ == "__main__":
    test()

