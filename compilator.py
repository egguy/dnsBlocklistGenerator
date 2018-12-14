# encoding: utf-8

from sys import argv
import re
import os
import errno

ipv4_re = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

print(argv)
blocklists = argv[1:]


top1 = set()
with open('top-1m.csv') as top1_fd:
    for l in top1_fd:
        _, domain = l.strip().split(",")
        top1.add(domain) 

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

mkdir_p("output")
mkdir_p("output/rpz")
mkdir_p("output/unbound")


with open('output/rpz/recursorconf.lua', 'w+') as fd:
    for i in blocklists:
        fd.write('rpzFile("%s.rpz", {policyName="%s"})\n' % (i, i,))



for i in blocklists:
    all_domains = set()
    top1_domains = set()
    with open("blacklist/dest/%s/domains" % (i,), "r") as src:
        for line in src:
            line = line.strip()
            if ipv4_re.match(line):
                print("Skip: %s" % (line, ))
                continue
            if line.startswith('http://') or line.startswith('https://'):
                print("Skip URL: %s" % (line, ))
                continue
            if line:
                all_domains.add(line)
                if line in top1:
                    top1_domains.add(line)
    print "%s all: %s top1: %s" % (i, len(all_domains), len(top1_domains))
    # improve de diffs
    all_domains = sorted(all_domains)
    top1_domains = sorted(top1_domains)

    rpz_fd = open("output/rpz/%s.rpz" % (i,), "w+")
    unbound_fd = open("output/unbound/%s.conf" % (i,), "w+")

    rpz_fd.write("""
$TTL 5m;
$ORIGIN %s.block.com.
@          SOA powerdns.block.net. hostmaster.block.com ( 1 12h 15m 3w 2h)
           NS block.net.
; begin RPZ RR definitions

""" % (i,))

    for domain in all_domains:
        rpz_fd.write("%s CNAME .\n" % (domain,))
        rpz_fd.write("*.%s CNAME .\n" % (domain,))
        unbound_fd.write('local-zone: "%s" static\n' % (domain,))

    rpz_fd.close()
    unbound_fd.close()

    rpz_fd = open("output/rpz/%s.top1.rpz" % (i,), "w+")
    unbound_fd = open("output/unbound/%s.conf" % (i,), "w+")

    rpz_fd.write("""
$TTL 5m;
$ORIGIN %s.block.com.
@          SOA powerdns.block.net. hostmaster.block.com ( 1 12h 15m 3w 2h)
           NS block.net.
; begin RPZ RR definitions

""" % (i,))

    for domain in top1_domains:
        rpz_fd.write("%s CNAME .\n" % (domain,))
        rpz_fd.write("*.%s CNAME .\n" % (domain,))
        unbound_fd.write('local-zone: "%s" static\n' % (domain,))

    rpz_fd.close()
    unbound_fd.close()
