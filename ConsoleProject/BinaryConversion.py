print("CONVERSION OF DECIMAL NUMBER TO BINARY NUMBER")

def decimal_to_binary(dec,fract_precision=6):
    integer=int(dec)
    fraction=dec-integer

    def int_converter(num):
        if num==0:
            return 0
        return (num & 1) + 10*int_converter(num>>1)

    def fract_converter(fract,precision=6):
        if precision==0 or fract==0:
            return 0
        fract=fract*2
        return 0.1*int(fract) + 0.1*fract_converter(fract-int(fract),precision-1)

    return int_converter(integer)+ round(fract_converter(fraction),fract_precision)


if __name__ == "__main__":
    print(decimal_to_binary(95.0625))
