import argparse
import json
import os
import requests
import csv
from datetime import datetime
from pathlib import Path
import fnmatch
from tqdm import tqdm
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
import time
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- CSV字段大小限制调整 ---
csv.field_size_limit(512 * 1024)

# --- 全局常量 ---
DEFAULT_CONFIG_CONTENT = {
    "api_token": "your-api-key-here",
    "api_url": "https://api.siliconflow.cn/v1/chat/completions",
    "model": "Qwen/Qwen3-235B-A22B",
    "max_tokens": 8192, "temperature": 0.6, "top_p": 0.7,
    "directory_whitelist": ["*"], "logfile_whitelist": ["*.log", "*.txt"]
}
BASE_HEADERS = ["Root Dir", "Sub Dir 1", "Sub Dir 2", "Log File Path", "Analysis Result", "Analysis Details"]
DEBUG_HEADERS = ["Final Prompt to LLM", "LLM Reasoning & Response"]
STATUS_PENDING = "Pending"; STATUS_SUCCESS = "成功"; STATUS_FAILURE = "失败"
CSV_ENCODING = 'utf-8-sig'

# --- Excel 格式化 ---
FILL_SUCCESS = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
FILL_FAILURE = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
FILL_ERROR = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
FONT_BOLD = Font(bold=True)
ALIGNMENT_WRAP = Alignment(wrap_text=True, vertical='top')

# --- 辅助函数 ---
def get_default_config_path(): return Path.home() / ".config" / "ai-test-analyze" / "config.json"
def get_default_prompt_template_path(): return Path(__file__).resolve().parent.parent / "prompt.template"

def ensure_config_exists(config_path: Path):
    if config_path.exists(): return True
    print(f"配置文件不存在。将在 '{config_path}' 创建。")
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG_CONTENT, f, indent=4, ensure_ascii=False)
        print(f"配置文件已创建。请打开 '{config_path}' 并填入 'api_token'。")
    except Exception as e:
        print(f"创建配置文件失败: {e}")
    return False

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f: return json.load(f)

def load_prompt_template(template_path: Path):
    if not template_path.exists(): raise FileNotFoundError(f"Prompt模板文件未找到: {template_path}")
    with open(template_path, 'r', encoding='utf-8') as f: return f.read()

def find_log_files(target_path, dir_w, file_w):
    log_files = []
    base_path = Path(target_path).resolve()
    for root, dirs, files in os.walk(base_path, topdown=True):
        dirs[:] = [d for d in dirs if any(fnmatch.fnmatch(d, p) for p in dir_w)]
        for file in files:
            if any(fnmatch.fnmatch(file, p) for p in file_w):
                log_files.append(str(Path(root) / file))
    return log_files

def get_dir_parts(log_path_str: str, base_path_str: str):
    try:
        base_path = Path(base_path_str).resolve()
        log_path = Path(log_path_str).resolve()
        relative_path = log_path.relative_to(base_path)
        parts = relative_path.parent.parts
        return [base_path.name, parts[0] if parts else "", parts[1] if len(parts) > 1 else ""]
    except ValueError:
        path = Path(log_path_str)
        return [path.parent.parent.name, path.parent.name, ""]

# --- 文件操作 (CSV & Excel) ---

def initialize_report(report_path, log_files, debug, base_path):
    ext = Path(report_path).suffix
    if ext == '.csv':
        _initialize_csv(report_path, log_files, debug, base_path)
    elif ext == '.xlsx':
        _initialize_xlsx(report_path, log_files, debug, base_path)

def get_tasks_from_report(report_path):
    ext = Path(report_path).suffix
    if ext == '.csv':
        return _get_tasks_from_csv(report_path)
    elif ext == '.xlsx':
        return _get_tasks_from_xlsx(report_path)
    return [], None

def update_report_row(report_path, row_index, data, debug, lock, wb=None):
    with lock:
        ext = Path(report_path).suffix
        if ext == '.csv':
            _update_csv_row(report_path, row_index, data, debug)
        elif ext == '.xlsx' and wb:
            _update_xlsx_row(wb.active, row_index, data, debug)

def finalize_report(report_path, wb=None):
    if Path(report_path).suffix == '.xlsx' and wb:
        _finalize_xlsx(wb, report_path)

