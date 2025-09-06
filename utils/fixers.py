import re

def fix_main_block(text):
    text = re.sub(
        r'if[\s_]*[_]+[\s_]*name[\s_]*[_]*[\s_]*(==|=)[\s_]*["\'`]{0,2}_*[_]*main_*_*["\'`]{0,2}\s*:',
        'if __name__ == "__main__":',
        text, flags=re.IGNORECASE
    )
    lines = text.split('\n')
    out = []
    for line in lines:
        l = line.strip()
        if l.startswith('if') and 'main' in l and '__name__' not in l:
            out.append('if __name__ == "__main__":')
        else:
            out.append(line)
    return '\n'.join(out)