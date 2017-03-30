# Murtaza Meerza - HW 5

def pascalLine(n):
    ''' Function that returns nth line of Pascals Triangle '''
    if n == 0:
        return [1]
    else:
        current = [1]
        old = pascalLine(n-1)
        for ice in range(len(old)-1):
            current.append(old[ice] + old[ice+1]) 
        current += [1]
    return current


def levy(n):
    ''' Function that recursively generates Levy Curves '''
    if n == 0:
        return 'F'
    else:
        j = 'L'
        l = levy(n-1)
        return j + l + 'RR' + l + j
        

def base(a,b):
    ''' Function that returns a in base b '''
    if a == 0:
        return '0'
    else:
        ans = ''
        j = base(a//b,b)
        ans += str(j)
        ans += str(a%b)
    return ans
   
        
if __name__=='__main__':
    import doctest
    print(doctest.testfile('hw5TEST.py'))          
