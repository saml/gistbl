#!/usr/bin/python2

from BeautifulSoup import BeautifulSoup

import urllib2
import subprocess
import tempfile
import os
import sys
import re

GIST_ID=re.compile(r'.*/([a-z0-9]+)[^a-z0-9].*')

def get_gist_id(gist_url):
    m = GIST_ID.match(gist_url)
    return m.group(1)


class Gistbl(object):
    def __init__(self, repo_base, htdocs, gitcmd='git', curlcmd='curl'):
        self.repo_base = repo_base
        self.htdocs = htdocs
        self.gitcmd = gitcmd
        self.curlcmd = curlcmd

    def clone_or_merge_repo(self, repo_id):
        repo_dir = self.repo_dir(repo_id)
        if os.path.exists(repo_dir):
            return self.merge_repo(repo_dir)
        return self.clone_repo(repo_id)

    def repo_dir(self, repo_id):
        return os.path.join(repo_base, repo_id)

    def htdoc(self, repo_id):
        return os.path.join(self.htdocs, repo_id + '.html')

    def repo_url(self, repo_id):
        return 'https://gist.github.com/%s.git' % repo_id

    def page_url(self, repo_id):
        return 'https://gist.github.com/%s/' % repo_id

    def merge_repo(self, repo_dir):
        p = subprocess.Popen([self.gitcmd, 'pull', 'origin'], cwd=repo_dir)
        p.communicate()
        return p.returncode

    def clone_repo(self, repo_id):
        repo_url = self.repo_url(repo_id)
        p = subprocess.Popen([self.gitcmd, 'clone', repo_url], cwd=self.repo_base)
        p.communicate()
        return p.returncode

    def download(self, page_url):
        target_dir = tempfile.mkdtemp()
        target_path = os.path.join(target_dir, 'index.html')

        p = subprocess.Popen([self.curlcmd, '-s', '-o', target_path, page_url])
        p.communicate()
        
        return target_path

    def scrape(self, repo_id):
        page_url = self.page_url(repo_id)
        file_path = self.download(page_url)
        src_file = open(file_path, 'r')


        soup = BeautifulSoup(src_file)
        articles = soup('article')
        data = soup.findAll('div', attrs={'class': 'data'})
        
        htdoc = self.htdoc(repo_id)
        target_file = open(htdoc, 'w')
        for article in articles:
            target_file.write(unicode(article))
        for x in data:
            target_file.write(unicode(x))

        target_file.close()
        src_file.close()


def main(argv):
    gist_url = argv[1]
    repo_id = get_gist_id(gist_url)
    gist = Gistbl('.', '.')
    gist.scrape(repo_id)

if __name__ == '__main__':
    main(sys.argv)
