import nose.tools
import yaml
import re

from victims_db_builder.library import BaseLibrary, JavaLibrary


# def test_multi_libraries():
#     data = yaml.load(file('tests/data/6504.yaml'))
#     libraries = data['affected']
#     loaded_libraries = []
#     for affectedLibrary in libraries:
#         version = affectedLibrary['version']
#         artifactId = affectedLibrary['artifactId']
#         groupId = affectedLibrary['groupId']
#         lib = JavaLibrary(version, groupId, artifactId)
#         assert len(lib.versions) >= 1
#         loaded_libraries.append(lib)
#     assert len(loaded_libraries) == 4

def testJettyShouldContainExpectedVersions():
    expectedVersions = ['9.2.4.v20141103', '9.2.5.v20141112', '9.2.6.v20141205', '9.2.7.v20150116']

    lib = JavaLibrary(['>=9.2.3,9.2', '<=9.2.8,9.2'], "org.eclipse.jetty", "jetty-http")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_matches(expectedVersions, lib)


def confirm_versions_does_not_exist(shouldNotBeInTheList, lib):
    if isinstance(shouldNotBeInTheList, list):
        for var in shouldNotBeInTheList:
            assert not any(val.version == var for val in lib.affectedMvnSeries)
    if isinstance(shouldNotBeInTheList, basestring):
        assert not any(var.version == shouldNotBeInTheList for var in lib.affectedMvnSeries)

def testJettyShouldNotContainVersion():
    shouldNotBeInTheList = '9.2.16.v20160414'
    lib = JavaLibrary(['>=9.2.3,9.2', '<=9.2.8,9.2'], "org.eclipse.jetty", "jetty-http")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_does_not_exist(shouldNotBeInTheList, lib)


def testSpringShouldContainExpectedVersions():
    expectedVersions = ['4.0.1.RELEASE', '4.0.8.RELEASE', '4.1.6.RELEASE', '4.0.7.RELEASE', '4.0.5.RELEASE',
                        '4.1.0.RELEASE',
                        '4.0.4.RELEASE', '4.1.1.RELEASE', '3.2.1.RELEASE', '4.1.3.RELEASE', '3.2.10.RELEASE',
                        '4.0.2.RELEASE',
                        '4.1.4.RELEASE', '4.0.3.RELEASE', '3.2.13.RELEASE', '4.0.9.RELEASE', '4.0.0.RELEASE',
                        '3.2.11.RELEASE',
                        '4.1.2.RELEASE', '4.1.5.RELEASE', '3.2.12.RELEASE', '3.2.0.RELEASE', '4.0.6.RELEASE']

    lib = JavaLibrary(['<=3.2.13,3.2', '<=4.1.6,4'], "org.springframework", "spring-web")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_matches(expectedVersions, lib)

def testSpringShouldNotContainVersions():
    shouldNotBeInTheList = ['3.2.14.RELEASE', '3.2.15.RELEASE', '3.2.16.RELEASE', '4.1.9.RELEASE', '4.1.7.RELEASE']
    lib = JavaLibrary(['<=3.2.13,3.2', '<=4.1.6,4'], "org.springframework", "spring-web")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_does_not_exist(shouldNotBeInTheList, lib)


def testStruts2ShouldContainVersions():
    expectedVersions = ['2.0.11.2', '2.1.2', '2.0.11.1', '2.0.11']
    lib = JavaLibrary(['<=2.0.11.2,2.0', '<=2.1.2,2.1'], "org.apache.struts", "struts2-core")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_matches(expectedVersions, lib)


def testStruts2ShouldNotContainVersions():
    shouldNotBeInTheList = ['2.0.12', '2.0.14', '2.1.6']
    lib = JavaLibrary(['<=2.0.11.2,2.0', '<=2.1.2,2.1'], "org.apache.struts", "struts2-core")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_does_not_exist(shouldNotBeInTheList, lib)


