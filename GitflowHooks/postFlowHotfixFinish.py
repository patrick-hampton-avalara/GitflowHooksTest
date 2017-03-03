#!/usr/bin/python

import sys
import subprocess

def main():
	#This script needs to be called with the path to the repose that is having it's release finished
	repoPath = sys.argv[1]
	
	
	
	
	versionFile = repoPath + '/BuildVersion/mylodge-version.txt'
	buildVersion = ''
	with open(versionFile, 'r') as buildVersionFile:
		buildVersion = buildVersionFile.readline().strip('\n')

	print ('Current build version: {0}'.format(buildVersion))
	nextVersion = incrementVersionPostRelease(buildVersion)
	print ('Build version incremented to: {0}'.format(nextVersion))

	with open(versionFile, 'w') as buildVersionFile:
		buildVersionFile.write(nextVersion)
	
	print ('Pushing version changes to the remote server')	
	commitAndPushBuildVersionChanges(repoPath, versionFile, 'Auto-increment version as part of finishing a release branch');
	print ('Build version changes have been pushed!')
	
	return	
	
def incrementVersionPostRelease(currentVersion):
	versionParts = map(int, currentVersion.split("."))
	versionParts[2] += 1
	versionParts[3] = 0
	nextReleaseVersion = '{0}.{1}.{2}.{3}\n'.format(versionParts[0], versionParts[1], versionParts[2], versionParts[3])
	return nextReleaseVersion
	
def commitAndPushBuildVersionChanges(repoPath, versionFile, commitMessage):
	
	print ('Version File: {0}').format(versionFile)
	print ('Staging modified files')
	cmd = ['git', 'add', versionFile]
	p = subprocess.Popen(cmd, cwd=repoPath, stdout=subprocess.PIPE)
	result = p.wait()
	print p.stdout.read();
	
	if result != 0:
		raise Exception('stage call failed')
	
	print ('Commiting staged changes')
	cmd = ['git', 'commit', '-m', commitMessage]
	p = subprocess.Popen(cmd, cwd=repoPath, stdout=subprocess.PIPE)
	result = p.wait()
	print p.stdout.read();
	
	if result != 0:
		raise Exception('commit failed')
	
	print ('Pushing to origin')
	cmd = ['git', 'push']
	p = subprocess.Popen(cmd, cwd=repoPath, stdout=subprocess.PIPE)
	result = p.wait()
	print p.stdout.read();
	
	if result != 0:
		raise Exception('push failed')
	
if __name__ == "__main__":
	main()
