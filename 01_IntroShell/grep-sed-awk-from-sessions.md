# `grep` / `sed` / `awk` 与常用命令速记

| 命令 | 主要用途 |
|------|--------|
| `grep` | 从一堆文本里"找匹配行" |
| `sed` | 从长文本里"切片看几行"或做轻量替换 |
| `awk` | 把每一行按"字段"拆开，再筛选、统计、格式化 |
| `rg` | 更快的全文搜索，平时比 `grep` 用得更多 |
| `find` | 在目录树里找文件，常常是很多管道的起点 |
| `nl` | 给文本补行号，便于引用位置 |
| `git` | 看代码状态、差异和提交 |
| `jq` | 处理 JSON |
| `curl` | 抓网页和原始文本 |
| `test` | 做文件存在性判断 |
| `bash` | 临时跑一段小脚本 |

## `grep`：精确定位

`grep` 真正出场时，通常是“我已经知道要查哪个文件，只想把目标行筛出来”。

```bash
grep -n '^# *zh_CN.UTF-8 UTF-8\|^zh_CN.UTF-8 UTF-8' /etc/locale.gen
```

- `-n`：顺手带上行号，后面好改文件。
- `^...`：要求从行首匹配。
- `\|`：两个模式二选一。

## `sed`：非交互式看片段

用于快速查看长文本的某个片段，或者做一些轻量替换。

```bash
sed -n '起始行,结束行p' file
```

几个例子：

```bash
sed -n '1,200p' .vscode/settings.json
man tldr | sed -n '1,220p'
nl -ba ~/.zshrc | sed -n '65,95p'
curl -L .../CHANGELOG.md | sed -n '68,96p'
```

- `-n`：默认不打印。
- `'65,95p'`：只打印第 65 到 95 行。
- 配合 `nl -ba`：先补行号，再切片，引用代码时很方便。

## `awk`：按字段处理

`awk` 主要用于两类事：按分隔符取字段，和做小计算。只要开始出现“第几列”“最后一列”“计数”“格式化”，就该想到 `awk`。

例 1. 提取扩展名

```bash
find "$HOME" -type f -printf '%f\n' | awk -F. 'NF > 1 && $1 != "" { print $NF }' | sort | uniq -c | sort -nr | head -5
```

- `-F.`：用 `.` 分列。
- `NF`：当前行字段数。
- `$NF`：最后一列。
- `NF > 1 && $1 != ""`：跳过没扩展名和隐藏文件的干扰情况。

例 2. 格式化数字

```bash
awk -v ns="$1" 'BEGIN { printf "%.3f ms", ns / 1000000 }'
```

- `-v ns="$1"`：把 shell 变量传进 `awk`。
- `BEGIN { ... }`：不读输入，直接执行一段格式化逻辑。

## 其他常用命令

### `rg`

搜文本和列文件时，`rg` 往往是第一选择。出场频率比 `grep` 更高，主要因为速度快，而且默认结果更适合直接读。

```bash
rg -n "pattern" .
rg --files
```

### `find`

经常用来把“候选文件集合”喂给后面的管道。

```bash
find "$HOME" -type f
find "$HOME" -type f -printf '%f\n'
```

### `nl`

想引用“第几行”时，用 `nl -ba` 很顺手。和 `sed` 搭配非常高频。

```bash
nl -ba ~/.zshrc | sed -n '65,95p'
```

### `git`

进仓库先看 `git status`，改完再看 `git diff`。

```bash
git status --short
git diff
```

### `jq`

处理 JSON 日志和接口返回时很省力。

```bash
jq -r '.payload.command[2]' file.jsonl
```

### `curl`

主要用来抓文档、网页源码、原始文本。

```bash
curl -L https://example.com/file.txt | sed -n '1,40p'
```

### `test`

轻量判断。

```bash
test -f .vscode/settings.json
test -f file && sed -n '1,40p' file || echo missing
```

### heredoc

这不是单独的命令，而是 shell 语法。作用是把后面的一大段文本直接送给前面的命令作为标准输入。

```bash
# 例 1
bash <<'EOF'
echo hello
echo world
EOF
# 例 2
python <<'PY'
print("hello")
print("world")
PY
```

- `EOF`、`PY` 只是结束标记，名字可以自己取，前后一致即可。
- `<<EOF` （不带单引号）会先做 shell 展开，所以 `$HOME`、`$(cmd)` 会先被解释。
- `<<'EOF'` 不做展开，内容按字面值传进去；这也是我更常用的写法。
- 结束标记必须单独占一行。
