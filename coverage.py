#!/usr/local/bin/pyhon
# _*_coding:utf_8_*_
# python3
import code
import copy
import fileinput
import getopt
import os
import re
import sys

version = "1.0.0"
write_coding = "UTF-8"


class CoverageData:
    def __init__(self) -> None:
        self.clear()

    def __repr__(self) -> str:
        return self.TN \
               + ":" + self.SF \
               + ":" + self.FNs.__repr__() \
               + ":" + self.FNDAs.__repr__() \
               + ":" + str(self.FNF) \
               + ":" + str(self.FNH) \
               + ":" + self.DAs.__repr__() \
               + ":" + str(self.LF) \
               + ":" + str(self.LH)

    def clear(self):
        self.TN = ""  # 测试用例名称
        self.SF = ""  # 源码文件路径
        self.FNs = {}  # 函数名及行号
        self.FNDAs = {}  # 函数名及执行次数
        self.FNF = 0  # 函数总数
        self.FNH = 0  # 函数执行数
        self.DAs = []  # 代码行及执行次数
        self.LF = 0  # 代码总行数
        self.LH = 0  # 代码执行行数


class DiffData:
    def __init__(self) -> None:
        self.clear()

    def __repr__(self) -> str:
        return (self.filename
                + ":" + str(self.old_version)
                + ":" + str(self.new_version)
                + ":" + self.blocks.__repr__())

    def clear(self):
        self.filename = ""
        self.old_version = 0
        self.new_version = 0
        self.blocks = []


class DiffBlock:
    def __init__(self) -> None:
        self.clear()

    def __repr__(self) -> str:
        return str(self.index) \
               + ":" + str(self.old_affect_begin) \
               + ":" + str(self.old_affect_lines) \
               + ":" + str(self.new_affect_begin) \
               + ":" + str(self.new_affect_lines) \
               + ":" + self.oldsub_lines.__repr__() \
               + ":" + self.newadd_lines.__repr__()

    def clear(self):
        self.index = 0
        self.old_affect_begin = 0
        self.old_affect_lines = 0
        self.new_affect_begin = 0
        self.new_affect_lines = 0
        self.oldsub_lines = []
        self.newadd_lines = []


def format_exception(etype, value, tb, limit=None, logname=None):
    """ 格式化异常信息 """
    import traceback
    result = ['Traceback信息:']
    if not limit:
        if hasattr(sys, 'tracebacklimit'):
            limit = sys.tracebacklimit
    n = 0
    while tb and (not limit or n < limit):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        locals = f.f_locals
        result.append('File %s, line %d, in %s' % (filename, lineno, name))
        try:
            result.append('(Object: %s)' %
                          locals[co.co_varnames[0]].__name__)
        except:
            pass
        try:
            result.append('(Info: %s)') % (
                str(locals['__traceback_info__']))  # type: ignore
        except:
            pass
        tb = tb.tb_next
        n += 1
    result.append(' '.join(traceback.format_exception_only(etype, value)))
    print("程序出现异常:")

    if logname is not None:
        try:
            # logname 为 None 会报错 UnboundLocalError: local variable 'logfile' referenced before assignment
            logfile = open(logname, "w")
            logfile.write('\n'.join(result))
        finally:
            if logfile is not None:
                logfile.close()
    return result


def format_exc(*exc_info):
    import traceback
    traceback.print_exc(file=sys.stdout)
    try:
        logfile = open("except.log", "w")
        traceback.print_exception(*exc_info, file=logfile)
    finally:
        if logfile is not None:
            logfile.close()


