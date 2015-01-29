#!/usr/bin/env python
# pip install github3.py

import argparse
from github3 import login


def main(token, organization, username=None, verbose=False):
    gh = login(token=token)
    user = gh.user(username) if username else gh.me()
    org = gh.organization(organization)

    print u"User: {} ({})".format(user.name, user.login)
    print u"Organization: {}".format(organization)
    print u"RateLimit Remaining: {}".format(gh.ratelimit_remaining)
    print

    repos = [repo for repo in org.repositories()]
    repo_pulls = {repo: [pull for pull in repo.pull_requests()
                         if pull.assignee and pull.assignee == user]
                  for repo in repos}

    repo_format = u"{name}"
    pull_format = u"    {title}: {url}"
    if verbose:
        pull_format = (u"    {title}\n"
                       "\turl: {url}\n"
                       "\tupdated: {updated}")

    for repo, pulls in repo_pulls.iteritems():
        if len(pulls) == 0:
            continue

        repo_fmt_dict = {"name": repo.name,
                         "updated": repo.updated_at}
        print repo_format.format(**repo_fmt_dict)
        for pull in pulls:
            assignee = pull.assignee
            if not assignee or assignee != user:
                continue
            pull_fmt_dict = {"title": pull.title,
                             "assignee": pull.assignee or "",
                             "url": pull.html_url,
                             "updated": pull.updated_at}
            print pull_format.format(**pull_fmt_dict)

parser = argparse.ArgumentParser()
parser.add_argument("token")
parser.add_argument("organization")
parser.add_argument("-u", "--user",
                    dest="user",
                    default=None)
parser.add_argument("-v", "--verbose",
                    dest="verbose",
                    action="store_true")

if __name__ == "__main__":
    args = parser.parse_args()
    main(args.token, args.organization,
         username=args.user, verbose=args.verbose)
