#!/usr/bin/python

import sys
import subprocess

def main():
	print('Updating the Build Version file for the new hotfix branch')

	#This script needs to be called with the path to the repose that is having it hotfix started
	repoPath = sys.argv[1]
	
	versionFile = repoPath + '/BuildVersion/mylodge-version.txt'
	buildVersion = ''
	with open(versionFile, 'r') as buildVersionFile:
		buildVersion = buildVersionFile.readline().strip('\n')

	print ('-Current build version: {0}'.format(buildVersion))
	nextVersion = incrementVersionForHotfix(buildVersion)
	print ('-Build version incremented to: {0}'.format(nextVersion))

	with open(versionFile, 'w') as buildVersionFile:
		buildVersionFile.write(nextVersion)
	
	print ('-Comming version changes to local repo')		
	commitBuildVersionChanges(repoPath, versionFile, 'Auto-increment version as part of starting a hotfix branch');
	print ('-Build version changes have been commited')
	
	return	
	
def incrementVersionForHotfix(currentVersion):
	versionParts = map(int, currentVersion.split("."))
	versionParts[2] += 1
	versionParts[3] = 0
	nextReleaseVersion = '{0}.{1}.{2}.{3}\n'.format(versionParts[0], versionParts[1], versionParts[2], versionParts[3])
	return nextReleaseVersion
	
def commitBuildVersionChanges(repoPath, versionFile, commitMessage):
	print ('-Staging modified files')
	cmd = ['git', 'add', versionFile]
	p = subprocess.Popen(cmd, cwd=repoPath, stdout=subprocess.PIPE)
	result = p.wait()
	print p.stdout.read();
	
	if result != 0:
		raise Exception('stage call failed')
	
	print ('-Commiting staged changes')
	cmd = ['git', 'commit', '-m', commitMessage]
	p = subprocess.Popen(cmd, cwd=repoPath, stdout=subprocess.PIPE)
	result = p.wait()
	print p.stdout.read();
	
	if result != 0:
		raise Exception('commit failed')
	
	
if __name__ == "__main__":
	main()

