#!/usr/local/bin/pyhon
#_*_coding:utf_8_*_

from xml.dom import minidom
import xlrd, os, sys, re, getopt
from chardet import detect

field_name_row = 0
var_name_row = 1
type_name_row = 2
data_begin_row = 3
namespace = "XmlConfig"
struct_name_suffix = "_t"
cpp_var_type = "Fir::VarType"
cpp_xmlparser_no_const = "Fir::XMLParser"
cpp_xmlparser = "const Fir::XMLParser"
cpp_xmlparser_node = "const Fir::XMLParser::Node"
write_coding = "UTF-8"

'''
# 第一个参数为函数，第二个参数为列表 依次遍历 第二个参数 为第一个函数的参数
def square(x) :  return x ** 2
map(square, [1,2,3,4,5])   # 计算列表各个元素的平方
map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])
map(lambda x: x ** 2, [1, 2, 3, 4, 5])  # 使用 lambda 匿名函数
'''
def file_ext_name(*endstring): # *endstring 多个参数
    def run(s): # 匿名函数 闭包
        f = list(map(s.endswith, endstring)) 
        if True in f:
             return s
    return run

def get_file_name(filename):
    fpath, fname = os.path.split(filename)
    fname, extname = os.path.splitext(fname)
    return fname

'''
open函数如果不用二进制方式打开，同时不指定编码或者指定编码错误，会有可能报错
    try:
        charset = re.compile(".*\s*encoding=\"([^\"]+)\".*", re.M).match(content).group(1)
    except:
        charset = write_coding
    if charset.upper != write_coding:
        content = re.sub(charset, write_coding, content)
        content = content.decode(charset).encoding(write_coding)
'''
# 读取文件并返回xml结构
def read_xml(fname):
    fp = open(fname, "rb")
    content = fp.read()
    fp.close()
    try:
        charset = detect(content)["encoding"]
    except:
        charset = write_coding
    try:
        content = content.decode(charset.upper())
    except:
        if charset.upper() != write_coding:
            print("detect%s猜测解码失败,默认尝试%s解码" %(detect(content), write_coding))
            content = content.decode(charset.upper())
    return minidom.parseString(content)

def create_load_vector_func(tab_char):
    code = ""
    code += tab_char + "template <typename T>\n"
    code += tab_char + "void load_vector(std::string vec_name, std::string sub_nodename, std::vector<T> &var, {0} &xml, {1} *node) {{\n".format(cpp_xmlparser, cpp_xmlparser_node)
    code += tab_char + "\tif (NULL == node) return;\n"
    code += tab_char + "\t{0} *vec_node = xml.child(node, \"vector\");\n".format(cpp_xmlparser_node)
    code += tab_char + "\twhile (vec_node) {\n"
    code += tab_char + "\t\tif (xml.node_attribute(vec_node, \"var\") == vec_name) {\n"
    code += tab_char + "\t\t\tvar.resize(xml.child_count(vec_node, sub_nodename.c_str()));\n"
    code += tab_char + "\t\t\t{0} *sub_node = xml.child(vec_node, sub_nodename.c_str());\n".format(cpp_xmlparser_node)
    code += tab_char + "\t\t\tsize_t i = 0;\n"
    code += tab_char + "\t\t\twhile (sub_node && i < var.size()) {\n"
    code += tab_char + "\t\t\t\tvar[i].load(xml, sub_node);\n"
    code += tab_char + "\t\t\t\t++i;\n"
    code += tab_char + "\t\t\t\tsub_node = xml.next(sub_node, sub_nodename.c_str());\n"
    code += tab_char + "\t\t\t}\n"
    code += tab_char + "\t\t\tbreak;\n"
    code += tab_char + "\t\t}\n"
    code += tab_char + "\t\tvec_node = xml.next(vec_node, \"vector\");\n"
    code += tab_char + "\t}\n"
    code += tab_char + "}\n\n"
    code += tab_char + "static void load_vartype_vector(std::string vec_name, std::vector<{0}> &var, {1} &xml, {2} *node) {{\n".format(cpp_var_type, cpp_xmlparser, cpp_xmlparser_node)
    code += tab_char + "\tif (NULL == node) return;\n"
    code += tab_char + "\t{0} *vec_node = xml.child(node, \"vector\");\n".format(cpp_xmlparser_node)
    code += tab_char + "\twhile (vec_node) {\n"
    code += tab_char + "\t\tif (xml.node_attribute(vec_node, \"var\") == vec_name) {\n"
    code += tab_char + "\t\t\t{0} *sub_node = xml.child(vec_node, NULL);\n".format(cpp_xmlparser_node)
    code += tab_char + "\t\t\twhile (sub_node) { \n"
    code += tab_char + "\t\t\t\tvar.push_back(xml.node_value(sub_node));\n"
    code += tab_char + "\t\t\t\tsub_node = xml.next(sub_node, NULL);\n"
    code += tab_char + "\t\t\t}\n"
    code += tab_char + "\t\t\tbreak;"
    code += tab_char + "\t\t}\n"
    code += tab_char + "\t\tvec_node = xml.next(vec_node, \"vector\");\n"
    code += tab_char + "\t}\n"
    code += tab_char + "}\n\n"
    return code

