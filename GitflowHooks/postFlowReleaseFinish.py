#!/usr/bin/python

import sys

def main():
	repoPath = sys.argv[1]
	versionFile = repoPath + '/BuildVersion/mylodge-version.txt'
	print 'versionFile: {0}'.format(versionFile)
	buildVersion = ''
	with open(versionFile, 'r') as buildVersionFile:
		buildVersion = buildVersionFile.readline().strip('\n')

	print ('Current build version: {0}'.format(buildVersion))
	nextVersion = incrementVersionPostRelease(buildVersion)
	print ('Build version incremented to: {0}'.format(nextVersion))

	with open(versionFile, 'w') as buildVersionFile:
		buildVersionFile.write(nextVersion)
	return	
	
def incrementVersionPostRelease(currentVersion):
	versionParts = map(int, currentVersion.split("."))
	versionParts[1] += 1
	versionParts[2] = 0
	versionParts[3] = 0
	nextReleaseVersion = '{0}.{1}.{2}.{3}\n'.format(versionParts[0], versionParts[1], versionParts[2], versionParts[3])
	return nextReleaseVersion

if __name__ == "__main__":
	main()
