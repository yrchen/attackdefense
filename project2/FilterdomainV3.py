#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#The program will filiter the domain,which forward ip less than 4,then record it in the goodresult
#If the asn of ip are different ,then record it in the badresult
#Source file : list   Result file : result 

import os
import popen2

#NumberOfIP() check the number of ip which is forwarded by the domain
def NumberOfIP(domain):
	IPlist=[]
	domain = "".join(domain.split())
	for dns in [" "," 139.175.55.244"," 8.8.8.8"]:
		DataOut,DataIn = popen2.popen2("host -t A " + domain + dns)
		SeparateIP = DataOut.readlines()
		for i in range (len(SeparateIP)-1):
			temp = SeparateIP[i].split()
			if len(temp) > 0 :
				try :
					IP = temp[3]
					if IP not in "alias" :
						if IP not in IPlist :
							IPlist.append(IP)
				except:
					continue

	return len(IPlist)

#NumberOfIP() check the number of asn which is forwarded by the ip forwarded by the domain
def NumberOfAsn(domain):
	ASN = []
	domain = "".join(domain.split())
	for dns in [" "," 139.175.55.244"," 8.8.8.8"]:
		DataOut,DataIn = popen2.popen2("host -t A " + domain + dns)
		SeparateIP = DataOut.readlines()
		for i in range(len(SeparateIP) - 1):
			temp = SeparateIP[i].split()
			if len(temp) > 0 :
				try :
					IP = temp[3]
					ASNOut,IPIN = popen2.popen2("whois -h whois.cymru.com "+IP)		
					SeparateASN = (ASNOut.read()).split("\n")
					temp = SeparateASN[1].split()
					if temp[0] not in ASN :
						ASN.append(temp[0])
				except :
					continue
	return len(ASN)	

#TryCDN will check the domain whether belong to cdn.
def TryCDN(domain):
	CDN = ["akamai","cdn","akafms","amazon","google","adobe"]
	DataOut,DataIn = popen2.popen2("host -t NS " + domain)
	SeparateIP = (DataOut.read()).split(".")
	for i in CDN :
		if i in SeparateIP :
			return True
	return False

if __name__=='__main__':
	fileopengood = open('goodresult','w')
	fileopenbad = open('badresult','w')	
	for domain in open('list'):  
		if NumberOfIP(domain) > 4 :
			if not TryCDN(domain) and NumberOfAsn(domain) > 1 :
				fileopenbad.write(domain)
			else :
				fileopengood.write(domain)
				
	fileopengood.close()
	fileopenbad.close()
