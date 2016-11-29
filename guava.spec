%{?scl:%scl_package guava}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

Name:          %{?scl_prefix}guava
Version:       18.0
Release:       6.%{baserelease}%{?dist}
Summary:       Google Core Libraries for Java
License:       ASL 2.0
URL:           https://github.com/google/guava

Source0:       https://github.com/google/guava/archive/v%{version}.tar.gz
Patch0:        %{pkg_name}-java8.patch
Patch1:        guava-jdk8-HashMap-testfix.patch


BuildRequires: %{?scl_prefix_maven}maven-local

BuildRequires: %{?scl_prefix_maven}mvn(com.google.code.findbugs:jsr305) >= 0-0.6.20090319svn
BuildRequires: %{?scl_prefix_java_common}ant
BuildRequires: %{?scl_prefix_maven}apache-ivy
BuildRequires: %{?scl_prefix_java_common}easymock2
BuildRequires: %{?scl_prefix}mockito

BuildArch:     noarch

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{pkg_name}

%description
Guava is a suite of core and expanded libraries that include
utility classes, Google’s collections, io classes, and much
much more.
This project is a complete packaging of all the Guava libraries
into a single jar.  Individual portions of Guava can be used
by downloading the appropriate module and its dependencies.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -n %{pkg_name}-%{version} -q
%patch0 -p1
%patch1 -p1
find . -name '*.jar' -delete

%pom_disable_module guava-gwt
%pom_disable_module guava-testlib
%pom_disable_module guava-tests
%pom_remove_plugin -r :animal-sniffer-maven-plugin 
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_dep jdk:srczip guava
%pom_remove_dep :caliper guava-tests
%mvn_package :guava-parent guava
%mvn_package :guava-tests __noinstall

# javadoc generation fails due to strict doclint in JDK 1.8.0_45
%pom_remove_plugin -r :maven-javadoc-plugin

%pom_xpath_inject /pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration/pom:instructions "<_nouses>true</_nouses>" guava/pom.xml

# Avoid dep on findbugs at runtime
%pom_xpath_inject "pom:dependencies/pom:dependency" "<scope>provided</scope>" guava
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x

%mvn_file :%{pkg_name} %{pkg_name}
%mvn_alias :%{pkg_name} com.google.collections:google-collections com.google.guava:guava-jdk5
%mvn_build -s
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles-guava
%doc COPYING

%files javadoc -f .mfiles-javadoc
%doc COPYING

%changelog
* Sat Jul 23 2016 Mat Booth <mat.booth@redhat.com> - 18.0-6.2
- Disable building tests due to unavailable Google 'truth' library
- Avoid run-time dep on findbugs annotations
- Remove some problematic doc files causing "cpio: bad magic" on EL6

* Sat Jul 23 2016 Mat Booth <mat.booth@redhat.com> - 18.0-6.1
- Auto SCL-ise package for rh-eclipse46 collection

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 18.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 22 2015 Noa Resare <noa@resare.com> - 18.0-5
- enable module guava-testlib
- enable tests in guava-testlib
- backport fix to HashMap related test from 19.0-SNAPSHOT

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 18.0-3
- Remove maven-javadoc-plugin execution

* Fri Feb  6 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 18.0-2
- Update upstream website URL

* Wed Jan  7 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 18.0-1
- Update to v. 18 (#1175401)
- Use %license

* Wed Oct  8 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 17.0-2
- Add alias for com.google.guava:guava-jdk5

* Fri Jun 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 17.0-1
- Add patch for Java 8

* Tue Jun 17 2014 Roland Grunberg <rgrunber@redhat.com> - 15.0-4
- Do not generate uses directive for exports.

* Fri Jun 13 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 17.0-1
- Update to latest upstream version (#1109442).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 15.0-2
- Use Requires: java-headless rebuild (#1067528)

* Wed Jan  8 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 15.0-1
- Update to upstream version 15.0

* Mon Aug 12 2013 gil cattaneo <puntogil@libero.it> 13.0-6
- fix rhbz#992456
- update to current packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 13.0-4
- Replace BR on ant-nodeps with ant

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 13.0-4
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 13.0-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 13.0-1
- Update to upstream version 13.0
- Remove RPM bug workaround
- Convert patches to pom macros

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 gil cattaneo <puntogil@libero.it> 11.0.2-1
- Update to 11.0.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 09-1
- Update to 09
- Packaging fixes
- Build with maven

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 14 2010 Hui wang <huwang@redhat.com> - 05-4
- Patch pom

* Fri Jun 18 2010 Hui Wang <huwang@redhat.com> - 05-3
- Fixed jar name in install section
- Removed spaces in description

* Thu Jun 17 2010 Hui Wang <huwang@redhat.com> - 05-2
- Fixed summary
- Fixed description
- Fixed creating symlink insturctions
- add depmap

* Thu Jun 10 2010 Hui Wang <huwang@redhat.com> - 05-1
- Initial version of the package
