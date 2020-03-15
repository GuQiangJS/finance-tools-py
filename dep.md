#### 依赖

使用 finance-tools-py 依赖于以下包：

##### 运行时依赖

* talib
    window环境下下载并安装 https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
* pandas
* numpy

##### 测试中依赖

* QUANTAXIS
* pytest

##### 开发时使用以下包：

* [yapf](https://github.com/google/yapf/)。

    pycharm下配置：
        Settings->Tools->External Tools->Add
        
        Name: yapf
        
        Program: yapf.exe 安装目录。一般在当前python环境的Scripts下。
        
        Arguments: `-i $FilePathRelativeToProjectRoot$`
        
        Working directory: `$ProjectFileDir$`
    可以设置快捷键替换与版本的格式化代码。
    
        Settings->Keymap 搜索yapf设置快捷键为 `Ctrl+Alt+L`

##### 编译帮助文档时使用：

* sphinx
* sphinxcontrib-napoleon

