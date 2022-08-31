import os, sys, re, subprocess, json, argparse


class Symbol:
    def __init__(self, name, size, t):
        self.name = name
        self.size = size
        self.type = t

    def __eq__(self, s2):
        return self.name == s2.name and self.size == s2.size and self.type == s2.type

    def str(self):
        return "Symbol s:{} t:{} n:{}".format(self.size, self.type, self.name)

    def print(self):
        print(self.str())


class OutFile:
    def __init__(self, s):
        self.type_str = s
        self.file_size = 0
        self.nm_file_num_lines = 0
        self.missing_symbols = []
        
    def set_path(self, p):
        self.path = p
    
    def set_prefix(self, p):
        self.prefix = p

    def check_if_exists(self):
        if not os.path.exists(self.path):
            raise ValueError("error, file {} doesn't exists".format(self.path))
   
    def check_file_size(self):
        self.file_size = os.stat(self.path).st_size

    def generate_nm_file(self):
        self.out_dir = os.path.join("out", self.prefix)
        os.makedirs(self.out_dir, exist_ok=True)
        self.nm_file = os.path.join(self.out_dir, "nm-{}.txt".format(self.type_str))
        cmd_line = "nm.exe -l -S --size-sort {} > {}".format(self.path, self.nm_file)
        print("generate nm files using: {}".format(cmd_line))
        os.system(cmd_line)

    def load_symbols(self):
        self.nm_file_num_lines = sum(1 for line in open(self.nm_file))
        # allocate table of symbols
        self.symbols = [None for x in range(self.nm_file_num_lines)]
        with open(self.nm_file) as f:
            i = 0
            for line in f.readlines():
                name = line.split()[3]
                size = line.split()[1]
                t = line.split()[2]
                self.symbols[i] = Symbol(name, size, t)
                i += 1

    def compare_symbols(self, symlist, title):
        for s in self.symbols:
            if s not in symlist:
                self.missing_symbols.append(s)
        self.missing_symbols_file = os.path.join(self.out_dir, "missing-in-{}.txt".format(title))
        with open(self.missing_symbols_file, 'w') as f:
            for s in self.missing_symbols:
                f.write("{}\n".format(s.str()))

    def render_results(self):
        print(" ***** {} file *****".format(self.type_str))
        print(" * location: {}".format(self.path))
        print(" * size: {}".format(self.file_size))
        print(" * nm file number of line: {}".format(self.nm_file_num_lines))
        print(" * missing symbols num: {}".format(len(self.missing_symbols)))
        print(" ******************")


if __name__ == "__main__":
    print("comparing out files")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="the config file", required=True)
    args = parser.parse_args()

    with open(args.file) as json_file:
        data = json.load(json_file)
    
    file_A = OutFile("file_A")
    file_B = OutFile("file_B")
    
    file_A.set_prefix(data["filename"])
    file_B.set_prefix(data["filename"])
    
    file_A.set_path(data["fileA"]["path"])
    file_B.set_path(data["fileB"]["path"])

    file_A.check_if_exists()
    file_B.check_if_exists()
    
    file_A.check_file_size()
    file_B.check_file_size()
    
    file_A.generate_nm_file()
    file_B.generate_nm_file()

    file_A.load_symbols()
    file_B.load_symbols()

    file_A.compare_symbols(file_B.symbols, "file_B")
    file_B.compare_symbols(file_A.symbols, "file_A")
    
    file_A.render_results()
    file_B.render_results()