def create_define_file(out_dir, struct_code):
    code = ""
    code += "#ifndef __XML_CONFIG_DEFINE_H__\n"
    code += "#define __XML_CONFIG_DEFINE_H__\n"
    code += "#include <map>\n"
    code += "#include <vector>\n"
    code += "#include \"vartype.h\"\n"
    code += "#include \"xmlparser.h\"\n"
    code += "\n"
    code += "namespace {0} {{\n\n".format(namespace)
    code += create_load_vector_func("\t")
    code += struct_code
    code += "}\n\n"
    code += "#endif\n\n"
    filename = os.path.join(out_dir, "xmlconfig_define.h")
    fp = open(filename, "wb")
    fp.write(code.encode(write_coding))
    fp.close()

def create_code(out_dir, xmlfiles):
    func_declare = ""
    struct_declare = ""
    func_define = ""
    struct_load = ""
    for xmlname in xmlfiles:
        func_declare += "\tconst {0}{1} &{0}();\n".format(xmlname, struct_name_suffix)
        func_declare += "\tbool reset{0}(const {1}::ReadXmlFunc &func);\n\n".format(xmlname, namespace)
        struct_declare += "\tstatic {0}{1} *_{0} = NULL;\n".format(xmlname, struct_name_suffix)
        func_define += "\tconst {0}{1} &{0}() {{\n\t\tif (NULL == _{0})\n\t\t{{\n\t\t\tzLogger::debug(\"[XML配置], 加载 ExampleSecond.xml 未初始化\");\n\t\t\t_{0} = new {0}{1}();\n\t\t}}\n\t\treturn *_{0};\n\t}}\n".format(xmlname, struct_name_suffix)
        func_define += "\tbool reset{0}(const {1}::ReadXmlFunc &func) {{\n\t\t{2} xml;\n\t\tif (_{0}) {{\n\t\t\tdelete _{0};\n\t\t\t_{0} = NULL;\n\t\t}}\n\t\t_{0} = new {0}{3};\n\t\t_{0}->load(xml, func(xml, \"{0}.xml\"));\n\t\tzLogger::debug(\"[XML配置] 加载 {0}.xml 成功\");\n\t\treturn true;\n\t}}\n\n".format(xmlname, namespace, cpp_xmlparser_no_const, struct_name_suffix)
        struct_load += "\t\tif (_{0}) {{\n\t\tdelete _{0};\n\t\t\t_{0} = NULL;\n\t\t}}\n\t\t_{0} = new {0}{1};\n\t\t_{0}->load(xml, func(xml, \"{0}.xml\"));\n\t\tzLogger::debug(\"[XML配置], 加载 {0}.xml 成功\");\n".format(xmlname, struct_name_suffix)
        struct_load += "\t\tfileResetMap.insert(std::make_pair(\"{0}\", reset{0}));\n".format(xmlname)
    # 生成.h
    code = ""
    code += "#ifndef __XML_CONFIG_H__\n"
    code += "#define __XML_CONFIG_H__\n"
    code += "#include <functional>\n"
    code += "#include \"xmlconfig_define.h\"\n"
    code += "\n"
    code += "namespace {0} {{\n\n".format(namespace)
    code += "\ttypedef std::function<{0} *({1} &, const char *)>\tReadXmlFunc;\n\n".format(cpp_xmlparser_node, cpp_xmlparser_no_const)
    code += "\tbool existConfig(const std::string &fileName);\n\n"
    code += "\tbool loadConfig(const std::string &fileName, const {0}::ReadXmlFunc &fun);\n\n".format(namespace)
    code += "\tvoid init(const {0}::ReadXmlFunc &func);\n\n".format(namespace)
    code += func_declare
    code += "}\n\n"
    code += "#endif\n\n"
    filename = os.path.join(out_dir, "xmlconfig.h")
    fp = open(filename, "wb")
    fp.write(code.encode(write_coding))
    fp.close()

    # 生成cpp
    code = ""
    code += "#include \"xmlconfig.h\"\n"
    code += "#include \"zLogger.h\"\n"
    code += "\n"
    code += "namespace {0} {{\n\n".format(namespace)
    code += "\tstatic std::map<std::string, bool (*)(const {0}::ReadXmlFunc &)> fileResetMap = std::map<std::string, bool (*) (const {0}::ReadXmlFunc &)>();\n\n".format(namespace)
    code += struct_declare
    code += "\n"
    code += "\tbool existConfig(const std::string &fileName) {\n"
    code += "\t\treturn fileResetMap.find(fileName) != fileResetMap.end();\n"
    code += "\t}\n"
    code += "\n"
    code += "\tbool loadConfig(const std::string &fileName, const {0}::ReadXmlFunc &func) {{\n".format(namespace)
    code += "\t\tconst auto iter = fileResetMap.find(fileName);\n"
    code += "\t\tif (iter != fileResetMap.end())\n"
    code += "\t\t\treturn iter->second(func);\n"
    code += "\t\treturn false;\n"
    code += "\t}\n"
    code += "\n"
    code += "\tvoid init(const {0}::ReadXmlFunc &func) {{\n".format(namespace)
    code += "\t\tfileResetMap.clear();\n"
    code += "\t\t{0} xml;\n".format(cpp_xmlparser_no_const)
    code += struct_load
    code += "\t}\n"
    code += "\n"
    code += func_define
    code += "}\n\n"
    filename = os.path.join(out_dir, "xmlconfig.cpp")
    fp = open(filename, "wb")
    fp.write(code.encode(write_coding))
    fp.close()

