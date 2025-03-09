import math
def quadratic(a,b,c,):
    q=b**2-4*a*c
    if q>0:
        l=math.sqrt(q)
        x=(-b+l)/(2*a)
        y=(-b-l)/(2*a)
        return x,y
    elif q==0:
        x=-b/2*a
        return x,x
    else:
        return None
print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))

if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('测试失败')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('测试失败')
else:
    print('测试成功')