def testJbosswebShouldContainVersions():
    expectedVersions = ['7.0.16.Final-redhat-1', '7.3.2.Final-redhat-1', '7.5.15.Final-redhat-1',
                        '7.4.8.Final-redhat-4', '7.4.10.Final-redhat-1', '7.2.2.Final-redhat-4',
                        '7.3.1.Final-redhat-1', '7.0.17.Final-redhat-1', '7.5.11.Final-redhat-1',
                        '7.4.7.Final-redhat-1', '7.0.13.Final', '7.2.2.Final-redhat-1', '7.0.0.CR2',
                        '7.5.10.Final-redhat-1', '7.4.9.Final-redhat-1', '7.3.0.Final-redhat-1',
                        '7.2.0.Final-redhat-1', '7.5.12.Final-redhat-1']

    lib = JavaLibrary(['<=7.5.15,7'], "org.jboss.web", "jbossweb")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_matches(expectedVersions, lib)


def testJbosswebShouldNotContainVersions():
    shouldNotBeInTheList = '7.5.16.Final-redhat-1'
    lib = JavaLibrary(['<=7.5.15,7'], "org.jboss.web", "jbossweb")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_does_not_exist(shouldNotBeInTheList, lib)


def testGroovyallShouldContainVersions():
    expectedVersions = ['2.0.7', '2.0.6', '2.0.5', '2.0.4', '2.0.3', '2.0.2', '2.0.1', '2.0.0', '2.0.8', '2.1.8',
                        '2.1.9', '2.2.1', '2.2.0', '2.2.2', '2.1.2', '2.1.3', '2.1.0', '2.1.1', '2.1.6', '2.1.7',
                        '2.1.4', '2.1.5', '2.4.0-beta-2', '2.4.0-beta-3', '2.4.0-beta-1', '2.4.0-rc-2', '2.4.0-beta-4',
                        '2.2.0-beta-1', '2.2.0-beta-2', '2.0.0-beta-3', '2.3.8', '2.1.0-beta-1', '2.3.0', '2.3.1',
                        '2.3.2', '2.3.3', '2.3.4', '2.3.5', '2.3.6', '2.3.7', '2.0.0-rc-3', '2.3.10', '2.3.11',
                        '2.4.3', '2.4.2', '2.4.1', '2.4.0', '2.1.0-rc-1', '2.1.0-rc-2', '2.1.0-rc-3', '2.2.0-rc-1',
                        '2.2.0-rc-3', '2.2.0-rc-2', '2.0.0-beta-2', '2.4.0-rc-1', '2.0.0-beta-1', '2.3.0-beta-2',
                        '2.3.0-beta-1', '2.3.0-rc-2', '2.0.0-rc-2', '2.0.0-rc-1', '2.3.0-rc-1', '2.3.0-rc-4',
                        '2.0.0-rc-4', '2.3.9']

    lib = JavaLibrary(["<=2.4.3,2"], "org.codehaus.groovy", "groovy-all")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_matches(expectedVersions, lib)


def testGroovyallShouldContainVersionsWithDecimalPoint_1():
    expectedVersions = ['2.4.0-beta-2', '2.4.0-beta-3', '2.4.0-beta-1', '2.4.0-beta-4', '2.4.0-rc-1',
                        '2.4.3', '2.4.2', '2.4.1', '2.4.0', '2.4.0-rc-2']

    lib = JavaLibrary(["<=2.4.3,2.4"], "org.codehaus.groovy", "groovy-all")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_matches(expectedVersions, lib)


def testGroovyallShouldContainVersionsWithDecimalPoint_2():
    expectedVersions = ['2.3.0', '2.3.1', '2.3.2', '2.3.3', '2.3.0-beta-2', '2.3.0-beta-1',
                        '2.3.0-rc-2', '2.3.0-rc-1', '2.3.0-rc-4']

    lib = JavaLibrary(["<=2.3.3,2.3"], "org.codehaus.groovy", "groovy-all")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_matches(expectedVersions, lib)


def testGroovyallShouldNotContainVersions():
    shouldNotBeInTheList = ['2.4.11', '2.4.12']
    lib = JavaLibrary(["<=2.4.3,2.4"], "org.codehaus.groovy", "groovy-all")
    assert len(lib.affectedMvnSeries) != 0
    confirm_versions_does_not_exist(shouldNotBeInTheList, lib)


def confirm_versions_matches(expectedVersions, lib):
    for val in expectedVersions:
        assert any(var.version == val for var in lib.affectedMvnSeries)