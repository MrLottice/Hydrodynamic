SHP转XYZ 1.5 By 火鸟1412（YF1412） 2018.5.29

在原基础上，加入界面化，方便操作，双击Main.exe,即可选择输入输出文件，无需复制程序。原命令行方式依旧可行。




SHP转XYZ 1.0 By 火鸟1412（YF1412） 2018.5.25

本程序用于将岸线Shp文件转化为MIKE可用XYZ文件。具体注意事项如下：

1 Shp为多段线Polyline文件，请勿夹杂其他点、面，以免转换报错；

2 xyz默认岸线Z值均为10，4列，x y connection z;

3 将shp2xyz拷贝至目标shp文件夹内，空白处Shift+右键，在此处打开CMD或则powershell

cmd命令如下(win7)：

shp2xyz.exe 目标.shp 输出.xyz

Powershell命令如下(win10)：

./shp2xyz.exe 目标.shp 输出.xyz

请勿遗漏后缀名

4 本程序在Win7 64位与Win10 64位上测试无误。32位系统上可能报错，请谅解。

5 本程序转化后xyz在mesh generator中加载可能会出现部分连线异常，请使用者注意修改。

6 如有其他问题或报错反馈，请联系fyang@nhri.cn或517952143@qq.com.