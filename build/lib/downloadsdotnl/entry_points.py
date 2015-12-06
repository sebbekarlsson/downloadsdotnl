from downloadsdotnl.Searcher import Searcher
import argparse


s = Searcher()
parser = argparse.ArgumentParser()

def search():
    parser.add_argument('-s')
    parser.add_argument('-p')
    args = parser.parse_args()
    
    page = 1

    if args.p:
        page = args.p

    s.get_songs(page, args.s)

