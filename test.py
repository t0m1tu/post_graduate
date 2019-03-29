from multiprocessing import Pool

school_name = {'研招网': {'website': 'https://yz.chsi.com.cn/', 'info': '', 'into': '', 'select': ''}}

def job(x):
    return x*x
def multicore():
    pool = Pool()
    res = pool.map(job, range(10))
    print(res)


if __name__ == '__main__':
    multicore()