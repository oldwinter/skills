# 构图样例

将任意 `.canvas` 文件复制到 Obsidian vault 后打开。每份样例都是独立单文件，没有附件或插件依赖。它们使用同一组假设内容、语义节点 ID 和关系，方便比较构图。内容不代表真实仓库。

| 文件 | 构图与配色 | 看哪里 |
|---|---|---|
| [editorial.canvas](editorial.canvas) | 杂志与纸本 | 大主卡、左侧依据、右侧边注 |
| [archipelago.canvas](archipelago.canvas) | 群岛与花园 | 分离的材料、判断与阅读区域 |
| [orbit.canvas](orbit.canvas) | 轨道与暮色 | 中心判断和外围输入输出 |
| [workbench.canvas](workbench.canvas) | 工作台与单色 | 错层材料、中央判断、右侧待办 |

用 `Shift+1` 查看全图，再放大主卡检查正文。样例中的颜色只强调当前判断，其他卡片保持中性。实际效果取决于 Obsidian 的应用主题；未设置字体、背景纹理或自定义 CSS。

尺寸和选型参考 [构图与配色](../references/visual-styles.md)。样例是阅读结构的参考，不是填空模板。真实任务需要自己的来源、问题和语义 ID。

在 Skill 目录中静态校验一份样例：

```bash
python3 scripts/check_canvas.py --vault examples editorial.canvas
```
