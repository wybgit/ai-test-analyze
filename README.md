# AI-Test-Analyze: AI 驱动的日志分析工具

`ai-test-analyze` 是一个专业的命令行工具，它利用大语言模型（LLM）的强大能力，通过多线程并发，快速分析指定的测试日志文件，并生成一个结构化、可配置、可选格式的动态分析报告。

## 核心功能

- **开箱即用**: 项目内置 `example` 目录，包含丰富的示例日志，让您无需任何准备即可体验工具的完整功能。
- **子命令结构**:
    - `run`: 执行核心的分析任务。
    - `config`: 快速显示所有配置和模板文件的路径。
- **强大的过滤功能**:
    - 通过 `config.json` 文件，同时支持**白名单**和**黑名单**规则。
- **高级 Prompt 模板**:
    - 所有模板都存放在 `~/.config/ai-test-analyze/templates/` 目录下，方便集中管理。
    - 主 `prompt.template` 可以动态地从 `success_pattern.template` 和 `failed_pattern.template` 文件中加载成功/失败的关键模式。
- **多线程并发分析**: 通过 `--threads` 参数指定线程数（默认为8），大幅缩短分析时间。
- **动态目录报告**: 报告能自动适应任意深度的目录结构，动态生成 `Sub Dir 1`, `Sub Dir 2`... 等列。
- **自动初始化**: 首次运行时，所有必需的配置文件和模板都会自动在您的用户主目录中创建。

## 安装

在项目根目录下，运行以下命令进行安装或更新。

```bash
pip install .
```

## 快速开始

本项目自带一个 `example` 目录，其中包含了不同类型的日志文件。我们将使用这个目录来演示如何使用本工具。

### 1. 查看配置

安装后，首先运行 `config` 命令查看所有配置文件的位置。程序在首次运行时会自动创建这些文件。

```bash
ai-test-analyze config
```
输出:
```
配置文件目录: /home/user/.config/ai-test-analyze
主配置文件: /home/user/.config/ai-test-analyze/config.json
模板文件目录: /home/user/.config/ai-test-analyze/templates
```

### 2. 填入 API Token

根据上一步显示的路径，打开 `config.json` 文件，**��填入您的 `api_token`**。对于本示例，其他配置（如黑白名单）可暂时保持默认。

### 3. 执行分析

现在，让我们用 `run` 命令来分析 `example` 目录，并生成一个 Excel 报告。

```bash
ai-test-analyze run ./example --format xlsx --output example_report
```

程序会：
1.  显示一个进度条，扫描 `example` 目录下的所有文件。
2.  显示第二个进度条，使用8个线程并发分析找到的日志。
3.  在当前目录下生成一个名为 `example_report.xlsx` 的精美报告。

您可以打开这个 Excel 文件，查看工具对 `example` 目录中每个日志的分析结果。

### 4. (可选) 自定义模板

如果您想调整分析逻辑，可以编辑 `~/.config/ai-test-analyze/templates/` 目录下的模板文件。例如，您可以向 `failed_pattern.template` 中添加更多您自己的失败关键词。

## 命令行

### `ai-test-analyze run [OPTIONS]`
执行分析任务。
- `path`: 要分析的日志文件或目录的路径。
- `--output`: *可选*。指定输出报告的路径和名称（无需后缀）。
- `--threads`: *可选*。并发分析的线程数。默认为 `8`。
- `--format`: *可选*。输出报告的格式，可选值为 `csv` 或 `xlsx`。默认为 `csv`。
- `--resume`: *可选*。指定一个报告文件以恢复分析。
- `--debug`: *可选*。激活调试模式。

### `ai-test-analyze config`
显示所有配置和模板文件的路径。