# CSV specific
def _initialize_csv(path, logs, debug, base):
    headers = BASE_HEADERS + DEBUG_HEADERS if debug else BASE_HEADERS
    with open(path, 'w', newline='', encoding=CSV_ENCODING) as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for log in logs:
            row = get_dir_parts(log, base) + [log, STATUS_PENDING, ""]
            if debug: row.extend(["", ""])
            writer.writerow(row)
    print(f"任务列表已生成: {path}。共 {len(logs)} 个文件。")

def _get_tasks_from_csv(path):
    tasks = []
    with open(path, 'r', encoding=CSV_ENCODING) as f:
        reader = csv.reader(f)
        headers = next(reader)
        path_idx = headers.index("Log File Path")
        result_idx = headers.index("Analysis Result")
        for i, row in enumerate(reader):
            if row[result_idx] == STATUS_PENDING:
                tasks.append((i + 2, row[path_idx]))
    return tasks, None

def _update_csv_row(path, index, data, debug):
    rows = list(csv.reader(open(path, 'r', encoding=CSV_ENCODING)))
    res, reason, req, resp = data
    res_idx, det_idx = BASE_HEADERS.index("Analysis Result"), BASE_HEADERS.index("Analysis Details")
    rows[index-1][res_idx], rows[index-1][det_idx] = res, reason
    if debug:
        rows[index-1][len(BASE_HEADERS)] = req
        rows[index-1][len(BASE_HEADERS)+1] = resp
    writer = csv.writer(open(path, 'w', newline='', encoding=CSV_ENCODING))
    writer.writerows(rows)

# Excel specific
def _initialize_xlsx(path, logs, debug, base):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "分析报告"
    headers = BASE_HEADERS + DEBUG_HEADERS if debug else BASE_HEADERS
    ws.append(headers)
    for cell in ws[1]: cell.font = FONT_BOLD
    for log in logs:
        row = get_dir_parts(log, base) + [log, STATUS_PENDING, ""]
        if debug: row.extend(["", ""])
        ws.append(row)
    ws.freeze_panes = 'A2'
    wb.save(path)
    print(f"报告已初始化: {path}。共 {len(logs)} 个文件。")

def _get_tasks_from_xlsx(path):
    wb = openpyxl.load_workbook(path); ws = wb.active
    tasks = []
    path_idx = BASE_HEADERS.index("Log File Path") + 1
    result_idx = BASE_HEADERS.index("Analysis Result") + 1
    for i, row in enumerate(ws.iter_rows(min_row=2)):
        if row[result_idx-1].value == STATUS_PENDING:
            tasks.append((i + 2, row[path_idx-1].value))
    return tasks, wb

def _update_xlsx_row(ws, index, data, debug):
    res, reason, req, resp = data
    res_idx, det_idx = BASE_HEADERS.index("Analysis Result")+1, BASE_HEADERS.index("Analysis Details")+1
    ws.cell(row=index, column=res_idx, value=res)
    ws.cell(row=index, column=det_idx, value=reason)
    cell_to_format = ws.cell(row=index, column=res_idx)
    if res == STATUS_SUCCESS: cell_to_format.fill = FILL_SUCCESS
    elif res == STATUS_FAILURE: cell_to_format.fill = FILL_FAILURE
    else: cell_to_format.fill = FILL_ERROR
    if debug:
        ws.cell(row=index, column=len(BASE_HEADERS)+1, value=req)
        ws.cell(row=index, column=len(BASE_HEADERS)+2, value=resp)

def _finalize_xlsx(wb, path):
    ws = wb.active
    for col in ws.columns:
        max_len = 0; col_letter = col[0].column_letter
        for cell in col:
            cell.alignment = ALIGNMENT_WRAP
            if len(str(cell.value)) > max_len: max_len = len(str(cell.value))
        ws.column_dimensions[col_letter].width = min((max_len + 2) * 1.2, 60)
    wb.save(path)

