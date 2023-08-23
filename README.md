## DONATE

Paypal / Alipay: `wangsitan@aliyun.com`

# bitwise-range

OpenFlow and Open vSwitch support bitwise match on individual fields, but don't support range match directly.

`man ovs-fields`:  
> Range matches can be expressed as a collection of bitwise matches.

This piece of code works for this. It transforms a range of number (nonnegative integer) into a set of bitwise stuff. The number of results is designed to be as few as possible.

There is also an encapsulation for IPv4 address range.



## corresponding content in ovs-fields manual

```
    Some  types of matches on individual fields cannot be expressed directly with OpenFlow and
    Open vSwitch. These can be expressed indirectly.

        Range match, e.g. ``1000 ≤ tcp_dst ≤ 1999’’
            The value of the field must lie within a numerical range, for  example,  TCP
            destination ports between 1000 and 1999.

            Range matches can be expressed as a collection of bitwise matches. For exam‐
            ple, suppose that the goal is to match TCP source ports 1000 to 1999, inclu‐
            sive. The binary representations of 1000 and 1999 are:

            01111101000
            11111001111

            The following series of bitwise matches will match 1000 and 1999 and all the
            values in between:

            01111101xxx
            0111111xxxx
            10xxxxxxxxx
            110xxxxxxxx
            1110xxxxxxx
            11110xxxxxx
            1111100xxxx

            which can be written as the following matches:

            tcp,tp_src=0x03e8/0xfff8
            tcp,tp_src=0x03f0/0xfff0
            tcp,tp_src=0x0400/0xfe00
            tcp,tp_src=0x0600/0xff00
            tcp,tp_src=0x0700/0xff80
            tcp,tp_src=0x0780/0xffc0
            tcp,tp_src=0x07c0/0xfff0
```



## example

```
>>> from bitwise_range import BitwiseRange, BitwiseIPv4Range

>>> BitwiseRange(0b0100, 0b1110, 4).print_result_x()
01xx
10xx
110x
1110

>>> BitwiseRange(1000, 1999).print_result_x()
01111101xxx
0111111xxxx
10xxxxxxxxx
110xxxxxxxx
1110xxxxxxx
11110xxxxxx
1111100xxxx

>>> BitwiseRange(1000, 1999, 16).print_result_hex()
0x3e8/0xfff8
0x3f0/0xfff0
0x400/0xfe00
0x600/0xff00
0x700/0xff80
0x780/0xffc0
0x7c0/0xfff0

>>> BitwiseIPv4Range("10.0.1.0", "10.0.2.100").print_result_ipv4()
10.0.1.0/24
10.0.2.0/26
10.0.2.64/27
10.0.2.96/30
10.0.2.100/32
```


