# -*- coding: utf-8 -*-

from mylogger import mylogg
import datetime
import sys, os
import copy
import numpy
import glob

gidName = {}
gsegTime = {}
ghcTime = {}
topK = 20

mylog = None


def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]


def fidName(fn):
    with open(fn, 'r', encoding='utf-8') as reader:
        for lines in reader:
            line = lines.strip().split(',')
            ids = line[0]
            names = line[1]
            gidName[ids] = names
            
            
def fsegTime(fn):
    with open(fn, 'r', encoding='utf-8') as reader:
        for lines in reader:
            line = lines.strip().split(',')
            start = line[0]
            end = line[1]
            utTime = int(line[4]) 
            uwTime = int(line[5])
            dtTime = int(line[6])
            dwTime = int(line[7])
            gsegTime[start + '|' + end] = (utTime, uwTime)
            gsegTime[end + '|' + start] = (dtTime, dwTime)
            
            
def fhcTime(fn):
    with open(fn, 'r', encoding='utf-8') as reader:
        for lines in reader:
            line = lines.strip().split(',')
            fstart = line[0]
            start = line[1]
            end = line[2]
            bend = line[3]
            uwait = int(line[4])
            uwalk = int(line[5])
            dwait = int(line[6])
            dwalk = int(line[7])
            ghcTime[fstart + '|' + start + '|' + end + '|' + bend] = (uwait, uwalk)
            ghcTime[bend + '|' + end + '|' + start + '|' + fstart] = (dwait, dwalk)
            

#过滤路径中的如2-3-4的线路
def hcTime(paths):
    otp = None
    atp = []
    aatp = []
    tpline = copy.deepcopy(paths)
    for itp, tp in enumerate(tpline):
      lines = int(int(hex(int(tp))[2:])/100)
      if otp != lines and otp != None:
          atp.append(itp)
      else:
          if len(atp) > 1:
              aatp.append(atp)
          atp = []
      otp = lines
    if len(atp) > 0:
        aatp.append(atp)
    for ia, ival in enumerate(aatp):
        aatp[ia] = ival[:-1]
    aatp = sum(aatp, [])
    atp = []
    for itp, tp in enumerate(tpline):
        if itp not in aatp:
            atp.append(tp)
    return atp
        
                  

def pathtime(paths, hc1, hc2, hc3):
    global mylog
    path = paths.split('|')
    ttime = 0
    incnt = 0
    for ind in range(len(path)-1):
        oind = path[ind]
        dind = path[ind+1]
        tkey = oind + '|' + dind
        if tkey in gsegTime.keys():
            ttime += gsegTime[tkey][0]
            ttime += gsegTime[tkey][1]
        else:
            mylog.error('%s not exist in segMap', tkey)
            
    ttpaths = hcTime(path)
    for ind in range(len(ttpaths)-1):
        oind = ttpaths[ind]
        dind = ttpaths[ind+1]
        if (ind - 1) >= 0 and (ind + 2) <= (len(ttpaths)-1):
            foind = ttpaths[ind - 1]
            bdind = ttpaths[ind + 2]
            tkey = foind + '|' + oind + '|' + dind + '|' + bdind
            if tkey in ghcTime.keys():
                hctime = ghcTime[tkey][0] + ghcTime[tkey][1]
                if incnt == 0:
                    ttime += hctime*hc1
                elif incnt == 1:
                    ttime += hctime*hc2
                else:
                    ttime += hctime*hc3
                incnt += 1
            #else:
            #    mylog.error('%s not exist in hcMap', tkey)
    return (ttime, '|'.join(ttpaths), incnt)
                
def pathname(paths):
    names = []
    for path in paths.split('|'):
         if path in gidName.keys():
             names.append(gidName[path])
         else:
            names.append('')
    return '|'.join(names)
             

