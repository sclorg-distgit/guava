%{?scl:%scl_package guava}
%{!?scl:%global pkg_name %{name}}

Name:          %{?scl_prefix}guava
Version:       15.0
Release:       1.3%{?dist}
Summary:       Google Core Libraries for Java

Group:         Development/Libraries
License:       ASL 2.0 
URL:           http://code.google.com/p/guava-libraries
# git clone https://code.google.com/p/guava-libraries/
# (cd ./guava-libraries && git archive --format=tar --prefix=guava-%{version}/ v%{version}) | xz >guava-%{version}.tar.xz
Source0:       %{pkg_name}-%{version}.tar.xz
BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix_maven}maven-dependency-plugin

BuildRequires: java-devel >= 0:1.7.0
BuildRequires: %{?scl_prefix_maven}sonatype-oss-parent
BuildRequires: %{?scl_prefix_maven}jsr-305
%{?scl:BuildRequires:	  %{?scl_prefix}build}

BuildArch:     noarch
%{?scl:Requires: %scl_runtime}

%description
Guava is a suite of core and expanded libraries that include 
utility classes, Google's collections, io classes, and much 
much more.
This project is a complete packaging of all the Guava libraries
into a single jar.  Individual portions of Guava can be used
by downloading the appropriate module and its dependencies.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
find . -name '*.jar' -delete

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_disable_module guava-gwt
%pom_disable_module guava-testlib
%pom_disable_module guava-tests
%pom_remove_plugin :animal-sniffer-maven-plugin guava
%pom_remove_plugin :maven-gpg-plugin

%pom_xpath_inject /pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration/pom:instructions "<_nouses>true</_nouses>" guava/pom.xml
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_file :%{pkg_name} %{pkg_name}
%mvn_alias :%{pkg_name} "com.google.collections:google-collections"
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc AUTHORS CONTRIBUTORS COPYING README*

%files javadoc -f .mfiles-javadoc
%doc COPYING

%changelog
* Mon Feb 23 2015 Roland Grunberg <rgrunber@redhat.com> - 15.0-1.3
- Rebuilt to generate metadata.
- Related: rhbz#1175108.

* Mon Jun 02 2014 Roland Grunberg <rgrunber@redhat.com> - 15.0-1.2
- Do not generate uses directive for exports.

* Tue May 27 2014 Mat Booth <mat.booth@redhat.com> - 15.0-1.1
- SCL-isation for DTS3.

* Fri May 23 2014 Sami Wagiaalla <swagiaal@redhat.com> 15.0-1
- Import latest version from rawhide.

* Fri May 23 2014 Sami Wagiaalla <swagiaal@redhat.com> 13.0-5
- Build for DTS 3.

* Tue Apr 2 2013 Krzysztof Daniel <kdaniel@redhat.com> 13.0-4
- Import from RHEL 7 and SCLization.
- Removed javadoc.

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