def parse_info(file_info):
    coverage_dict = {}
    coverage = CoverageData()

    for line in fileinput.input(file_info, encoding='utf-8'):
        if line.startswith('TN:'):
            charset = re.compile("TN:(.*)", re.M).match(line)
            coverage.TN = charset.group(1)
        elif line.startswith('SF:'):
            charset = re.compile("SF:(.*)", re.M).match(line)
            coverage.SF = charset.group(1)
        elif line.startswith('FN:'):
            charset = re.compile("FN:([0-9]*),(.*)\n", re.M).match(line)
            if charset is not None:
                coverage.FNs[int(charset.group(1))] = charset.group(2)
        elif line.startswith('FNDA:'):
            charset = re.compile("FNDA:([0-9]*),(.*)\n", re.M).match(line)
            if charset is not None:
                coverage.FNDAs[charset.group(2)] = int(charset.group(1))
        elif line.startswith('FNF:'):
            charset = re.compile("FNF:([0-9]*)", re.M).match(line)
            coverage.FNF = int(charset.group(1))
        elif line.startswith('FNH:'):
            charset = re.compile("FNH:([0-9]*)", re.M).match(line)
            coverage.FNH = int(charset.group(1))
        elif line.startswith('DA:'):
            charset = re.compile("DA:([0-9]*),([0-9]*)\n", re.M).match(line)
            if charset is not None:
                coverage.DAs.append([int(charset.group(1)), int(charset.group(2))])
        elif line.startswith('LF:'):
            charset = re.compile("LF:([0-9]*)", re.M).match(line)
            coverage.LF = int(charset.group(1))
        elif line.startswith('LH:'):
            charset = re.compile("LH:([0-9]*)", re.M).match(line)
            coverage.LH = int(charset.group(1))
        elif line == "end_of_record\n":
            if coverage.SF != "":
                print(coverage)
                coverage_dict[coverage.SF] = copy.deepcopy(coverage)  # 深拷贝否则会被覆盖 append默认浅拷贝
                coverage.clear()
    return coverage_dict


def parse_diff(file_diff):
    diff_dict = {}
    is_match = False
    block_index = 0
    old_sub_lines = 0
    new_add_lines = 0
    diff = DiffData()
    block = DiffBlock()
    for line in fileinput.input(file_diff, encoding='utf-8'):
        if line.startswith('Index: '):
            if len(diff.blocks) != 0:
                diff_dict[diff.filename] = diff
                print(str(diff))
                diff.clear()
                pass
            charset = re.compile(r"Index:\s(.*)", re.M).match(line)
            diff.filename = charset.group(1)
        elif line.startswith('--- '):
            charset = re.compile(
                r"---\s.*[(]revision\s([0-9].*)[)]", re.M).match(line)
            diff.old_version = int(charset.group(1))
        elif line.startswith('+++'):
            charset = re.compile(
                r"\+\+\+\s.*[(]revision\s([0-9].*)[)]", re.M).match(line)
            diff.new_version = int(charset.group(1))
        elif not re.compile(r"@@\s-([0-9]*),([0-9]*)\s+.([0-9]*),([0-9]*)\s@@", re.M).match(line) is None:
            charset = re.compile(
                r"@@\s-([0-9]*),([0-9]*)\s+.([0-9]*),([0-9]*)\s@@", re.M).match(line)
            is_match = True
            block_index += 1
            block.index = block_index
            block.old_affect_begin = int(charset.group(1))
            block.old_affect_lines = int(charset.group(2))
            block.new_affect_begin = int(charset.group(3))
            block.new_affect_lines = int(charset.group(4))
            old_sub_lines = 0
            new_add_lines = 0
        elif is_match and line.startswith(' '):
            old_sub_lines += 1
            new_add_lines += 1
        elif is_match and line.startswith('-'):
            block.oldsub_lines.append(block.old_affect_begin + old_sub_lines)
            old_sub_lines += 1
        elif is_match and line.startswith('+'):
            block.newadd_lines.append(block.new_affect_begin + new_add_lines)
            new_add_lines += 1
        else:
            pass
        if is_match and old_sub_lines == block.old_affect_lines and new_add_lines == block.new_affect_lines:
            diff.blocks.append(copy.deepcopy(block))  # 深拷贝否则会被覆盖 append默认浅拷贝
            is_match = False
            block.clear()
    return diff_dict


