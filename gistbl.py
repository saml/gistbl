#!/usr/bin/python2

import HTMLParser

import subprocess
import tempfile
import os
import sys
import re

GIST_ID=re.compile(r'^.*/gist.github.com/([a-z0-9]+)[^a-z0-9]*.*$')

def get_gist_id(gist_url):
    m = GIST_ID.match(gist_url)
    if m:
        return m.group(1)
    return None


def to_starttag(tag, attrs):
    return '<%s %s>' % (tag, ' '.join(('%s="%s"' % (k,v) for k,v in attrs)))

def to_endtag(tag):
    return '</%s>' % tag

class GistScraper(HTMLParser.HTMLParser):

    def __init__(self, *args):
        HTMLParser.HTMLParser.__init__(self, *args)
        self.collect = None
        self.data = []


    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrd = dict(attrs)
        attr_class = attrd.get('class', '')
        if (not self.collect) and (tag == 'article' or attr_class.find('data') >= 0):
            self.collect = tag

        if self.collect:
            self.data.append(to_starttag(tag, attrs))

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.collect:
            self.data.append(to_endtag(tag))

        if tag == self.collect:
            self.collect = None

    def handle_data(self, data):
        if self.collect:
            self.data.append(data)

    def scrapped_data(self):
        return ''.join(self.data)


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
        return os.path.join(self.repo_base, repo_id)

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
        target_dir = tempfile.mkdtemp(prefix='gistbl-')
        target_path = os.path.join(target_dir, 'index.html')

        p = subprocess.Popen([self.curlcmd, '-s', '-o', target_path, page_url])
        p.communicate()
        
        return target_path

    def scrape(self, repo_id):
        page_url = self.page_url(repo_id)
        file_path = self.download(page_url)
        src_file = open(file_path, 'r')
        src_doc = src_file.read()
        src_file.close()


        print('opening: %s' % file_path)
        scraper = GistScraper()
        scraper.feed(src_doc)
        
        htdoc = self.htdoc(repo_id)
        target_file = open(htdoc, 'w')
        print('writing: %s' % htdoc)
        target_file.write(scraper.scrapped_data())

        target_file.close()


def main(argv):
    if len(argv) <= 1:
        print("Usage: %s gist-url [repo-base] [htdocs]" % argv[0])
        sys.exit(1)

    gist_url = argv[1]
    if len(argv) > 2:
        repo_base = argv[2]
    else:
        repo_base = os.path.abspath('.')
    if len(argv) > 3:
        htdocs = argv[3]
    else:
        htdocs = os.path.abspath('.')

    repo_id = get_gist_id(gist_url)
    if repo_id is None:
        print("invalid gist-url. cannot get gist id from the url")
        sys.exit(1)

    gist = Gistbl(repo_base, htdocs)
    gist.clone_or_merge_repo(repo_id)
    gist.scrape(repo_id)

if __name__ == '__main__':
    main(sys.argv)
