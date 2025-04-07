def extract_hidden_message(original_file, output_files, replacement='*'):
    hidden_message = ""

    with open(original_file, 'r', encoding='utf-8') as f_orig:
        original_content = f_orig.read()

    for output_file in output_files:
        with open(output_file, 'r', encoding='utf-8') as f_mod:
            modified_content = f_mod.read()

        # 查找第一个被替换的位置
        replaced_index = None
        for i, (orig_char, mod_char) in enumerate(zip(original_content, modified_content)):
            if mod_char == replacement and orig_char != replacement:
                replaced_index = i
                print(replaced_index)
                break  # 只取第一个不同的字符位置
        
        if replaced_index is not None:
            hidden_char = chr(replaced_index + 1)
            hidden_message += hidden_char

    return hidden_message

output_files = [f"output_{i+1}.txt" for i in range(0, 26)]  

# 读取隐藏信息
original_file = "base.txt"
hidden_message = extract_hidden_message(original_file, output_files)

print("flag:", hidden_message)
