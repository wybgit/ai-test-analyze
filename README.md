# AI-Test-Analyze: AI 驱动的日志分析工具

`ai-test-analyze` 是一个命令行的效率工具，它利用大语言模型（LLM）的强大能力，通过多线程并发，快速分析指定的测试日志文件，并生成一个结构化、可选格式的分析报告。

## 核心功能

- **多线程并发分析**：通过 `--threads` 参数指定线程数（默认为8），大幅缩短分析大量日志文件所需的时间。
- **智能判断**：根据自定义的 Prompt，智能判断用例的成功或失败。
- **双格式报告**：
    - **CSV 或 Excel**：通过 `--format` 参数自由选择输出 `.csv` 或 `.xlsx` 格式。
    - **精美排版 (Excel)**：选择 `xlsx` 格式时，报告将自动应用颜色标记、自动列宽、文本换行和固定表头，极大提升可读性。
- **实时进度**：使用总进度条实时显示并发分析的完成进度。
- **断点续传**：支持从上次中断的报告（CSV 或 Excel）继续分析，无需重复工作。
- **增强的调试模式**：提供 `--debug` 选项，可在报告中额外记录**最终发送给 LLM 的 Prompt** 和 **LLM 返回的、包含思考过程和最终答���的完整响应**。
- **高度可配置**：通过 `config.json` 和 `prompt.template` 文件，轻松定制工具的行为。

## 安装

在项目根目录下，运行以下命令进行安装或更新。该命令会自动处理所有依赖库。

```bash
pip install .
```

## 打包与分发

项目包含一个一键式打包脚本，用于生成可分发的 `.whl` 文件。

1.  **确保脚本可执行** (只需首次执行):
    ```bash
    chmod +x build.sh
    ```

2.  **运行打包脚本**:
    ```bash
    ./build.sh
    ```

脚本会自动清理旧的构建产物，并生成一个新的 wheel 文件到 `dist/` 目录下。你可以将这个 `.whl` 文件分发给他人，他们可以通过以下命令进行安装：

```bash
pip install /path/to/the/generated-wheel-file.whl
```

## 快速开始

### 1. 首次运行与配置

首次运行 `ai-test-analyze` 时，程序会自动在 `~/.config/ai-test-analyze/config.json` 创建配置文件。请根据提示，打开该文件并填入您的 `api_token`。

### 2. 执行分析

将工具指向包含日志文件的根目录。

**使用默认的8个线程进行分析：**
```bash
ai-test-analyze /path/to/your/logs
```

**指定16个线程，并输出为 Excel 报告：**
```bash
ai-test-analyze /path/to/your/logs --threads 16 --format xlsx
```

### 3. 中断与恢复

如果分析中断，使用 `--resume` 参数指向之前生成的报告文件即可。程序将使用与新命令中指定的相同线程数继续执行剩余任务。

```bash
ai-test-analyze --resume ./analysis_report_20250701_103000.xlsx --threads 16
```

### 4. 调试模式

如果需要深入分析 LLM 的行为，请使用 `--debug` 标志。

```bash
ai-test-analyze /path/to/your/logs --debug --threads 4
```

## 命令行选项

- `path`: 要分析的日志文件或目录的路径。**（与 `--resume` 冲突）**
- `--threads`: *可选*。并发分析的线程数。默认为 `8`。
- `--format`: *可选*。输出报告的格式，可选值为 `csv` 或 `xlsx`。默认为 `csv`。
- `--resume`: *可选*。指定一个报告文件（.csv 或 .xlsx）以恢复分析。
- `--output`: *可选*。为新任务指定输出报告的路径。
- `--config`: *可选*。指定一个自定义的配置文件路径。
- `--debug`: *可选*。激活调试模式，在报告中记录最终的Prompt和包含思考过程的LLM响应。

---
由 Gemini 强力驱动
