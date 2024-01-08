import os
import glob

from src.models import Request
from src.antcolony import AntAlgorithm
from progress.bar import IncrementalBar

def process_file(input_file):
    request = Request.from_txt(path=input_file)
    ant_algo = AntAlgorithm(request)
    return ant_algo.run()


def main(directory):
    os.chdir(directory)
    files = glob.glob("input*.txt")
    bar = IncrementalBar('Прогресс:', max = len(files))

    for input_file in files:
        
        output_file = "output" + input_file[5:]
        data = process_file(input_file)
        with open(output_file, "w") as file:
            file.write(str(len(data) - 1))
            file.write("\n")
            file.write(" ".join([str(i) for i in data][1:]))
        bar.next()
    bar.finish()

if __name__ == "__main__":
    directory = input("Введите путь к директории: ")
    main(directory)
