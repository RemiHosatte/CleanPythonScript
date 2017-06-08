from bluepy.btle import Scanner
print "Scan ..."
scanner = Scanner(0)
devices = scanner.scan(3)
for d in devices:
    print str(d.addr) + " - " + str(d.addrType)

print "Done"