'''

'''
def create_struct(name, objects, tab_char, prefix):
    code = ""
    cpp = ""
    struct_list = objects["struct"]
    var_list = objects["var"]
    code += tab_char + "struct {0}{1} {{\n".format(name, struct_name_suffix)
    if len(struct_list) > 0:
        code += tab_char + "\tpublic:\n"
        for struct_name in sorted(struct_list):
            objs = struct_list[struct_name]
            pre = ""
            if prefix == "":
                pre = name + "_t"
            else:
                pre = prefix + "::" + name + "_t"
            co, cp = create_struct(struct_name, objs, tab_char+"\t\t", pre)
            code += co
            cpp += cp
    if len(var_list) > 0:
        code += tab_char + "\tpublic:\n"
        code += tab_char + "\t\tvoid load({0} &xml, {1} *node);\n".format(cpp_xmlparser, cpp_xmlparser_node)
        cpp += "\tvoid "
        fix = prefix
        if len(fix) == 0:
            fix = name + "_t" "::"
        else:
            fix += "::"+ name + "_t" + "::"
        cpp += fix + "load({0} &xml, {1} *node) {{\n".format(cpp_xmlparser, cpp_xmlparser_node)
        cpp += "\t\tif (!node)\n"
        cpp += "\t\t\treturn;\n"
        cpp += create_load_var_code(objects, "\t\t")
        cpp += "\t}\n"
        cpp += "\n"
        for var_name in sorted(var_list):
            var_type = var_list[var_name]
            if var_type in struct_list.keys():
                var_type += struct_name_suffix
            code += tab_char + "\t\tconst {0} &{1}()const {{ return _{1}; }}\n".format(var_type, var_name)
        code += "\n"
        code += tab_char + "\tprivate:\n"
        for var_name in sorted(var_list):
            var_type = var_list[var_name]
            if var_type in struct_list.keys():
                var_type += struct_name_suffix
            code += tab_char + "\t\t{0} _{1};\n".format(var_type, var_name)
    code += tab_char + "};\n\n"
    return code, cpp

