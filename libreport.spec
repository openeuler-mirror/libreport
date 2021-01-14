%define _unpackaged_files_terminate_build 0
%bcond_with python2_libreport

Name:    libreport
Version: 2.10.1
Release: 10
License: GPLv2+
Summary: Generic library for reporting various problems
URL:     https://abrt.readthedocs.org/
Source:  https://github.com/abrt/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

Patch9000: fix-bug-delete-gtk-deprecation-warnings.patch

BuildRequires: dbus-devel gtk3-devel curl-devel desktop-file-utils python2-devel python3-devel
BuildRequires: gettext libxml2-devel libtar-devel intltool libtool texinfo asciidoc xmlto
BuildRequires: newt-devel libproxy-devel satyr-devel >= 0.24 glib2-devel >= 2.43 git doxygen
BuildRequires: glibc-all-langpacks xmlrpc-c-devel systemd-devel augeas-devel augeas xz lz4
BuildRequires: json-c-devel gdb

Requires: satyr >= 0.24 glib2 >= 2.43 xz lz4

Obsoletes: %{name}-plugin-bugzilla %{name}-plugin-mantisbt %{name}-plugin-ureport %{name}-plugin-rhtsupport %{name}-rhel

%if %{without python2_libreport}  
Obsoletes: python2-libreport    
%endif       

%description
Libraries providing API for reporting different problems in applications
to different bug targets like Bugzilla, ftp, trac, etc...

%package filesystem
Summary: Filesystem layout for libreport
BuildArch: noarch

%description filesystem
Filesystem layout for libreport

%package devel
Summary: Development libraries and headers for libreport
Requires: libreport = %{version}-%{release}



%description devel
Development libraries and headers for libreport

%package web
Summary: Library providing network API for libreport
Requires: libreport = %{version}-%{release}

%description web
Library providing network API for libreport

%package web-devel
Summary: Development headers for libreport-web
Requires: libreport-web = %{version}-%{release}

%description web-devel
Development headers for libreport-web



%if %{with python2_libreport}
%package -n python2-libreport
Summary:   Python bindings for report-libs
Requires:  libreport = %{version}-%{release}
Requires:  python2-dnf
Provides:  %{name}-python = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}

%description -n python2-libreport
Python bindings for report-libs.
%endif

%package -n python3-libreport
Summary:   Python3 bindings for report-libs
Requires:  libreport = %{version}-%{release}
Requires:  python3-dnf
Provides:  %{name}-python3 = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}

%description -n python3-libreport
Python 3 bindings for report-libs.

%package cli
Summary:  libreport's command line interface
Requires: %{name} = %{version}-%{release}

%description cli
This package contains simple command line tool for working
with problem dump reports

%package newt
Summary:  libreport's newt interface
Requires: %{name} = %{version}-%{release}
Provides: report-newt = 0:0.23-1
Obsoletes: report-newt < 0:0.23-1

%description newt
This package contains a simple newt application for reporting
bugs

%package gtk
Summary: GTK front-end for libreport
Requires: libreport = %{version}-%{release}
Requires: libreport-plugin-reportuploader = %{version}-%{release}
Requires: fros >= 1.0
Provides: report-gtk = 0:0.23-1
Obsoletes: report-gtk < 0:0.23-1

%description gtk
Applications for reporting bugs using libreport backend

%package gtk-devel
Summary: Development libraries and headers for libreport
Requires: libreport-gtk = %{version}-%{release}

%description gtk-devel
Development libraries and headers for libreport-gtk

%package plugin-kerneloops
Summary: %{name}'s kerneloops reporter plugin
Requires: curl
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}

%description plugin-kerneloops
This package contains plugin which sends kernel crash information to specified
server, usually to kerneloops.org.

%package plugin-logger
Summary: %{name}'s logger reporter plugin
Requires: %{name} = %{version}-%{release}

%description plugin-logger
The simple reporter plugin which writes a report to a specified file.

%package plugin-systemd-journal
Summary: %{name}'s systemd journal reporter plugin
Requires: %{name} = %{version}-%{release}

%description plugin-systemd-journal
The simple reporter plugin which writes a report to the systemd journal.

%package compat
Summary: %{name}'s compat layer for obsoleted 'report' package
Requires: libreport = %{version}-%{release}

