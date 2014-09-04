#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import datetime

import subprocess as sp
import os
import os.path as opath
import shutil

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
    docvars = [ 'advtheme', 'keywords', 'website', 'ordernums' ]
    ret = ""
    for v in docvars:
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

#if __name__ == '__main__': main()
process('slot_machine', {'advtheme':'ЪЙ', 'keywords':'one two', 'website':'www.leningrad.ru', 'ordernums':'666 666'}, 'test.pdf')

