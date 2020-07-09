### 山西文物勘探保护系统

### 数据模型

#### 状态枚举
```
status {
    0: 对接,
    1: 调查,
    2: 勘察,
    3: 发掘,
    4: 竣工
}

relic_type {
    1: {
        "dswwzy":"地上文物资源",
        "dxwwzy":"地下文物资源"
    },
    2: {
        "yjxq2":"遗迹详情",
        "ywxq":"遗物详情"
    },
    3: {
        "yjxq3":"遗迹详情",
        "gzxq":"工作详细"
    }
}

tagname: {
    areamap: 开发区,
    project_type: 项目性质,
    phototype: 底图类型,
    project_level: 项目级别,
    dswwzy:"地上文物资源",
    dxwwzy:"地下文物资源"
    yjxq2:"遗迹详情",
    ywxq:"遗物详情"
    yjxq3:"遗迹详情",
    gzxq:"工作详细"
}

```


#### 城市编码   
```
areacode {
    id: xxx,
    parent_id: 父节点ID 0
    name: 名称
}

post /areacodes
get /areacodes/{parent_id}
delete /areacodes/{id}
```

#### 标签系统
```
tag {
    id: xxx,
    tag:"tagname", # 哪种类型的的分类
    name: xxx,
    hits: count
}

post /tags
get /tags/{tagname}
delete /tags/{tagname}/{id}

```

### 项目
```
project {
    name: 名称,
    areamap: 开发区 tag,
    status: 状态,
    project_type: 项目性质 tag,
    city: 城市,
    cityarea: 市区,
    localmap:[{lat,lag}], # 区域经纬度列表,
    level: 级别(国保、省保、市县保、未定级) tag
    organization: 批准机关(eg: 国务院、山西省委、省政府)
    addon: unixtime 年份单选,
    numbercode: 时间及文号,
    planarea:规划面积,
    industry:主导产业,
    mark:备注
}

post /projects
put /projects/{id}
get /projects
get /projects/{id}
delete /projects/{id}
```

### 项目对接
```
project_btb  {
    project_id: 项目id,
    addon: unixtime 对接时间,
    body: 对接内容
}
```

#### 项目对接文件
```
project_btb_file  {
    id: xxx,
    project_id: 项目id,
    project_btb_id: xxx,
    name:xxx,
    fid:xxx,
    addon:xxx
}
```


### 项目进度
```
project_process  {
    project_id: 项目id,
    status: 项目状态(调查, 勘探, 发掘),
    start: unixtime 开始,
    end:unixtime 结束,
    peoples: ['xx', 'xx'],
    area: 面积,
    areaname: 调查区域,
    body: 对接内容
}
```



#### 项目进度-评估建议
```
project_sprocess_suggest {
    id:1,
    project_id: 项目id,
    status: 项目状态(对接, 调查, 勘探, 发掘, 竣工),
    stype: xxx,
    body:xxxx,
    addon:xxx,
}

```

#### 项目文件报告
```
project_report {
    project_id: 项目id,
    status: 项目状态(对接, 调查, 勘探, 发掘, 竣工),
    ftype: tag,
    name:xxx,
    addon:xxx,
    fid:xxx
}
```



#### 项目进度-调查区域图形
```
project_areaphoto{
    id:1,
    project_id: 项目id,
    status: 项目状态(对接, 调查, 勘探, 发掘, 竣工),
    phototype: tag,
    fid: 底图,
    layer: 图层信息
}

```


#### 项目进度-项目调查文物
```
project_relic_wwxq  {
    project_id: 项目id,
    status: 项目状态(对接, 调查, 勘探, 发掘, 竣工),
    tag:文物类型（国保、省保、市县保、未定级）,遗迹性质(灰坑、窑址、房址等),
    relic_type: 调查(地上文物资源,地下文物资源)
    name: 名称,
    times: 时代,
    projectarea: 保护区域,
    buildarea: 建设控制地带,
    photos:[{
        min_fid
        fid,
    }]
}
```

#### 项目进度-项目遗迹遗物
```
project_relic_yjyw  {
    project_id: 项目id,
    status: 项目状态(对接, 调查, 勘探, 发掘, 竣工),
    tag:文物类型（国保、省保、市县保、未定级）,遗迹性质(灰坑、窑址、房址等),
    relic_type: 调查(地上文物资源,地下文物资源)
    name: 名称,
    times: 时代,
    projectarea: 保护区域,
    buildarea: 建设控制地带,
    photos:[{
        min_fid
        fid,
    }]
}
```