#Description(add requirements):
##version-0.1
- 完成svc_base.html模板,查询service/resource/svcInstance
##version-0.2
- 新增/修改/删除(修改状态)--service/resource/svcInstance
- 与后端自动化部署软件集成设计思路：
  -->设计service type[service plugins]/可以设置固定plugins目录，程序内自动解析此目录下的已实现特定API的插件
  -->然后决定后端调用不同的 implementor {ansible/puppet/任何具有api的程序/等等}
  -->接上条：关于中间件服务后端可以连接自动化部署工具/应用服务的话，可以对接PaaS平台/管理应用生命周期[含权限]
