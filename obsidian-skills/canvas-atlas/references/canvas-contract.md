# 最小 Canvas 契约

依据 [JSON Canvas 1.0](https://jsoncanvas.org/spec/1.0/)。这是基础输出约束；布局和内容判断由 SKILL.md 管理。

根对象包含 `nodes` 和 `edges` 两个数组。输出 UTF-8 严格 JSON，不添加 Markdown fence。

每个节点都有字符串 `id`、`type` 和数值 `x`、`y`、`width`、`height`。ID 在本文件内唯一；采用 16 位小写十六进制是本 Skill 的约定，不是标准强制长度。数值必须有限，宽高为正。

| type | 必要内容 | 用途 |
|---|---|---|
| text | `text` | Markdown 解释、真实 wikilink、源码 URL |
| file | `file` | vault 根相对文件路径，可带 `subpath` 指向标题或块 |
| link | `url` | 网页引用；静态图通常优先用文本链接，避免加载远程预览 |
| group | 无额外必填 | `label` 命名视觉容器，子节点由坐标包含，不存在 children 数组 |

节点 `color` 可用 `"1"` 至 `"6"` 或十六进制色值。分组先写入 nodes 数组，内容卡片随后写入，避免容器遮挡内容。

边包含 `id`、`fromNode`、`toNode`。可指定 `fromSide`、`toSide` 为 `top/right/bottom/left`，以及 `fromEnd`、`toEnd` 为 `none/arrow`。业务关系写 `label`，默认只在目标端画箭头。

下面是一个可解析的单文件例子。它说明两个角色的关系；真实任务需要用来源支持卡片内容。

```json
{
  "nodes": [
    {"id":"1a00000000000001","type":"text","x":0,"y":0,"width":320,"height":180,"text":"## 分析者\n阅读来源，提炼职责与关系。","color":"5"},
    {"id":"1a00000000000002","type":"text","x":440,"y":0,"width":320,"height":180,"text":"## 架构地图\n呈现主要模块及关系。","color":"4"}
  ],
  "edges": [
    {"id":"2a00000000000001","fromNode":"1a00000000000001","fromSide":"right","toNode":"1a00000000000002","toSide":"left","toEnd":"arrow","label":"生成"}
  ]
}
```

用标准 JSON serializer 写入换行和引号。不要手工拼接 JSON。文本中的实际换行在序列化后应为 `\n`，不能变成显示给读者的反斜杠加字母 n。

引用注意事项：

- file 节点的 `file` 不带 `[[...]]`，不带机器绝对路径。
- 文件名的 `#标题` 放入 `subpath`，不混入 file 路径。
- text 节点可用 `[[地图/子图.canvas|进入子图]]`。中文及空格保持原样。
- 外部仓库文件用固定 commit 的 GitHub URL，或明确标注的源码相对路径。它们不是 vault file 节点。
- 不向原生 Canvas 新增私有 schema 或 provenance 字段。来源和日期写在导读卡片或伴随笔记中。
