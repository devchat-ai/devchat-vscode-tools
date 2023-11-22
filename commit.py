"""
commit.py: 通过几个步骤完成提交。

具体步骤包含：
1. 获取当前修改文件列表；
2. 获取用户选中的修改文件；
    a. 标记出已经staged的文件；
    b. 获取用户选中的文件；
    c. 根据用户选中文件，重新构建stage列表；
3. 获取用户选中修改文件的Diff信息；
4. 生成提交信息；
5. 展示提交信息并提交。

注意： 步骤2.c, 步骤5有专门的函数实现，本脚本中不需要具体这两个步骤的实现。
"""

import os
import sys
import re
import json
import subprocess


def output_message(output):
    out_data = f"""\n<<Start>>\n{output}\n<<End>>\n"""
    print(out_data)

def pipe_interaction(output: str):
    output_message(output)

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == '<<End>>':
                break
            elif line.strip() == '<<Start>>':
                continue
            lines.append(line)
        except EOFError:
            pass

    replay_message = '\n'.join(lines)
    # replay_message is a json string
    # {"commit_message": "some text", "commit": true}
    # parse replay_message by json module
    replay_object = json.loads(replay_message)
    return replay_object


def extract_info(text):
    pattern = r"User: (?P<user>[^\n]*)\nDate: (?P<date>[^\n]*)\n(?P<content>.*)\nprompt (?P<prompt>.*)"
    match = re.search(pattern, text, re.S)
    if match:
        return match.groupdict()
    else:
        return None

def call_gpt(input: str) -> str:
    """
    This function calls GPT through the devchat chat command.
    It takes a string as input and returns a string as output.

    Args:
        input (str): The input string to send to GPT.
        prompt (str): The prompt string to send to GPT.

    Returns:
        str: The output string from GPT.
    """
    new_prompt = input
    
    # call devchat chat {new_prompt}
    # devchat is a command line tool that calls GPT through the OpenAI API
	# set PYTHONPATH to environment variable PYTHONLIBPATH
    pythonLibPath = os.environ.get("PYTHONLIBPATH")
    pythonBinPath = os.environ.get("DEVCHATPYTHON")
    result = subprocess.run([pythonBinPath, "-m", "devchat", "-m", "gpt-3.5-turbo-16k", 'prompt', new_prompt], capture_output=True, text=True, env={"PYTHONPATH": pythonLibPath})

    if result.returncode != 0:
        print(result.stderr)
        raise Exception(f"Error in calling GPT: {result.stderr}")

    info = extract_info(result.stdout)
    return info

def get_modified_files():
    """ 获取当前修改文件列表以及已经staged的文件列表"""
    output = subprocess.check_output(["git", "status", "-s"])
    output = output.decode('utf-8')
    lines = output.split('\n')
    modified_files = []
    staged_files = []
    
    def strip_file_name(file_name):
        file = file_name.strip()
        if file.startswith('"'):
            file = file[1:-1]
        return file

    for line in lines:
        if len(line) > 2:
            status, filename = line[:2], line[3:]
            modified_files.append(strip_file_name(filename))
            if status == "M " or status == "A ":
                staged_files.append(strip_file_name(filename))
    return modified_files, staged_files
 
def get_file_summary(modified_files, staged_files):
    """ 当modified_files文件列表<=5时，根据项目修改差异生成每一个文件的修改总结 """
    diffs = []
    for file in modified_files:
        if file not in staged_files:
            subprocess.check_output(["git", "add", file])
        diff = subprocess.check_output(["git", "diff", "--cached", file])
        if file not in staged_files:
            subprocess.check_output(["git", "reset", file])
        diffs.append(diff.decode('utf-8'))
    # total_diff = subprocess.check_output(["git", "diff", "HEAD"])
    total_diff_decoded = '\n'.join(diffs) #  total_diff.decode('utf-8')
    
    if len(total_diff_decoded) > 15000:
        return {}

    # 在prompt中明确处置AI模型的输出格式需求
    prompt = f""" 
    I have made the following changes: 
    ```{total_diff_decoded}```
    Please provide a summary for each modified file. The output should ONLY be a JSON format like: 
    {{"file1": "Summary of the changes made in file1", 
    "file2": "Summary of the changes made in file2"}}
    Please make sure there is no other additional output.
    """
    file_summaries = call_summary_AI(prompt)

    return file_summaries


def call_summary_AI(prompt):
    # 此处应该是调用AI模型并处理返回结果的代码
    try:
        response = call_gpt(prompt)
        info = json.loads(response["content"])
        return info
    except:
        return {}


def get_marked_files(modified_files, staged_files, file_summaries):
    """ 获取用户选中的修改文件及已经staged的文件"""
    # Coordinate with user interface to let user select files.
    # assuming user_files is a list of filenames selected by user.

    out_str = "```chatmark\n"
    out_str += "Staged:\n"
    for file in staged_files:
        out_str += f"- [x] {file} {file_summaries.get(file, '')}\n"
    out_str += "Unstaged:\n"
    for file in modified_files:
        if file in staged_files:
            continue
        out_str += f"- [] {file} {file_summaries.get(file, '')}\n"
    out_str += "```"
    
    replay_object = pipe_interaction(out_str)
    select_files = replay_object["select_files"]
    return staged_files

def rebuild_stage_list(user_files):
    """ 根据用户选中文件，重新构建stage列表 """
    # Unstage all files
    subprocess.check_output(["git", "reset"])
    # Stage all user_files
    for file in user_files:
        os.system(f"git add \"{file}\"")
    
def get_diff():
    """ 获取staged files的Diff信息 """
    return subprocess.check_output(["git", "diff", "--cached"])

def generate_commit_message_base_diff(user_input, diff):
    """ Based on the diff information, generate a commit message through AI """
    prompt = f"""
    I have made the following changes to the code:
    ```
    {diff}
    ```
    Please help me generate a commit message. {user_input}. If you don't know exact closed issue number, please don't output "Closes #Issue_number" line. The format is as follows:
    feat: commit message title
    
    Commit message body:
    - Detailed message 1.
    - Detailed message 2.
    
    Closes #Issue_number
    """
    response = call_gpt(prompt)
    return response


def display_commit_message_and_commit(commit_message):
    """ 展示提交信息并提交 """
    commit_message_with_flag = f"""
```editor
{commit_message["content"]}
```
    """
    replay_object = pipe_interaction(commit_message_with_flag)
    new_commit_message, commit = replay_object["commit_message"], replay_object["commit"]

    if commit:
        subprocess.check_output(["git", "commit", "-m", new_commit_message])


if __name__ == '__main__':
    user_input = sys.argv[1]

    modified_files, staged_files = get_modified_files()
    file_summaries = get_file_summary(modified_files, staged_files)
    selected_files = get_marked_files(modified_files, staged_files, file_summaries)
    rebuild_stage_list(selected_files)
    diff = get_diff()
    commit_message = generate_commit_message_base_diff(user_input, diff)
    display_commit_message_and_commit(commit_message)
    output_message("""\n```progress\n\nDone\n\n```""")
