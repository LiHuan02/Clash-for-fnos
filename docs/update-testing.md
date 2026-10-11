# 更新源与独立测试

正式 FPK 的更新源由 `update-source.json` 固定为
`chenpingonline/Clash-for-fnos`。构建脚本将它编译到 Web 与 Root Helper，
两者使用相同更新仓库；fnOS 运行时环境变量不能覆盖此来源。
页面查询的新版信息与后端选择的安装包来自同一更新源。

## 测试包切回正式版

本次独立测试仓库为 `chenpingonline/Clash-for-fnos-update-test`，
测试包最高版本为 1.3.26。手动安装正式仓库的 1.3.27 FPK 后，
后续更新将查询正式仓库；无需卸载应用，也不要通过降级恢复来源。
测试与正式包使用相同应用身份，安装会升级现有应用。

在「设置 → 更新设置」查看当前版本和更新内容。已有更新时直接显示
“立即更新”，无需再检查一次。升级期间等待下载、校验、原位升级与重连；
新版运行后页面自动重新加载，完成提示随重连结束收起。
手动安装达到或超过旧失败目标的新版后，不再显示已过时的失败提示。
仍需确认订阅、配置、图标、Core 状态以及使用中的 TUN 流量是否正常。

## 工作目录与诊断

已验证的正式实现使用 `/var/tmp/clash-for-fnos-update/` 保存独立 worker、
锁、状态、临时 FPK 和安装/启动/健康检查日志；更新程序不会随着应用停止而退出。
应用中心解包的暂存目录由飞牛管理，应用配置仍使用原有持久数据目录。
工作区与应用数据、应用中心暂存区是不同用途的目录。

失败时保存界面提示、`status.json` 和分阶段日志，并核对应用中心实际版本
与运行状态。未知升级结果应先确认任务，避免重复提交；CLI 返回成功不代表
已经升级，也不能只靠下载摘要确认安装成功。

## 隔离测试与打包验证

- 在独立工作区将 `update-source.json` 改为测试仓库；不要改动正式发布配置。
- 共享源码必须已提交，以完整 SHA 固定在 `upstream.lock`。修改 manifest 版本，
  先完成匹配的 CHANGELOG，再运行 `./scripts/check.sh`。
- 串行构建 x86 / arm / all，运行 `scripts/audit-fpk.py`。审计同时核对
  `build-info.json` 与 Web / Helper 二进制的内嵌更新源。
- 可设置 `CLASH_AUDIT_EXECUTE=1`，在隔离 Docker 容器运行每个二进制的
  `--build-info`，确认真实版本、架构和来源；这不会启动应用。
  ARM 环境可用 `CLASH_AUDIT_QEMU_X86_64` 指定静态模拟器，
  `tonistiigi/binfmt` 模拟器同时设置 `CLASH_AUDIT_QEMU_BINFMT=1`。
  QEMU 或容器验证不能替代 fnOS 真机升级与网络验收。
- 测试源使用普通 Release：Root Helper 排除 draft / prerelease，并校验
  GitHub 资产提供的 SHA-256 digest。发布仅上传三个 FPK；摘要与审计报告留在本地。
- 测试仓库发布不授权正式仓库推送；正式合并和发布需用户明确要求。
