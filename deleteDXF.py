from dxfMethod import *
if __name__ == '__main__':
    file_path = ''  #文件地址
    target = ''  #要保留的图层名称
    new_path = ''  # 新文件存储地址
    new_file = 'ttt00010.dxf'  # 要生成的文件名

    result = [] #将文件存进result
    layerType = 'AcDbEntity\n'
    textType = 'AcDbText\n'
    #读取文件
    f = open(file_path)
    line = f.readline()
    while line:
        result.append(line)
        line = f.readline()
    #删除多余图层
    i = 0
    while i < len(result):
        if result[i] == layerType and notZeroLayer(result,i) and validBound(result,i):
            if result[i+2] != target:
                #print('find',i)
                start = i-1
                end = findEnd(result,i)
                #print('end',end)
                #print('length',len(result))
                del result[start:end] #删除该实体
                i = 0
        i +=1
    #删除目标图层里的文字
    i = 0
    step = 6
    while i <len(result)-5:
        if result[i] == target:
            if result[i+ step] ==textType:
                #找到了里面的text模块
                start = i+5 # value: 100
                flag,end = findTextEnd(result,start)
                if flag:
                    del result[start:end]  # 删除该实体
                    i = 0
        i += 1

    #写文件
    new_f = open(new_path+new_file,'w')
    while len(result)>0:
        line = result.pop(0)
        new_f.write(line)
    new_f.close()