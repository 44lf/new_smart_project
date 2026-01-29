import re
import os

# 配置：你的补丁文件名
PATCH_FILE = "codex.patch"

def apply_patch_manually():
    if not os.path.exists(PATCH_FILE):
        print(f"❌ 错误：找不到文件 {PATCH_FILE}，请确保它在当前目录下。")
        return

    print(f"🚀 开始解析 {PATCH_FILE} ...")
    
    with open(PATCH_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    current_file = None
    file_content = []
    is_new_file = False
    
    # 正则用来匹配文件名，例如: diff --git a/app/main.py b/app/main.py
    # 或者 diff --git a/.env.example b/.env.example
    file_pattern = re.compile(r'^diff --git a/(.*) b/(.*)')

    for i, line in enumerate(lines):
        # 1. 检测新文件开始
        match = file_pattern.match(line)
        if match:
            # 如果之前有正在处理的文件，先保存
            if current_file and file_content:
                save_file(current_file, file_content)
            
            # 重置状态
            #即使补丁里写的是 b/app/... 我们通常只需要 app/...
            raw_path = match.group(2).strip() 
            # 如果路径以 "ai_agent/" 开头保持不变，如果没有，根据你的目录结构可能需要调整
            # 假设 patch 里的路径是相对根目录的
            current_file = raw_path
            
            file_content = []
            is_new_file = True
            print(f"📄 发现文件: {current_file}")
            continue

        # 2. 跳过 Git 的元数据行
        if line.startswith('index ') or \
           line.startswith('new file mode') or \
           line.startswith('--- ') or \
           line.startswith('+++ ') or \
           line.startswith('@@ '):
            continue

        # 3. 提取内容
        # Git diff 中，新增的行以 "+" 开头
        if current_file:
            if line.startswith('+') and not line.startswith('+++'):
                # 去掉开头的 "+"
                content = line[1:]
                file_content.append(content)
            # 如果是空格开头，通常是上下文，但在新建文件模式下，几乎都是+
            elif line.startswith(' '):
                file_content.append(line[1:])
    
    # 保存最后一个文件
    if current_file and file_content:
        save_file(current_file, file_content)
        
    print("\n✅ 所有文件已生成完毕！")

def save_file(filepath, content_lines):
    # 确保目录存在
    dir_path = os.path.dirname(filepath)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"   📂 创建目录: {dir_path}")

    # 写入文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(content_lines)
        print(f"   💾 已写入: {filepath}")
    except Exception as e:
        print(f"   ❌ 写入失败 {filepath}: {e}")

if __name__ == "__main__":
    apply_patch_manually()