def create_load_map_code(var_name, var_type, objects, tab_char):
    code = ""
    struct_list = objects["struct"]
    map_type = var_type[var_type.find(", ") + 2 : var_type.find(" >")]
    no_suffix = map_type[0 : -len(struct_name_suffix)]
    code += tab_char + "{1} *map_{0}_node = xml.child(node, \"map\");\n".format(var_name, cpp_xmlparser_node)
    code += tab_char + "while (map_{0}_node) {{\n".format(var_name)
    code += tab_char + "\tif (xml.node_attribute(map_{0}_node, \"var\") == \"{0}\") {{\n".format(var_name)
    code += tab_char + "\t\t{0} keyname = xml.node_attribute(map_{1}_node, \"key\");\n".format(cpp_var_type, var_name)
    if no_suffix in struct_list.keys():
        map_type = no_suffix
        code += tab_char + "\t\t{2} *sub_node = xml.child(map_{0}_node, \"{1}\");\n".format(var_name, map_type, cpp_xmlparser_node)
        code += tab_char + "\t\twhile (sub_node) {\n"
        code += tab_char + "\t\t\t_{0}[xml.node_attribute(sub_node, keyname)].load(xml, sub_node);\n".format(var_name)
        code += tab_char + "\t\t\tsub_node = xml.next(sub_node, \"{0}\");\n".format(map_type)
        code += tab_char + "\t\t}\n"
    elif map_type == cpp_var_type: # map必定有一个key， 不会为 VarType
        code += tab_char + "\t\t{1} *sub_node = xml.child(map_{0}_node, NULL);\n".format(var_name, cpp_xmlparser_node)
        code += tab_char + "\t\twhile (sub_node) {\n"
        code += tab_char + "\t\t\t_{0}[xml.node_attribute(sub_node, keyname)] = xml.node_value(sub_node);\n".format(var_name)
        code += tab_char + "\t\t\tsub_node = xml.next(sub_node, NULL);\n"
        code += tab_char + "\t\t}\n"
    else:
        code += tab_char + "\t\t_{0} = error;\n".format(var_name)
        print ("暂不支持容器嵌套，请使用节点嵌套！！！ map：", var_name)
    code += tab_char + "\t\tbreak;\n"
    code += tab_char + "\t}\n"
    code += tab_char + "\tmap_{0}_node = xml.next(map_{0}_node, \"map\");\n".format(var_name)
    code += tab_char + "}\n"
    return code

def create_load_vector_code(var_name, var_type, objects, tab_char):
    code = ""
    struct_list = objects["struct"]
    vec_type = var_type[ var_type.find("<") + 2 : var_type.find(" >") ]
    no_suffix = vec_type[ 0 : -len(struct_name_suffix) ]
    if no_suffix in struct_list.keys():
        code += tab_char + "load_vector< {0} >(\"{1}\", \"{2}\", _{1}, xml, node);\n".format(vec_type, var_name, no_suffix)
    elif vec_type == cpp_var_type:
        code += tab_char + "load_vartype_vector(\"{0}\", _{0}, xml, node);\n".format(var_name)
    else:
        code += tab_char + "_{0} = error;\n".format(var_name)
        print ("暂不支持容器嵌套，请使用节点嵌套！！！ vector:", var_name)
    return code

