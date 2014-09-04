#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import datetime

import subprocess as sp
import os
import os.path as opath
import shutil

def main():

    #args = parseArguments()

    name = 'test.pdf'

    wdir = opath.join( programDir(), 'texfiles' )

    f = FileWriter( wdir )

#    f.wirte( 'variant.tex', choiseVariant(args.variant) )
    f.write( 'date.tex', generateDate() )

    buildAndCopyPDF( wdir, currentDir(), name )

#def parseArguments():
#    ap = argparse.ArgumentParser()
#    ap.add_argument(  )
# ap.add_argument( "filename", help="input file name" )
# ap.add_argument( "-s", "--skipfirst", dest="skipfirst", metavar="N", default=10, help="skip first N lines" )
# ap.add_argument( "-d", "--delimiter", dest="delimiter", metavar="CHAR", default=',', help="csv delimiter" )
# ap.add_argument( "-q", "--quotechar", dest="quotechar", metavar="CHAR", default='"', help="csv quotechar" )
# return ap.parse_args()

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
