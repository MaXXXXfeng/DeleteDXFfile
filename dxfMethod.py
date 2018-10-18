########################
#处理删除多余图层的方法#
########################
def notZeroLayer(result,index,layerType= 'AcDbEntity\n'):
    '''
    判断当前图层是否是第0层
    :param result: 读取后保存的文件
    :param index: 开始搜索的位置
    :return: 当前的图层是否是0层
    '''
    if result[index+2]=='0\n' or result[index+4]=='0\n':
        #print('ZERO!')
        return False
    return True
def validBound(result,index,bound=40,endBound=200,layerType= 'AcDbEntity\n'):
    '''
    防止两个搜索到的实体间夹杂太多其他类
    :param result:读取后保存的文件
    :param index:开始搜索的位置
    :param bound: 表示一个实体最多的行数
    :return:True:合理的范围 False:范围太长，不合理
    '''
    count = 0
    for i in range(index+1,len(result)):
        count += 1
        if result[i] == layerType:
            break
        if count >100:
            break
    if count > bound:
        if len(result)-index > endBound:
            return False
    return True


def findEnd(result,index,layerType= 'AcDbEntity\n'):
    '''
    找到下一个实体，作为删除的终止点
    :param result: 读取后保存的文件
    :param candidate_list: 所有实体名字保存
    :param index: 开始搜索的位置
    :return: 删除的结束点
    '''
    n = len(result)
    for i in range(index+1,n):
        if result[i] == layerType and notZeroLayer(result,i):
            #找到了下一个实体的开头
            end = i-1
            return end
####################
#处理删除文本的方法#
####################
def findTextEnd(result,index,layerType= 'AcDbEntity\n',textType = 'AcDbText\n'):
    '''
    找到要删除的文本的终点
    :param result:  读取后保存的文件
    :param index: 搜索起始点
    :return: falg,end ,是否可删，终点坐标
    '''
    endingType = '100\n' #搜索到100证明到了下一个
    #count = 0
    #bound = 25 #如果25行内没搜到100，则不删除
    #end = 0
    for i in range(index+2,len(result)):
        #count += 1
        if result[i] == endingType:
            end = i
            return True, end
    return False,0