def create_load_var_code(objects, tab_char):
    code = ""
    struct_list = objects["struct"]
    var_list = objects["var"]
    for var_name in sorted(var_list):
        var_type = var_list[var_name]
        if var_type in struct_list.keys():
            code += tab_char + "{1} *{0}_node = xml.child(node, \"{0}\");\n".format(var_name, cpp_xmlparser_node)
            code += tab_char + "while ({0}_node) {{\n".format(var_name)
            code += tab_char + "\t_{0}.load(xml, {0}_node);\n".format(var_name)
            code += tab_char + "\t{0}_node = xml.next({0}_node, \"{0}\");\n".format(var_name)
            code += tab_char + "}\n"
        else:
            if var_type[0:11] == "std::vector":
                code += create_load_vector_code(var_name, var_type, objects, tab_char)
            elif var_type[0:8] == "std::map":
                code += create_load_map_code(var_name, var_type, objects, tab_char)
            else:
                code += tab_char + "if (!xml.has_attribute(node, \"{0}\")) {{\n".format(var_name)
                code += tab_char + "\t{0} *sub = xml.child(node, \"{1}\");\n".format(cpp_xmlparser_node, var_name)
                code += tab_char + "\tif (sub)\n"
                code += tab_char + "\t\t_{0} = xml.node_value(sub);\n".format(var_name)
                code += tab_char + "}\n"
                code += tab_char + "else {\n"
                code += tab_char + "\t_{0} = xml.node_attribute(node, \"{0}\");\n".format(var_name)
                code += tab_char + "}\n"
    return code


'''
从根节点开始，逐层 解析每个元素 struct var
#objcets = { "struct":{ "struct_name":{} }, "var":{"var_name":"type_name"} }
#objects = { "struct":{}, "var":{} }
'''
def parse_node(node, objects): # node:当前节点 objects:
    struct_list = objects["struct"]
    var_list = objects["var"]
    for name, value in node.attributes.items(): 
        var_list[name] = cpp_var_type
    for sub_node in node.childNodes:
        if sub_node.nodeType == sub_node.ELEMENT_NODE: # 判断是否是元素节点
            var_name = var_type = sub_node.nodeName
            if sub_node.nodeName == "vector":
                var_name = sub_node.getAttribute("var")
                if var_name == "":
                    continue # 容器必须显示以var属性指定变量名，负责忽略此节点
                container_type = get_container_type(sub_node, struct_list)
                if container_type in struct_list.keys():
                    var_type = "std::vector< {0}{1} >".format(container_type, struct_name_suffix)
                else:
                    var_type = "std::vector< {0} >".format(container_type)
            elif sub_node.nodeName == "map":
                var_name = sub_node.getAttribute("var")
                if var_name == "":
                    continue
                keyname = sub_node.getAttribute("key")
                if keyname == "":
                    continue # map 必须显示声明keyname, 否则忽略这个节点
                container_type = get_container_type(sub_node, struct_list)
                if container_type in struct_list.keys():
                    var_type = "std::map< {0}, {1}{2} >".format(cpp_var_type, container_type, struct_name_suffix)
                else:
                    var_type = "std::map< {0}, {1} >".format(cpp_var_type, container_type)
            else:
                sub_objs = None
                if sub_node.nodeName in struct_list.keys():
                    sub_objs = struct_list[sub_node.nodeName]
                    parse_node(sub_node, sub_objs)
                else:
                    sub_objs = { "struct":{}, "var":{} }
                    parse_node(sub_node, sub_objs)
                    if len(sub_objs["var"]) > 0:
                        struct_list[sub_node.nodeName] = sub_objs
                    else:
                        var_type = cpp_var_type
            if var_name not in var_list:
                var_list[var_name] = var_type

def get_container_type(node, struct_list):
    var_type = ""
    is_vec = False
    is_map = False
    for sub_node in node.childNodes:
        if sub_node.nodeType == sub_node.ELEMENT_NODE:
            if var_type == "":
                var_type = sub_node.nodeName
            if sub_node.nodeName !=var_type:
                continue
            if sub_node.nodeName == "vector":
                container_type = get_container_type(sub_node, struct_list)
                var_type = "std::vector< {0}{1} >".format(container_type, struct_name_suffix)
                is_vec = True
            elif sub_node.nodeName == "map":
                keyname = sub_node.getAttribute("key")
                if keyname == "":
                    continue
                container_type = get_container_type(sub_node, struct_list)
                var_type = "std::map< {0}, {1}{2} >".format(cpp_var_type, container_type, struct_name_suffix)
                is_map = True
            else:
                sub_objs = None
                if sub_node.nodeName in struct_list.keys():
                    sub_objs = struct_list[sub_node.nodeName]
                    parse_node(sub_node, sub_objs)
                else:
                    sub_objs = { "struct":{}, "var":{} }
                    parse_node(sub_node, sub_objs)
                    if len(sub_objs["var"]) > 0:
                        struct_list[sub_node.nodeName] = sub_objs
                        var_type = sub_node.nodeName
    if not is_vec and not is_map and var_type not in struct_list.keys():
        var_type = cpp_var_type
    return var_type

