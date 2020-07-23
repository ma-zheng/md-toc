import sys, getopt


def reserveFlag(flag):
    if flag:
        return False
    else:
        return True


def generateTOC(md):
    f = open(md, encoding='UTF-8')
    all = f.readlines()
    f.close()

    hash_in_code = False
    new_file_content = []
    toc = []
    nums = [0, 0, 0, 0, 0, 0]   # 对应每级标题的个数

    for line in all:
        if line[:3] == '```':
            hash_in_code = reserveFlag(hash_in_code)
            new_file_content.append(line)                       # 以```开头是代码块
            continue
        if not hash_in_code:
            try:
                head_level, content = line.split(" ", 1)
            except ValueError:
                new_file_content.append(line)                   # 不在代码块内且无空格是普通文本
                continue

            level = 0
            for ch in head_level:
                if ch == "#":
                    level += 1
                else:
                    new_file_content.append(line)               # 有空格却不是以#开头，不是标题
                    break

            if level > 1:
                nums[level] += 1
                aid = f"{level}-{nums[level]}"
                head_with_jump = f"{'#' * level} <span id={aid}>{content.strip()}</span>\n"     # 是标题，进行添加jump
                toc.append(f"{'  '*(level-1)}* [{content.strip()}](#{aid})\n")
                new_file_content.append(head_with_jump)
            elif level == 1:
                new_file_content.append(f"{'#' * level} <span id={level}-{nums[level]+1}>{content.strip()}</span>\n")
                toc.append("**Tables of Content**\n")
        else:
            new_file_content.append(line)

    new_file = open(md, "w", encoding='UTF-8')
    for line in new_file_content[:1] + toc + new_file_content[1:]:
        new_file.write(line)
    new_file.write(f"\n\n[**Back to Top**](#1-1)\n")
    new_file.close()
    print("TOC Done!")


def main(argv):
    md_num = len(argv) - 1

    try:
        opts, args = getopt.getopt(argv, "guh", ["generate", "update", "help"])
    except getopt.GetoptError:
        print("Error format!")
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-g", "--generate"):
            for md_file in args:
                print(f"Generating TOC of {md_file}")
                generateTOC(md_file)
            sys.exit()
        elif opt in ("-u", "--update"):
            print("Update md TOC has not implements.")
            sys.exit()
        elif opt in ("-h", "--help"):
            print("\nUsage: Generate and update(future) TOC of md file using in github.\n")
            print("     mdtoc.py -g|-c md_file [md_file_1 md_file_2 ...]\n")
            print("         -g --generate | generate TOC of md")
            print("         -u --update   | update TOC of md")
            sys.exit()
        else:
            print(f"arg = {arg}")
            sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])