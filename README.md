# DeleteDXFfile-Python
前言
近期项目有个任务是要处理工程制图，标记图中一些零件或者部件的具体位置。考虑到制图非常精细，要标注里面很精准的东西有些复杂。于是更换了思路，先将无关图层删除掉，然后保留目标图层，这样标注或者识别的时候就容易很多了。
dxf文件简介
关于dxf的具体介绍这里我就不详细讲了，放一篇链接，里面讲的非常详细。
[https://blog.csdn.net/sinat_32349327/article/details/73480994](https://blog.csdn.net/sinat_32349327/article/details/73480994)
在autoCAD里面可以将图层关闭，但是另存为的时候一直出现错误，无法保存存有指定图层的dxf文件，所以只能写个Python文件来手动删除文件。
打开dxf文件，发现其格式其实很有规律。不算开头和结尾部分，大多数都是中间的实体图层。比如：
100
AcDbEntity
  8
图层名字（例如门）
  6
CONTINUOUS
 62
    15
100
AcDbText
 10
6568.75
 20
7650.0
 30
0.0
 40
125.0
  1
这里面100可以理解为一个开始，AcDbEntity表示是一个实体。下面的图层名字表示具体是什么图层。再往下就是一些具体的坐标等属性，这里不深究了。
关于删除图层，有两点需要注意。一是找到要保留的图层。二是不能删除第0层。因为第0层可以理解为一个基准，没了这一层图像是无法显示出来的。
过程
首先肯定是要读取文件，一行一行把文件存放在list里。后续删除都在这个list里面。
```
#读取文件
    f = open(file_path)
    line = f.readline()
    while line:
        result.append(line)
        line = f.readline()
```
下一步就是删除多余的图层，假设我们要保留的图层名字是target。
这里的思路是当有一行判断到是实体之后，接下来判断是不是第0层。同时再保证图层名字不是我们要保留的，就可以删除了。删除的长度要继续往后面搜索，搜索到下一个实体开始的时候作为结点。这里在具体实现的方法里设置了一个计数器，当搜索好多行依然没发现下一个实体时可以停止搜索，因为很可能是到了最后一个。
```
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
```
到了这一步之后基本上需要的图层就会完整的保留下来。但是下一个问题就是保留的图层里面含有很多文字信息，这些信息会干扰下一步程序的运行。这里将对保留的图层做进一步的优化，把里面的文字信息去掉，只留下需要的图形形状就可以。 分析前面的dxf文件格式，我们发现文本信息存放在AcDbText这个里面，我们可以先找到AcDbEntity，然后在它下面去搜AcDbText就可以找到是我们需要删除的文本信息。
```
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
```
最后一步就是把处理过的文件写进新的dxf文件就完成了。
```
new_f = open(new_path+new_file,'w')
    while len(result)>0:
        line = result.pop(0)
        new_f.write(line)
    new_f.close()
```
总结
因为是第一次接触dxf文件，花了比较多的时间在其结构上的研究。总的来说注意一下特殊情况处理，做里面的删除或其他操作还是比较简单的。文章也就没再特别详细的去分析删除中的细节。基本上打开dxf文件看一下就能分析出其结构和规律。