'''
filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回一个迭代器对象，如果要转换为列表，可以使用 list() 来转换。
该接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，然后返回 True 或 False，最后将返回 True 的元素放到新列表中。
'''
def extract_xml(in_dir, out_dir):
    files = list(filter(file_ext_name(".xml"), os.listdir(in_dir)))
    files.sort()
    code = ""
    xmlfiles = []
    for fname in files:
        filename = os.path.join(in_dir, fname)
        print("parse %s ... " %filename)
        xmlname = get_file_name(filename)
        xmlfiles.append(xmlname)
        xml = read_xml(filename) # xml文件根节点只能有一个否则加载失败
        root = xml.documentElement 
        objects = { "struct":{}, "var":{} }
        parse_node(root, objects) # 解析所有结构
        co, cp = create_struct(xmlname, objects, "\t", "")
        code += co
        cp = "#include \"xmlconfig_define.h\"\n" + "\nnamespace {0} {{\n\n".format(namespace) + cp + "}\n\n"
        cppfilename = os.path.join(out_dir, fname.split('.')[0] + ".cpp")
        cppfile = open(cppfilename, "wb")
        cppfile.write(cp.encode(write_coding)) # 创建每个结构体的load函数
        cppfile.close()
        print ("OK")
    create_define_file(out_dir, code) # 创建结构体定义文件
    create_code(out_dir, xmlfiles)

#格式化异常信息
def format_exception(etype, value, tb, limit=None, logname=None):
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
        result.append('File %s, line %d, in %s' %(filename, lineno, name))
        try:
            result.append('(Object: %s)' %(locals[co.co_varnames[0]].__name__))
        except:
            pass
        try:
            result.append(result.append('(Info:%s)') %(str(locals['__traceback_info__'])))
        except:
           pass
        tb = tb.tb_next
        n += 1
    result.append(' '.join(traceback.format_exception_only(etype, value)))
    print ("程序出现异常:")

    if not logname is None:
        try:
            logfile = open(logname, "w") # logname 为 None 会报错 UnboundLocalError: local variable 'logfile' referenced before assignment
            logfile.write('\n'.join(result))
        finally:
            if not logfile is None:
                logfile.close()
    return result

def format_exc(*exc_info):
    import traceback
    traceback.print_exc(file=sys.stdout)
    try:
        logfile = open("except.log", "w")
        traceback.print_exception(*exc_info, file=logfile)
    finally:
        if not logfile is None:
            logfile.close()

def schedule(in_dir, out_dir):
    try:
        extract_xml(in_dir, out_dir)
    except:
        format_exception(*sys.exc_info(), logname="except.log")
        format_exc(*sys.exc_info())
    finally:
        print ("create C++ code from files xml... OK")


''' 
python *.py '-h -o file --help --output=out file1 file2'
opts：[('-h', ''), ('-o', 'file'), ('--help', ''), ('--output', 'out')]
args：['file1', 'file2']
'''
def main():
    # reload(sys) python3 无需重新加载编码 默认无 unicode importlib.reload(sys)
    # sys.setdefaultencoding(write_coding)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "in_dir=", "out_dir="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    in_dir = "."
    out_dir = "."
    for o, a in opts:
        if o in ['-h', "--help"]:
            usage()
            sys.exit()
        elif o == "--in_dir":
            in_dir = a
        elif o == "--out_dir":
            out_dir = a
        else:
            assert False, "未作处理"
    try:
       schedule(in_dir, out_dir)
    except Exception as e:
       print(str(e))

def usage():
    print("\n\t--in_dir:xml文件目录\n\t--out_dir:输出生成代码目录")
    print(r'eg: python .\python\xmlbind.py --in_dir="Config\" --out_dir="Config\"')

if __name__ == "__main__":
    main()