from pathlib import Path
# deprecated
def write_into_file(market, line):
    path = Path(__file__).parent / Path('../results/' + market + '.txt')
    print(path)
    textfile = open(path , "a")
    textfile.writelines(line)
    textfile.close()