# --- Core Analysis Logic ---
def analyze_log(log_path, config, prompt_template):
    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read(4000)
    except Exception as e:
        return "文件读取错误", f"无法读取: {e}", "", ""

    prompt = prompt_template.format(log_content=log_content)
    headers = {"Authorization": f"Bearer {config['api_token']}", "Content-Type": "application/json"}
    payload = {"model": config.get("model"), "messages": [{"role": "user", "content": prompt}], "max_tokens": config.get("max_tokens"), "stream": True}
    
    buffer = ""
    reasoning_content = ""
    final_content = ""
    try:
        with requests.post(config['api_url'], headers=headers, json=payload, timeout=120, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=128):
                if not chunk:
                    continue
                
                buffer += chunk.decode('utf-8', errors='ignore')
                
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.startswith('data: '):
                        line_data = line[len('data: '):].strip()
                        if line_data == '[DONE]':
                            break
                        try:
                            json_data = json.loads(line_data)
                            delta = json_data['choices'][0]['delta']
                            
                            if delta.get('reasoning_content'):
                                reasoning_content += delta['reasoning_content']
                            if delta.get('content'):
                                final_content += delta['content']
                        except (json.JSONDecodeError, KeyError):
                            continue
        
        result, reason = "解析失败", "无法解析LLM返回"
        for line in final_content.strip().splitlines():
            if "用例分析结果：" in line: result = line.split("用例分析结果：")[1].strip()
            elif "用例分析内容：" in line: reason = line.split("用例分析内容：")[1].strip()
        
        debug_response = f"--- Reasoning ---\n{reasoning_content}\n\n--- Final Answer ---\n{final_content}"
        
        return result, reason, prompt, debug_response

    except Exception as e:
        return "API或解析错误", str(e), prompt, buffer

# --- Main Function ---
def main():
    parser = argparse.ArgumentParser(description="使用LLM并发分析日志并生成报告。")
    parser.add_argument("path", nargs='?', help="要分析的日志文件或目录。")
    parser.add_argument("--output", help="输出报告的路径。")
    parser.add_argument("--resume", help="从指定的报告文件恢复分析。")
    parser.add_argument("--format", choices=['csv', 'xlsx'], default='csv', help="输出报告的格式。")
    parser.add_argument("--threads", type=int, default=8, help="并发分析的线程数。")
    parser.add_argument("--config", default=str(get_default_config_path()), help="配置文件的路径。")
    parser.add_argument("--debug", action='store_true', help="在报告中包含LLM的Prompt和完整响应。")
    
    args = parser.parse_args()

    config = load_config(args.config)
    prompt_template = load_prompt_template(get_default_prompt_template_path())

    wb = None
    if args.resume:
        report_path = args.resume
        if not Path(report_path).exists():
            print(f"错误: 无法找到要恢复的报告 '{report_path}'"); return
        print(f"从 {report_path} 恢复分析...")
        tasks, wb = get_tasks_from_report(report_path)
    else:
        if not args.path: parser.error("必须提供 'path' 参数或使用 '--resume'。")
        base_path = str(Path(args.path).resolve())
        report_path = args.output or f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"
        log_files = find_log_files(base_path, config.get("directory_whitelist", ["*"]), config.get("logfile_whitelist", ["*.log"]))
        if not log_files: print(f"在 '{args.path}' 中没有找到匹配的日志文件。"); return
        
        initialize_report(report_path, log_files, args.debug, base_path)
        tasks, wb = get_tasks_from_report(report_path)

    if not tasks:
        print("所有任务已完成！"); return
        
    print(f"开始使用 {args.threads} 个线程并发分析 {len(tasks)} 个文件...")
    
    file_lock = threading.Lock()
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_task = {
            executor.submit(analyze_log, file_path, config, prompt_template): (row_index, file_path)
            for row_index, file_path in tasks
        }
        
        try:
            for future in tqdm(as_completed(future_to_task), total=len(tasks), desc="并发分析进度"):
                row_index, file_path = future_to_task[future]
                try:
                    result_data = future.result()
                    update_report_row(report_path, row_index, result_data, args.debug, file_lock, wb)
                except Exception as exc:
                    print(f"任务 {file_path} 生成了一个异常: {exc}")
                    error_data = ("线程异常", str(exc), "", "")
                    update_report_row(report_path, row_index, error_data, args.debug, file_lock, wb)
        finally:
            print("正在完成报告...")
            finalize_report(report_path, wb)
            print(f"分析完成！报告已保存在 {report_path}")

if __name__ == "__main__":
    main()