from __future__ import print_function

import json



class BitwiseRange(object):
    """
    Express a range of nonnegative integer as a set of bitwise stuff.
    The number of results is designed to be as few as possible.
    """

    def __init__(self, A, B, bits=0):
        """
        Args:
            <int> A: the smallest number in the range.
            <int> B: the biggest number in the range.
            [int] bits: max bits of a number, use (len(bin(B)) - 2) if not given.
        """

        self.A = A
        self.B = B

        if bits:
            self.total_bits = bits
        else:
            # bin(777) is '0b1100001001'
            self.total_bits = len(bin(B)) - 2

        self.sA = self._str(A)  # '0000001111101000'
        self.sB = self._str(B)  # '0000011111001111'

        self.res_list = []

        self._handle()


    def _handle(self):
        """
        Handle some special conditions here.
        """

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

        # from first_diff_index, A is all 0 and B is all 1. a big result
        if '1' not in self.sA[self.first_diff_index:] and \
            '0' not in self.sB[self.first_diff_index:]:
            self._append_res(self.A, self.total_bits - self.first_diff_index)
            return

        # split into 2 parts: A -> a_top, b_bottom -> B
        #   a_top: the bit on first_diff_index is 0, all bits after first_diff_index is 1.
        #   b_bottom: the bit on first_diff_index is 1, all bits after first_diff_index is 0.
        sa_top = self.sA[0:self.first_diff_index+1] + '1' * (self.total_bits - self.first_diff_index - 1)
        self.a_top = int(sa_top, base=2)
        self.b_bottom = self.a_top + 1

        self._part1()
        self._part2()


    def _str(self, n):
        """
        Transform integer to binary str.
        """
        return "{0:0{1}b}".format(n, self.total_bits)


    def _append_res(self, num, freeBits):
        """
        Add result to the result list.
        """
        self.res_list.append((num, freeBits))


    def _part1(self):
        """
        Handle A -> a_top.
        a_top: the bit on first_diff_index is 0, all bits after first_diff_index is 1.
        """

        a = self.A
        s = self._str(a)

        # special: A == 0
        if a == 0:
            freeBits = self.total_bits - self.first_diff_index - 1
            self._append_res(a, freeBits)
            return  # end

        # NOTE: can be handled in common loop, but this is OK.
        if s.endswith('1'):
            self._append_res(a, 0)
            a += 1
            s = self._str(a)

        # loop: look from low bit to high bit
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
        """
        Handle b_bottom -> B.
        b_bottom: the bit on first_diff_index is 1, all bits after first_diff_index is 0.
        """

        b = self.b_bottom
        s = self._str(b)

        index = self.first_diff_index + 1

        # loop: look from high bit to low bit
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
            else:  # sB[index] == '0'
                index += 1


    def print_result(self):
        for i in self.res_list:
            print(i)


    def print_result_x(self):
        """
        Print result like '000001111100xxxx'.
        """
        for (num, freeBits) in self.res_list:
            s = self._str(num)[0:(self.total_bits-freeBits)] + 'x' * freeBits
            print(s)


    def print_result_hex(self):
        """
        Print result like '0x780/0xffc0'.
        """
        for (num, freeBits) in self.res_list:
            maskStr = '1' * (self.total_bits - freeBits) + '0' * freeBits
            mask = int(maskStr, base=2)
            num = num & mask
            print("{}/{}".format(hex(num), hex(mask)))



class BitwiseIPv4Range(BitwiseRange):
    """
    Express a range of ipv4 addr as a set of subnet.
    The number of results is designed to be as few as possible.
    """

    def __init__(self, ipA, ipB):
        """
        Args:
            <str> ipA, ipB: such as "10.0.1.5", "10.0.2.100".
        """

        self.A = self._ipv4_to_int(ipA)
        self.B = self._ipv4_to_int(ipB)
        self.total_bits = 32
        self.sA = self._str(self.A)
        self.sB = self._str(self.B)

        self.res_list = []

        self._handle()


    def _ipv4_to_int(self, s):
        """
        "0.0.1.1" -> 257
        """

        l = s.split('.')
        num = (int(l[0]) << 24) + \
              (int(l[1]) << 16) + \
              (int(l[2]) << 8) + \
              (int(l[3]))

        return num


    def print_result_ipv4(self):
        """
        Print result like '10.0.2.96/30'.
        """

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
    BitwiseRange(0b0100, 0b1110, 4).print_result_x()
    BitwiseRange(1000, 1999).print_result_x()
    BitwiseRange(1000, 1999, 16).print_result_hex()
    BitwiseIPv4Range("10.0.1.0", "10.0.2.100").print_result_ipv4()


if __name__ == "__main__":
    test()

