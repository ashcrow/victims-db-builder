import yaml, httplib, string
import urllib
import urllib2

#COMMON_FIELDS = {
#    'cve': FieldValidator([is_string, is_cve]),
#    'title': FieldValidator([is_string]),
#    'description': FieldValidator([is_text], False),
#    'cvss_v2': FieldValidator([is_cvss_v2], False),
#    'references': FieldValidator([is_references], False),
#    'affected': FieldValidator([is_affected])
#}

#LANGUAGE_FIELDS = {
#    'python': {
#        'name': FieldValidator([is_string]),
#        'version': FieldValidator([is_version]),
#        'fixedin': FieldValidator([is_version], False),
#        'unaffected': FieldValidator([is_version], False),
#    },
#    'java': {
#        'groupId': FieldValidator([is_string]),
#        'artifactId': FieldValidator([is_string]),
#        'version': FieldValidator([is_version]),
#        'fixedin': FieldValidator([is_version], False),
#        'unaffected': FieldValidator([is_version], False),
#    }
#}

#VERSION_REGEX = regex_compile(
#    r'^(?P<condition>[><=]=)'
#    r'(?P<version>[^, ]+)'
#    r'(?:,(?P<series>[^, ]+)){0,1}$'
#)

##############################################################
## Vulnerability class
## Used for both parsing yaml file and building individual jar files
##############################################################

class Vulnerability:

    #This Base URL will only work for Java, need to add for Python and Ruby
    indexBaseUrl="http://mvnrepository.com/artifact/"


    ## upper range of z maintenance release in maven page
    maxRange = 99

    listVer = []
	
    def __init__(self, cve, title, description, cvss_v2, references, affected):
        self.cve = cve
	self.title = title
	self.description = description
	self.cvss_v2 = cvss_v2
	self.references = references
	self.affected = affected

    ## For loading in Yaml info
    def __init__(self,document):
	data = yaml.load(file(document))
        self.cve = data['cve']
        self.title = data['title']
        self.description = data['description']
        self.cvss_v2 = data['cvss_v2']
        self.references = data['references']
        self.affected = data['affected']
	#TODO this will only assign last artifact/group in affected list
        ##If there are mulitiple affected, need to create an affected list	
	for j in self.affected:
		self.groupId = j['groupId']
		self.artifactId = j['artifactId']
		self.verRanges = j['version']
        self.anchor = "/artifact/" + self.groupId + "/" + self.artifactId + "/"   
    
    ## Prints out basics
    def print_flaw(self):
	print "CVE= " + self.cve
        print "groupId= " + self.groupId
	print "artifactId= " + self.artifactId
	for r in self.verRanges:
        	self.genVersion(r)

    def genVersion(self, version):
	if version[0] == '>':
		genDown(self.splitRange(version[2:]))
	elif version[0] == '<':
		self.genUp(self.splitRange(version[2:]))
	else:
		pass

    #TODO test singe version and validate
    #		yield version[1:]

    def splitRange(self, numRange):
	return string.split(numRange, ',')

    def genUp(self, numRangeArray):
	toScale = numRangeArray[0].count('.')
	fromScale = numRangeArray[1].count('.')
	fromValue = numRangeArray[1]
	while fromScale < toScale:
		fromValue += '.0'
		fromScale = fromValue.count('.')
	numRangeArray[1] = fromValue
	print numRangeArray

    def genDown(numRangeArray):
        pass

    def genVerString(self, version):
        numRangeArray = self.splitRange(version[2:])
        toScale = numRangeArray[0].count('.')
        fromScale = numRangeArray[1].count('.')
        fromValue = numRangeArray[1]
        while fromScale < toScale:
    	    fromValue += '.0'
            fromScale = fromValue.count('.')
        numRangeArray[1] = fromValue
        return numRangeArray

    # Assumes string "4.0.2"
    # Returns list of [4.0,2] for looping as float
    def retlowHigh(self, string):
	valList = []
	k = string.rfind(".")
	valList.append(string[:k])
	valList.append(string[k+1:])
	return valList



    ## Opens Maven file for product, and checks through the version range to see whether
    ## it is listed as a release on the page
    ## Checks page for ex.: "/artifact/org.springframework/spring-web/4.0.9.RELEASE"
    ## Example range: <=3.2.13,3.2

    def checkMvnVer(self):
	#TODO This will not work for Python and Ruby
	coords = self.indexBaseUrl + self.groupId + "/" + self.artifactId
	try:
 		response = urllib2.urlopen(coords)
	except urllib2.URLError, e:
		if not hasattr(e, "code"):
			raise
		response = e
		print "Error with MavenPage:", response.code, response.msg
		return [] 

	HTMLPage = response.read()
	
	for r in self.verRanges:
		listString = self.genVerString(r)
		
		#split out values
		valList= self.retlowHigh(listString[1])
		lowDown = float(valList[0])
		lowUp = int(valList[1])
		valList= self.retlowHigh(listString[0])
		highDown = float(valList[0])
		highUp = int(valList[1])
		
        	ver = lowDown
        	while ver >= lowDown and ver <= highDown:
	                if (ver == lowDown and ver == highDown):
			  	for i in range (lowUp,highUp+1):	
					self.addVer(ver, i, HTMLPage)				
			elif (ver == lowDown):
				for i in range (lowUp, self.maxRange):
					self.addVer(ver, i, HTMLPage)					
			elif (ver == highDown):
				for i in range(highUp+1):
					self.addVer(ver, i, HTMLPage)				
			else:
				for i in range(self.maxRange):
					self.addVer(ver, i, HTMLPage)					
                	ver += 0.1
	return self.listVer 
	
    def addVer(self, ver, i, HTMLPage):
        tmpVers = str(ver) + "." + str(i)
	tmpAnchor = self.anchor + tmpVers 
	if tmpAnchor in HTMLPage:
            self.listVer.append(tmpVers)


##http://central.maven.org/maven2/org/springframework/spring-web/4.1.6.RELEASE/spring-web-4.1.6.RELEASE.jar
##############################################################
## Parse and build
##############################################################

jars = Vulnerability("../victims-cve-db/database/java/2015/3192.yaml")
jars.print_flaw()
listVers = jars.checkMvnVer() 
if listVers:
	print "Found releases in page:"
	for v in listVers:
		print v