def refactor(diff_data, coverage_data):
    """根据diff格式化info文件"""
    coverage_data_out = copy.deepcopy(coverage_data)
    for item in diff_data.items():
        diff_key = str(item[0])
        diff_info = item[1]
        for data in coverage_data_out.items():
            coverage_key = str(data[0])
            coverage_info = data[1]
            charset = re.compile(f".*{diff_key}", re.M).match(coverage_key)
            if charset is not None:
                for block in diff_info.blocks:
                    # 计算出 清除行数 减少行数 增加行数
                    clear_lines = block.old_affect_lines if block.new_affect_lines >= block.old_affect_lines else block.new_affect_lines
                    change_lines = block.new_affect_lines - block.old_affect_lines
                    tmp_clear_lines = clear_lines
                    tmp_change_lines = change_lines
                    tmp_sub_lines = []
                    tmp_add_lines = []
                    tmp_add_line_index = 0
                    for line in coverage_info.DAs.items():
                        if line[0] == block.new_affect_begin:
                            if tmp_clear_lines != 0:
                                line[1] = 0
                                tmp_clear_lines -= 1
                            elif tmp_change_lines < 0:
                                tmp_sub_lines.append(line)
                                tmp_clear_lines += 1
                            elif tmp_change_lines > 0:
                                tmp_add_lines.append(line)
                                tmp_clear_lines -= 1
                            elif tmp_change_lines == 0:
                                if change_lines > 0:
                                    if tmp_add_line_index == 0:
                                        tmp_add_line_index = coverage_info.DAs.index(line)
                                    line[0] += change_lines  # 增加平移
                                elif change_lines < 0:
                                    line[0] -= change_lines  # 减少平移
                    for sub in tmp_sub_lines:
                        coverage_info.DAs.remove(sub)
                    for add in tmp_add_lines:
                        add[1] = 0  # 清除次数
                        coverage_info.DAs.insert(tmp_add_line_index, add)
    return coverage_data_out


def create_coverage_info(coverage_data, filename):
    """输出到文件"""
    out_data = ""
    for item in coverage_data.items():
        item_data = item[1]
        out_data += f"TN:{item_data.TN}\n"
        out_data += f"SF:{item_data.SF}\n"
        for item_fns in item_data.FNs.items():
            out_data += f"FN:{item_fns[0]},{item_fns[1]}\n"
        for item_fndas in item_data.FNDAs.items():
            out_data += f"FNDA:{item_fndas[1]},{item_fndas[0]}\n"
        out_data += f"FNF:{item_data.FNF}\n"
        out_data += f"FNH:{item_data.FNH}\n"
        for item_das in item_data.DAs:
            out_data += f"DA:{item_das[0]},{item_das[1]}\n"
        out_data += f"LF:{item_data.LF}\n"
        out_data += f"LH:{item_data.LH}\n"
        out_data += "end_of_record\n"
    fp = open(filename, "wb")
    fp.write(out_data.encode(write_coding))
    fp.close()


def schedule(file_info, file_diff):
    try:
        diff_data = parse_diff(file_diff)
        coverage_data = parse_info(file_info)
        new_coverage = refactor(diff_data, coverage_data)

        fpath, fname = os.path.split(file_info)
        fname, extname = os.path.splitext(fname)
        filename = os.path.join(fpath, f"{fname}_cov_{extname}")
        create_coverage_info(new_coverage, filename)
    except:
        format_exception(*sys.exc_info(), logname="except.log")
        format_exc(*sys.exc_info())
    finally:
        print("create C++ code from files xml... OK")


''' 
python *.py '-h -o file --help --output=out file1 file2'
opts：[('-h', ''), ('-o', 'file'), ('--help', ''), ('--output', 'out')]
args：['file1', 'file2']
'''


def main():
    global version
    file_info = r"E:\Github\python\main.info"
    file_diff = r"E:\Github\python\diff"
    if len(sys.argv) != 3:
        usage()
        exit()
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "-h-i:-d:-v", ["help", "info=", "diff=", "version"])
    except getopt.GetoptError as err:
        print(str(err))
        exit(2)
    for o, a in opts:
        if o in ['-h', "--help"]:
            usage()
            sys.exit()
        elif o in ['-i', "-info"]:
            file_info = a
        elif o in ['-d', "-diff"]:
            file_diff = a
        elif o in ['-v', "-version"]:
            print("Version is", version)
            exit()
        else:
            assert False, "未作处理"
    try:
        schedule(file_info, file_diff)
    except Exception as e:
        print(str(e))


def usage():
    print("\t--info:lcov生成info文件\n\t--diff:当前修改的diff文件")
    print("\teg: python --info=main.info --diff=main.diff")
    print(f"\tcur version: {version}")


if __name__ == "__main__":
    main()
