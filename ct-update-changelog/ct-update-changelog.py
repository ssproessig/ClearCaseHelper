#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Original autor: Sören Sprößig <ssproessig@googlemail.com>
#
from optparse import OptionParser

import sys
import re
import subprocess

import platform

class UpdateInfo:
	def __init__(self, reResult):
		self.relFullPath = reResult.group(1).strip().split("\n")[0]
		self.mainFrom = int(reResult.group(2))
		self.mainTo = int(reResult.group(3))
		self.mainPos = self.mainFrom
	
	def getNextCtParameters(self):
		if self.mainPos == self.mainTo:
			return None
		self.mainPos = self.mainPos + 1
		return self

class ClearToolUpdateChangeLog:
	def parseArgs(self, args):
		parser = OptionParser()
		parser.add_option("-u", "--updt", dest="updt", help="The update result file to parser.")
		parser.add_option("-f", "--format", dest="format", help="The format the load rule is given (use 'Windows' for \main\X, or 'Linux' for /main/X.")

		(self.options, args) = parser.parse_args(args)
				
		if self.options.format is None:
			self.options.format = platform.system()
		if self.options.format not in ('Windows', 'Linux'):
			self.options.format = None
		if self.options.format is None:
			print("Can not determine the load rule format to use. Please specifiy one with -f")
			sys.exit(1)
		if self.options.format == "Windows":
			self.loadRuleFormat = "\\\\main\\\\"
		if self.options.format == "Linux":
			self.loadRuleFormat = "/main/"

		if self.options.updt is None:
			print("You must provide a .updt file (result of 'cleartool update')! See help with -h for more information.")
			sys.exit(1)
	
	def readFile(self, filename):
		lines = list()
		# open the file
		self.file = open(filename)
		# read line by line
		for line in self.file:
			# skip comments
			if line[0] == "#":
				continue
			if line.startswith("Updated: "):
				lines.append(line)
		#
		return lines
	
	def parseLines(self, lines):
		# prepare the result
		updateInformation = list()
		# parse all lines
		for line in lines:
			m = re.search('Updated:[ ]+(.*)' + self.loadRuleFormat + '(\d+) ' + self.loadRuleFormat + '(\d+)', line)
			if (m == None):
				continue
			entry = UpdateInfo(m)
			updateInformation.append(entry)
		# return the result
		return updateInformation
	
	def collectDataFromClearTool(self, allUpdateInfo):
		print("Collecting update information for '%s'..." % self.options.updt)
		for info in allUpdateInfo:
			clParam = info.getNextCtParameters()
			print("\n[%s]" % (clParam.relFullPath))
			while (clParam):
				cmd = 'cleartool describe -fmt "%%u: %%c" %s@@/main/%d' % (clParam.relFullPath, clParam.mainPos)
				p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)
				out, err = p.communicate()				
				print("%d->%d: %s" % (clParam.mainPos-1, clParam.mainPos, out.strip()))
				clParam = info.getNextCtParameters()
		return

	def main(self, args):
		# parse the command line arguments
		self.parseArgs(args)
		# read the file
		self.lines = self.readFile(self.options.updt)
		# parse the lines
		self.updateInformation = self.parseLines(self.lines)
		# run cleartool
		self.collectDataFromClearTool(self.updateInformation)
		return 0

if __name__ == '__main__':
	sdmu = ClearToolUpdateChangeLog()
	sys.exit (sdmu.main (sys.argv))