%description compat
Provides 'report' command-line tool.

%package plugin-reportuploader
Summary: %{name}'s reportuploader plugin
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}

%description plugin-reportuploader
Plugin to report bugs into anonymous FTP site associated with ticketing system.

%package anaconda
Summary: Default configuration for reporting anaconda bugs
Requires: %{name} = %{version}-%{release}
Requires: libreport-plugin-reportuploader = %{version}-%{release}

%description anaconda
Default configuration for reporting Anaconda problems or uploading the gathered
data over ftp/scp...


%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
./autogen.sh

CFLAGS="%{optflags}"
%configure --enable-doxygen-docs --disable-silent-rules

rm -rf  po/.intltool-merge-cache*
rm -rf  src/plugins/*.xml
rm -rf  src/workflows/*.xml

make

%install
%make_install

%find_lang %{name}

find %{buildroot} -name "*.py[co]" -delete

find %{buildroot} -name '*.la' -or -name '*.a' | xargs rm -f
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/events.d/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/events/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/workflows.d/
mkdir -p %{buildroot}/%{_datadir}/%{name}/events/
mkdir -p %{buildroot}/%{_datadir}/%{name}/workflows/

rm -f %{buildroot}/%{_infodir}/dir

%check
#make check|| {
    # find and print the logs of failed test
    # do not cat tests/testsuite.log because it contains a lot of bloat
    # find tests/testsuite.dir -name "testsuite.log" -print -exec cat '{}' \;
    # exit 1
# }

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc README.md
%license COPYING
%config(noreplace) %{_sysconfdir}/%{name}/libreport.conf
%config(noreplace) %{_sysconfdir}/%{name}/report_event.conf
%config(noreplace) %{_sysconfdir}/%{name}/forbidden_words.conf
%config(noreplace) %{_sysconfdir}/%{name}/ignored_words.conf
%{_datadir}/%{name}/conf.d/libreport.conf
%{_libdir}/libreport.so.*
%{_libdir}/libabrt_dbus.so.*
%{_datadir}/augeas/lenses/libreport.aug
%files filesystem
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/events.d/
%dir %{_sysconfdir}/%{name}/events/
%dir %{_sysconfdir}/%{name}/workflows.d/
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/conf.d/
%dir %{_datadir}/%{name}/conf.d/plugins/
%dir %{_datadir}/%{name}/events/
%dir %{_datadir}/%{name}/workflows/
%dir %{_sysconfdir}/%{name}/plugins/


%files devel

%doc apidoc/html/*.{html,png,css,js}
%{_includedir}/libreport/libreport_types.h
%{_includedir}/libreport/client.h
%{_includedir}/libreport/dump_dir.h
%{_includedir}/libreport/event_config.h
%{_includedir}/libreport/problem_data.h
%{_includedir}/libreport/problem_report.h
%{_includedir}/libreport/report.h
%{_includedir}/libreport/run_event.h
%{_includedir}/libreport/file_obj.h
%{_includedir}/libreport/config_item_info.h
%{_includedir}/libreport/workflow.h
%{_includedir}/libreport/problem_details_widget.h
%{_includedir}/libreport/problem_details_dialog.h
%{_includedir}/libreport/problem_utils.h
%{_includedir}/libreport/report_result.h
%{_includedir}/libreport/ureport.h
%{_includedir}/libreport/reporters.h
%{_includedir}/libreport/global_configuration.h
%{_includedir}/libreport/internal_abrt_dbus.h
%{_includedir}/libreport/internal_libreport.h
%{_includedir}/libreport/xml_parser.h
%{_includedir}/libreport/helpers
%{_libdir}/libreport.so
%{_libdir}/libabrt_dbus.so
%{_libdir}/pkgconfig/libreport.pc
%dir %{_includedir}/libreport

%files web
%{_libdir}/libreport-web.so.*

%files web-devel
%{_libdir}/libreport-web.so
%{_includedir}/libreport/libreport_curl.h
%{_libdir}/pkgconfig/libreport-web.pc


%if %{with python2_libreport}
%files -n python2-libreport
%{python2_sitearch}/report/
%{python2_sitearch}/reportclient/
%endif

%files -n python3-libreport
%{python3_sitearch}/report/
%{python3_sitearch}/reportclient/

%files cli
%{_bindir}/report-cli

%files newt
%{_bindir}/report-newt

%files gtk
%{_bindir}/report-gtk
%{_libdir}/libreport-gtk.so.*
%config(noreplace) %{_sysconfdir}/libreport/events.d/emergencyanalysis_event.conf
%{_datadir}/%{name}/events/report_EmergencyAnalysis.xml

%files gtk-devel
%{_libdir}/libreport-gtk.so
%{_includedir}/libreport/internal_libreport_gtk.h
%{_libdir}/pkgconfig/libreport-gtk.pc

%files plugin-kerneloops
%{_datadir}/%{name}/events/report_Kerneloops.xml
%{_bindir}/reporter-kerneloops

%files plugin-logger
%config(noreplace) %{_sysconfdir}/libreport/events/report_Logger.conf
%{_datadir}/%{name}/events/report_Logger.xml
%{_datadir}/%{name}/workflows/workflow_Logger.xml
%{_datadir}/%{name}/workflows/workflow_LoggerCCpp.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/print_event.conf
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_logger.conf
%{_bindir}/reporter-print

%files plugin-systemd-journal
%{_bindir}/reporter-systemd-journal


%files compat
%{_bindir}/report

%files plugin-reportuploader
%{_bindir}/reporter-upload
%{_datadir}/%{name}/events/report_Uploader.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/uploader_event.conf
%{_datadir}/%{name}/workflows/workflow_Upload.xml
%{_datadir}/%{name}/workflows/workflow_UploadCCpp.xml
%config(noreplace) %{_sysconfdir}/libreport/plugins/upload.conf
%{_datadir}/%{name}/conf.d/plugins/upload.conf
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_uploader.conf
%config(noreplace) %{_sysconfdir}/libreport/events/report_Uploader.conf

%files anaconda
%{_datadir}/%{name}/workflows/workflow_AnacondaRHEL.xml
%{_datadir}/%{name}/workflows/workflow_AnacondaUpload.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/anaconda_event.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_anaconda_event.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_anaconda.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_formatdup_anaconda.conf

%files help
%{_mandir}/man5/libreport.conf.5*
%{_mandir}/man5/report_event.conf.5*
%{_mandir}/man5/forbidden_words.conf.5*
%{_mandir}/man5/ignored_words.conf.5*
%{_mandir}/man1/report-cli.1.gz
%{_mandir}/man1/report-newt.1.gz
%{_mandir}/man1/report-gtk.1.gz
%{_mandir}/man5/emergencyanalysis_event.conf.5.*
%{_mandir}/man*/reporter-kerneloops.*
%{_mandir}/man5/print_event.conf.5.*
%{_mandir}/man5/report_logger.conf.5.*
%{_mandir}/man*/reporter-print.*
%{_mandir}/man5/report_Logger.conf.5.*
%{_mandir}/man*/reporter-systemd-journal.*
%{_mandir}/man1/report.1.gz
%{_mandir}/man*/reporter-upload.*
%{_mandir}/man5/uploader_event.conf.5.*
%{_mandir}/man5/upload.conf.5.*
%{_mandir}/man5/report_uploader.conf.5.*
%{_mandir}/man5/report_Uploader.conf.5.*
%{_mandir}/man5/anaconda_event.conf.5.*


%changelog
* Thu Jan 14 2021 wangjie<wangjie294@huawei.com> - 2.10.1-10
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:split sub-package
       cut reporter-mantisbt support

* Tue Aug 18 2020 wenzhanli<wenzhanli2@huawei.com> - 2.10.1-9
- add release version for update

* Mon Mar 30 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.10.1-8
- remove useless functions

* Sat Mar 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.10.1-7
- add necessary BuildRequires

* Thu Mar 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.10.1-6
- Remove some default installation packages

* Mon Jan 13 2020 chengquan <chengquan3@huawei.com> - 2.10.1-5
- fix bug in new glibc version

* Tue Dec 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.10.1-4
- Update tar package

* Sat Nov 23 2019 fangyufa<fangyufa1@huawei.com> - 2.10.1-3
- add rhel package

* Tue Nov 19 2019 fangyufa<fangyufa1@huawei.com> - 2.10.1-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:reinclude report_result.h in devel package

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.10.1-1
- Package init