def topkTime(fns, outffs, hc1, hc2, hc3):
    global mylog
    rpath = str(hc1) + '_' +  str(hc2) +  '_' + str(hc3)
    trpath = '/data/silx/pathtime/outs/' + rpath + '.tmp'
    drpath = '/data/silx/pathtime/outs/' + rpath + '.txt'
    #trpath = '..\\outs\\' + rpath + '.tmp'
    #drpath = '..\\outs\\' + rpath + '.txt'
    if drpath in outffs:
        mylog.info('file=%s exist, return', drpath)
        return
    wts = open(trpath, 'w')
    mylog.info('file=%s, start...', rpath)
    for fn in fns:
        mylog.info('file=%s, process start...', fn)
        maxfl = 9999999
        #nwts = open('../out/name_path_time_'  + str('%02d'%flag) + '.txt', 'w')
        fres = [(0,0,0,0,maxfl)] * topK
        ood = None
        t1 = datetime.datetime.now()
        cntod = 0
        with open(fn, 'r', encoding='utf-8') as reader:
            for lines in reader:
                line = lines.strip().split(',')
                od = line[0]
                idpath = line[1]
                tpaths = line[3]
                times, paths, hcnts = pathtime(tpaths, hc1, hc2, hc3)
                fres = sorted(fres, key=lambda k:k[4])
                if od != ood and ood != None:
                    fres = sorted(fres, key=lambda k:k[4])
                    for vals in fres:
                        if vals[4] < maxfl:
                            wts.write(vals[0] + ',' + vals[1] + ',' + str(vals[2]) + ',' + str(vals[3]) + ',' + str(vals[4]) + '\n')
                            wts.flush()
                            #nwts.write(vals[0] + ',' + pathname(vals[3]) + '\n')
                            #nwts.flush()
                    fres = [(0,0,0,0,maxfl)] * topK
                    t4 = datetime.datetime.now()
                    tods = (t4-t1).total_seconds()
                    t1 = t4
                    cntod += 1
                    mylog.info('%s finished, cnt=%d, times=%.2fs', ood, cntod, tods)
                if times < fres[topK-1][4]:
                    if paths not in set([x[3] for x in fres]) and hcnts <= 3:
                        fres[topK-1] = (od, idpath, hcnts, paths, times)
                ood = od
            fres = sorted(fres, key=lambda k:k[4])
            for vals in fres:
                if vals[4] < maxfl:
                    wts.write(vals[0] + ',' + vals[1] + ',' + str(vals[2]) + ',' + str(vals[3]) + ',' + str(vals[4]) + '\n')
                    wts.flush()
                    #nwts.write(vals[0] + ',' + pathname(vals[3]) + '\n')
                    #nwts.flush()
            #nwts.close()
            cntod += 1
            t4 = datetime.datetime.now()
            tods = (t4-t1).total_seconds()
            mylog.info('%s finished, cnt=%d, times=%.2fs', ood, cntod, tods)       
            mylog.info('file=%s, process finished.', fn) 
    wts.close()
    try:
        os.rename(trpath, drpath)
    except:
        mylog.error('%s rename to %s failed, please check.', trpath, drpath)
    mylog.info('file=%s, finished...', rpath)

                        
            
def init(flag):
    global mylog
    mylog = mylogg('../logs/' + os.path.basename(__file__).split('.')[0] + '_' + str('%02d'%flag) + '.log')
    mylog.info('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    mylog.info('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    mylog.info("---------------process starting--------------------")
    fidName('../conf/road_id_name.txt')
    fsegTime('../conf/road_time_seg.txt')
    fhcTime('../conf/road_time_hc.txt')
    mylog.info("-----------------init finished---------------------")
 
    
 
def getsource():
    source = numpy.linspace(1, 5, 9)
    sdata = []
    for k1 in source:
        for k2 in source:
            for k3 in source:
                if k2>= k1 and k3>= k2:
                    sdata.append((k1, k2, k3))
    return sdata

# linux 返回决定路径
def findfiles(bp):
    files = []
    for name in sorted(glob.glob(bp)):
        files.append(name)
    return files
    

def test():
    global flag
    flag = 0
    init(0)
    infn = """..\\simple_path_*.txt"""
    outfn = '..\\outs\\*.txt'
    inffs = findfiles(infn)
    outffs = findfiles(outfn)
    topkTime(inffs, outffs, 2.0, 3.0, 4.0)
 




def main():
    global flag
    if len(sys.argv) != 2:
        print ('usage: python %s flag' % (sys.argv[0]))
        sys.exit(-1)
    flag = int(sys.argv[1])
    init(flag)
    sdata = getsource()
    lsdata = list_split(sdata, 5)
    if flag >= len(lsdata):
        mylog.error('process %s end and exit.',  flag)
        return
    infn = '/data/silx/getpath/simple_path_*.txt'
    outfn = '/data/silx/pathtime/outs/*.txt'
    inffs = findfiles(infn)
    outffs = findfiles(outfn)
    for ld in lsdata[flag]:
        topkTime(inffs, outffs, round(ld[0], 2), round(ld[1], 2), round(ld[2], 2))
    

if __name__ == '__main__':
    main()

