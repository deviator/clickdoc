#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import datetime

import subprocess as sp
import os
import os.path as opath
import sys
import shutil

tvars_list = [ 'advtheme', 'keywords', 'website', 'ordernums' ]

def main():

    output = getOutputName()

    tvars = getVariables()

    tlist = choiseVariant()

    process(tlist, tvars, output)

    print( "output writen to '%s'" % output )

def exit():
    print( "goodbye" )
    sys.exit()

def getOutputName():
    while True:
        try:
            output = input( "output file name [default:clickdoc.pdf]: " )
            if len(output) == 0:
                return "clickdoc.pdf"
            else:
                return "%s.pdf" % opath.splitext(output)[0]
        except EOFError: exit()
        except KeyboardInterrupt: exit()

def getVariables():

    tvars = {}
    for tv in tvars_list:
        try: tvars[tv] = input( "%s: " % tv )
        except EOFError: exit()
        except KeyboardInterrupt: exit()

    return tvars


def choiseVariant():

    tlvars = getListVariants( opath.join( programDir(), 'texfiles', 'listvars' ) )

    print( "choise variant: " )
    for (i,variant) in enumerate(tlvars):
        print( "[% 2d]: %s"%(i,variant[1]) )

    no = -1
    while no == -1:
        tv = input( "inter number: " )
        try:
            no = int(tv) 
        except ValueError:
            print( "[ERROR]: %s is no a number" % tv )
        except EOFError: exit()
        except KeyboardInterrupt: exit()

        maxnum = len(tlvars)-1
        if( no > maxnum ):
            print( "[ERROR]: %d is greater than max (%d)" % (no, maxnum) )
            no = -1
        elif( no < 0 ):
            print( "[ERROR]: %d is less than 0" % no )
            no = -1

    return tlvars[no][0]


def getListVariants(vpath):
    tvars = []
    for fname in os.listdir(vpath):
        if not fname.endswith('.tex'): continue
        with open( opath.join( vpath, fname ), "r") as f:
            tvars.append( ( opath.splitext(fname)[0], f.readline()[1:-1] ) )
    return tvars

def process(tlist,tvars,output):

    wdir = opath.join( programDir(), 'texfiles' )

    f = FileWriter( wdir )

    f.write( 'list.tex', generateList(tlist) )
    f.write( 'vars.tex', generateVars(tvars) )
    f.write( 'date.tex', generateDate() )

    buildAndCopyPDF( wdir, currentDir(), output )

def generateList(tlist):
    return "\\input{listvars/%s}"%tlist

def generateVars(tvars):
    ret = ""
    for v in tvars_list:
        ret += "\\def\\%s{%s}"%(v,tvars[v])
    return ret

def programDir(): return opath.dirname(opath.realpath(__file__))

def currentDir(): return os.path.abspath('.')

def generateDate():
    now = datetime.datetime.today()
    return "%d.%02d.%d"%(now.day,now.month,now.year)

def buildAndCopyPDF( wdir, odir, name ):
    os.chdir( wdir )
    sp.check_output( '/usr/bin/pdflatex --halt-on-error main.tex', shell=True )
    shutil.copyfile( opath.join(wdir,"main.pdf"), opath.join(odir,name) )

class FileWriter:

    def __init__(self,directory):
        self.directory = directory

    def write(self, filename, string):
        with open( opath.join( self.directory, filename ), "w") as f:
            f.write( string )

if __name__ == '__main__': main()
