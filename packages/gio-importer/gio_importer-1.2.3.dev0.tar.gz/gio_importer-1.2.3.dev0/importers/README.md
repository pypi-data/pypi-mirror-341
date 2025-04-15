# GrowingIO Importer

GrowingIO Importer是GrowingIO CDP平台元数据创建和数据导入工具。

## 入门

有关GrowingIO Importer请访问[GrowingIO官方文档](https://docs.growingio.com/op/developer-manual/toolbox/ )获取帮助。

## 环境依赖

| | 4.4 |
|----|-----|
|Python| 3.8 |

## 安装

pip install gio-importer

## 环境参数
    import importers
    print(importers.__path__)

    根据路径信息，进入包目录，修改conf.cfg(导入工具配置信息)
    需要修改有关FTP，API信息(找负责项目运维提供FTP，API-uri相关信息)


## 元数据导入

目前支持如下：

* 创建事件
* 创建事件属性
* 创建用户属性
* 绑定事件与事件属性
* 导出元数据
* 导入元数据

### 使用说明

#### 创建事件

    from importers import meta_importer

    params = {
        'm': 'create_event',
        'key': '<事件名>',
        'name': '<事件显示名>',
        'desc': '<事件描述>'
    }

    meta_importer.do_meta(params)

|参数|参数说明|
|----|----|
|-m|必选参数，项目名。|
|--key|必选参数，事件名。仅允许大小写英文、数字、以及下划线，并且不能以数字开头，限长30字符|
|--name|可选参数，事件显示名。默认同事件名，限长30字符|
|--desc|可选参数，事件描述，默认为空。若描述中有空格则需要加双引号|

#### 创建事件属性

    from importers import meta_importer

    params = {
        'm': 'create_event_variables',
        'key': '<事件属性名>',
        'type': '<事件属性数据类型>',
        'name': '<事件属性显示名>',
        'desc': '<事件属性描述>'
    }

    meta_importer.do_meta(params)

|参数|参数说明|
|----|----|
|-m|必选参数，项目名。|
|--key|必选参数，事件名。仅允许大小写英文、数字、以及下划线，并且不能以数字开头，限长30字符|
|--type|必选参数，事件属性数据类型。可选值：string/int/double
|--name|可选参数，事件显示名。默认同事件名，限长30字符|
|--desc|可选参数，事件描述，默认为空。若描述中有空格则需要加双引号|

#### 创建用户属性

    from importers import meta_importer

    params = {
        'm': 'create_user_variables',
        'key': '<用户属性名>',
        'type': '<用户属性数据类型>',
        'name': '<用户属性显示名>',
        'desc': '<用户属性描述>'
    }

    meta_importer.do_meta(params)

|参数|参数说明|
|----|----|
|-m|必选参数，项目名。|
|--key|必选参数，标识符。仅允许大小写英文、数字、以及下划线，并且不能以数字开头，限长30字符|
|--type|必选参数，可选参数：string/int/date
|--name|可选参数，用户显示名。默认同标识符，限长30字符|
|--desc|可选参数，用户属性描述，默认为空。若描述中有空格则需要加双引号|

#### 绑定事件与事件属性

    python3 meta_importer.py -m bind_event_variables \
                             -k <事件名> \
                             -a <绑定事件属性名> \

|参数|参数说明|
|----|----|
|-m|必选参数，项目名。|
|--key|必选参数，事件名。若事件不存在则创建，否则更新事件|
|--attr|必选参数，绑定事件属性名。多个属性名使用英文逗号分隔(需加单引号或者在特殊符号前加上\)|

#### 导出元数据

    from importers import meta_importer

    params = {
        'm': 'bind_event_variables',
        'key': '<事件名>',
        'attr': '<绑定事件属性名集合>'
    }

    meta_importer.do_meta(params)

|参数|参数说明|
|----|----|
|-m|必选参数，项目名。|
|--file|必选参数，导出文件名|

#### 导入元数据

    from importers import meta_importer

    params = {
        'm': 'import_meta',
        'file': '<文件名>'
    }

    meta_importer.do_meta(params)

|参数|参数说明|
|----|----|
|-m|必选参数，项目名。|
|--file|必选参数，导入文件名|

## 数据导入

目前支持如下：

* 用户属性数据导入
* 用户行为数据导入

### 使用说明

#### 用户属性数据导入

    from importers import data_importer

    params = {
        'm': 'user_variables',
        'path': '<文件路径>',
        'datasource_id': '<数据源ID>',
        'format': '[CSV|TSV|Json]',
        'separator': ',',
        'skip_header': 'True',
        'attributes': 'userId,...'
    }

    data_importer.do_importer(params)


|参数|参数说明|
|---|----|
|-m|必填参数. 用户属性数据导入-user_variables|
|-path|必填参数. 需要导入的数据所在的路径|
|-datasource_id|必填参数. 数据源ID|
|-format|可选参数. 导入数据格式,目前支持JSON,CSV,TSV三种格式.默认值:JSON|
|-qualifier|可选参数. CSV,TSV格式文本限定符.默认值:"|
|-separator|可选参数. CSV,TSV格式文本分割符.默认值:,|
|-skip_header|可选参数. CSV,TSV格式设置则自动跳过首行,此参数不需要设置值.|
|-attributes|可选参数. CSV,TSV格式导入文件的各列按顺序映射到属性名，逗号分隔.userId必须指定(需加单引号或者在特殊符号前加上\)|

#### 用户行为数据导入

    from importers import data_importer

    params = {
        'm': 'events',
        'path': '<文件路径>',
        'datasource_id': '<数据源ID>',
        'format': '[CSV|TSV|Json]',
        'separator': ',',
        'skip_header': 'True',
        'attributes': 'userId,...,
        'event_start': '<数据起始日期 YYYY-MM-DD>',
        'event_end': '<数据结束日期 YYYY-MM-DD>'
    }

    data_importer.do_importer(params)


|参数|参数说明|
|-|----|
|-m|必填参数. 用户行为数据导入-events|
|-path|必填参数. 需要导入的数据所在的路径|
|-datasource_id|必填参数. 数据源ID|
|-event_start|必选参数. 数据起始时间,导入用户行为数据时指定.格式:YYYY-MM-DD|
|-event_end|必选参数. 数据结束时间,导入用户行为数据时指定.格式:YYYY-MM-DD|
|-format|可选参数. 导入数据格式,目前支持JSON,CSV,TSV三种格式.默认值:JSON|
|-qualifier|可选参数. CSV,TSV格式文本限定符.默认值:"|
|-separator|可选参数. CSV,TSV格式文本分割符.默认值:,|
|-skip_header|可选参数. CSV,TSV格式设置则自动跳过首行,此参数不需要设置值.|
|-attributes|可选参数. CSV,TSV格式导入文件的各列按顺序映射到属性名，逗号分隔.userId,event,timestamp必须指定(需加单引号或者在特殊符号前加上\)|

## 数据导入之MYSQL

目前支持如下：

* 用户属性数据导入
* 用户行为数据导入

### 使用说明

#### 用户属性数据导入

    from importers import format_importer

    params = {
        'm': 'user_variables',
        'format': 'mysql',
        'datasource_id': '<数据源ID>',
        'host': '<数据库连接地址>',
        'user': '<数据库连接用户>',
        'password': '<数据库连接密码>',
        'port': '<数据库连接端口号>',
        'sql': '<查询语句>'
    }

    format_importer.do_importer(params)

|参数|参数说明|
|----|----|
|-m|必填参数. 用户属性数据导入-user_variables|
|-datasource_id|必填参数. 数据源ID|
|-format|必选参数. 导入数据格式,目前支持mysql、hive数据源|
|-host|必选参数. mysql数据库ip|
|-user|必选参数. 客户端用户名|
|-password|必选参数.客户端密码|
|-port|必选选参数. 客户端端口号|
|-sql|必选参数. sql语句|

#### 用户行为数据导入

    from importers import format_importer

    params = {
        'm': 'events',
        'format': 'mysql',
        'datasource_id': '<数据源ID>',
        'host': '<数据库连接地址>',
        'user': '<数据库连接用户>',
        'password': '<数据库连接密码>',
        'port': '<数据库连接端口号>',
        'sql': '<查询语句>',
        'start_time': '<数据起始日期>',
        'end_time': '<数据结束日期>'
    }

    format_importer.do_importer(params) 

|参数|参数说明|
|----|----|
|-m|必填参数. 用户属性数据导入-user_variables|
|-datasource_id|必填参数. 数据源ID|
|-format|必选参数. 导入数据格式,目前支持mysql、hive数据源|
|-host|必选参数. mysql数据库ip|
|-user|必选参数. 客户端用户名|
|-password|必选参数.客户端密码|
|-port|必选选参数. 客户端端口号|
|-sql|必选参数. sql语句|
|-start_time|必选参数. 数据起始时间,导入用户行为数据时指定.格式:YYYY-MM-DD|
|-end_time|必选参数. 数据结束时间,导入用户行为数据时指定.格式:YYYY-MM-DD|

## 数据导入之HIVE

目前支持如下：

* 用户属性数据导入
* 用户行为数据导入

### 使用说明

#### 用户属性数据导入

    from importers import format_importer

    params = {
        'm': 'user_variables',
        'format': 'hive',
        'datasource_id': '<数据源ID>',
        'host': '<数据库连接地址>',
        'user': '<数据库连接用户>',
        'password': '<数据库连接密码>',
        'port': '<数据库连接端口号>',
        'sql': '<查询语句>'
    }

    format_importer.do_importer(params)

|参数|参数说明|
|----|----|
|-m|必填参数. 用户属性数据导入-user_variables|
|-datasource_id|必填参数. 数据源ID|
|-format|必选参数. 导入数据格式,目前支持mysql、hive数据源|
|-host|必选参数. mysql数据库ip|
|-user|必选参数. 客户端用户名|
|-password|必选参数.客户端密码|
|-port|必选选参数. 客户端端口号|
|-sql|必选参数. sql语句|

#### 用户行为数据导入

    from importers import format_importer

    params = {
        'm': 'events',
        'format': 'hive',
        'datasource_id': '<数据源ID>',
        'host': '<数据库连接地址>',
        'user': '<数据库连接用户>',
        'password': '<数据库连接密码>',
        'port': '<数据库连接端口号>',
        'sql': '<查询语句>',
        'start_time': '<数据起始日期>',
        'end_time': '<数据结束日期>'
    }

    format_importer.do_importer(params)

|参数|参数说明|
|----|----|
|-m|必填参数. 用户属性数据导入-user_variables|
|-datasource_id|必填参数. 数据源ID|
|-format|必选参数. 导入数据格式,目前支持mysql、hive数据源|
|-host|必选参数. mysql数据库ip|
|-user|必选参数. 客户端用户名|
|-password|必选参数.客户端密码|
|-port|必选选参数. 客户端端口号|
|-sql|必选参数. sql语句|
|-start_time|必选参数. 数据起始时间,导入用户行为数据时指定.格式:YYYY-MM-DD|
|-end_time|必选参数. 数据结束时间,导入用户行为数据时指定.格式:YYYY-MM-DD|

## 用户删除

目前支持如下：

* 触发用户删除任务
* 批量添加待删除用户

### 使用说明

#### 触发用户删除任务

    from importers import clear_user

    params = {
        'm': 'clear_users',
        'now': True
    }

    clear_user.do_user(params)

    python3 clear_user.py -m clear_users  -n True 

|参数|参数说明|
|---|----|
|-m|必填参数. 触发用户删除任务-clear_users |
|-now|必填参数. True - 立即执行离线任务,False - 天任务执行清理任务|

#### 批量添加待删除用户

    from importers import clear_user

    params = {
        'm': 'clear_users',
        'users': 'xxx,xxx,xxx'
    }

    clear_user.do_user(params)

|参数|参数说明|
|----|----|
|-m|必填参数. 批量添加待删除用户-clear_users_meta|
|-users|必填参数. 添加待删除用户,多个用户以逗号(,)分隔|