#!/usr/bin/python

import sys
import subprocess

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
		
	print ('calling commitBuildVersionChanges')
	commitBuildVersionChanges(repoPath, 'Auto-increment version as part of finishing a release branch');
	
	return	
	
def incrementVersionPostRelease(currentVersion):
	versionParts = map(int, currentVersion.split("."))
	versionParts[1] += 1
	versionParts[2] = 0
	versionParts[3] = 0
	nextReleaseVersion = '{0}.{1}.{2}.{3}\n'.format(versionParts[0], versionParts[1], versionParts[2], versionParts[3])
	return nextReleaseVersion
	
def commitBuildVersionChanges(repoPath, commitMessage):
	
	print ('Stage')
	cmd = ['git', 'stage', '*']
	p = subprocess.Popen(cmd, cwd=repoPath)
	result = p.wait()
	
	print ('result: {0}').format(result)
	if result != 0:
		raise Exception('stage call failed')
	
	print ('Commit')
	cmd = ['git', 'commit', '-m', commitMessage]
	p = subprocess.Popen(cmd, cwd=repoPath)
	result = p.wait()
	
	print ('result: {0}').format(result)
	if result != 0:
		raise Exception('commit failed')
	
	print ('Push')
	cmd = ['git', 'push']
	p = subprocess.Popen(cmd, cwd=repoPath)
	result = p.wait()
	
	print ('result: {0}').format(result)
	if result != 0:
		raise Exception('push failed')
	
	
if __name__ == "__main__":
	main()
