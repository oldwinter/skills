# 审批附件上传与验收

适用于报销表单的 `attachmentV2`，补充通用审批技能要求调用方提供 file code 的缺口。先阅读当前 `lark-cli api --help` 与 `lark-shared` 的身份、输出契约；以下为已验证的接口形态，响应结构变化时以实际响应及当前文档为准。

## 已验证路径

2026-09-22、lark-cli 1.0.91 的实测结果：

- `/open-apis/approval/v4/files/upload` 使用 `--as user` 返回 `99991668: user access token not support`。
- 同一路径使用已有可用的 `--as bot` 上传成功；审批实例仍可使用 `--as user` 创建，且附件能回读下载。
- 响应 file code 位于 `data.urls_detail[].code`，不是 `data.code`。过早用 jq 过滤到错误路径会丢失成功回执，诱发重复上传。
- 经该 CLI 原样调用 `/approval/openapi/v2/file/upload` 曾返回 404。旧版本文档中的路径和主机不能直接视为当前 CLI 的可用调用。

这些是特定环境的实测证据，不代表所有 CLI 构建都有应用身份。先复用当前配置；缺少应用身份、权限或构建限制时，读取权限错误并选择已授权的客户端上传途径，或请求必要配置。为上传而新建应用、扩大权限不属于默认步骤。

## 上传一份，确认结构，再继续

本地文件先按“费用名称_金额_凭证类型”命名。以附件控件为例：

```bash
lark-cli api POST /open-apis/approval/v4/files/upload \
  --as bot \
  --data '{"name":"软件订阅_100元_发票.pdf","type":"attachment"}' \
  --file 'content=./private-task/软件订阅_100元_发票.pdf' \
  > ./private-task/upload-receipt.json
```

`./private-task` 表示已创建的本机私有任务目录，优先替换为项目约定的 ignored runtime 路径。CLI 文件参数使用相对 cwd 的路径。每次上传一份；为每份文件保存原始 JSON 回执，再提取 code。脚本调用使用 argv 数组，动态名称通过 JSON 序列化传参。

成功响应形态：

```json
{
  "ok": true,
  "identity": "bot",
  "data": {
    "urls_detail": [
      {"code": "FILE_CODE", "message": "", "origin_url": ""}
    ]
  }
}
```

校验进程成功、`ok == true`、逐项消息无错误，以及非空 code 的数量符合预期；结构不匹配时保留回执并调查。后续 `attachmentV2.value` 填 code 字符串数组，不填云文档素材 token、本地路径或下载 URL。

## 文件名是独立验收项

实测请求传入了描述性名称，但实例详情的附件 URL 片段呈现 `obj.pdf` / `obj.jpg`；当次只验证了附件字节一致，未验证客户端名称。不能据此声称名称保留，也不能只凭 URL 断言界面一定显示“未知文件”。

若命名为验收要求，在批量上传和提交前先检查当前上传接口的文件名字段、multipart 行为及可用元数据。需要客户端才能确认时做客户端检查。名称不满足时优先采用保留名称的已验证上传方式；已提交实例则使用受支持的编辑流程，无法编辑时报告限制。撤回重建会改变审批状态，需用户授权，不能静默重建。

## 内容与恢复

维护逐文件台账：本地路径、展示名称、费用归属、大小、SHA-256、file code、回执路径。提交后保存实例附件映射，下载远端文件并核对本地摘要；仅向用户报告数量、匹配结果和不匹配名称。

凭证、回执和带签名 URL 均留在本机私有状态；可复用技能只保留接口经验和匿名示例。上传成功只代表取得附件标识，完成报销仍须创建实例并回读核验。
