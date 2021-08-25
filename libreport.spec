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
BuildRequires: sed json-c-devel gdb

Requires: libreport-filesystem = %{version}-%{release}
Requires: satyr >= 0.24
Requires: glib2 >= 2.43
Requires: xz
Requires: lz4
Requires: libreport = %{version}-%{release}
Requires: fros >= 1.0
Requires: curl

Provides:  %{name}-web = %{version}-%{release}
Obsoletes: %{name}-web < %{version}-%{release}

Provides:  %{name}-cli = %{version}-%{release}
Obsoletes: %{name}-cli < %{version}-%{release}

Provides:  report-newt = 0:0.23-1
Obsoletes: report-newt < 0:0.23-1

Provides:  %{name}-newt = %{version}-%{release}
Obsoletes: %{name}-newt < %{version}-%{release}

Provides: report-gtk = 0:0.23-1
Obsoletes: report-gtk < 0:0.23-1

Provides:  %{name}-gtk = %{version}-%{release}
Obsoletes: %{name}-gtk < %{version}-%{release}

Provides:  %{name}-plugin-kerneloops = %{version}-%{release}
Obsoletes: %{name}-plugin-kerneloops < %{version}-%{release}

Provides:  %{name}-plugin-logger = %{version}-%{release}
Obsoletes: %{name}-plugin-logger < %{version}-%{release}

Provides:  %{name}-plugin-systemd-journal = %{version}-%{release}
Obsoletes: %{name}-plugin-systemd-journal < %{version}-%{release}

Obsoletes: %{name}-plugin-ureport < %{version}-%{release}

Obsoletes: %{name}-plugin-bugzilla < %{version}-%{release}

Provides:  %{name}-plugin-mantisbt = %{version}-%{release}
Obsoletes: %{name}-plugin-mantisbt < %{version}-%{release}

Obsoletes: %{name}-plugin-rhtsupport < %{version}-%{release}

Provides:  %{name}-compat = %{version}-%{release}
Obsoletes: %{name}-compat < %{version}-%{release}

Provides:  %{name}-plugin-reportuploader = %{version}-%{release}
Obsoletes: %{name}-plugin-reportuploader < %{version}-%{release}

Provides:  %{name}-anaconda = %{version}-%{release}
Obsoletes: %{name}-anaconda < %{version}-%{release}

%if %{without python2_libreport}
Obsoletes: python2-libreport
%endif

%description
Generic library for reporting various problems to destinations like mailing lists, regular files, remote servers and bug tracking tools.
The library operates on problem data stored in the form of regular files in a directory (so called dump directory).
The library provides a low level API (dump_dir.h) for creating and modifying dump directories, a high level API allowing to avoid the need to work with dump directories (problem_data.h), and a set of tools that file reports.
The library also provides an infrastructure (run_event.h, report_event.conf) for automatic execution of shell scripts working with dump directories.

%package filesystem
Summary: Filesystem layout for libreport
BuildArch: noarch

%description filesystem
Filesystem layout for libreport

%package devel
Summary: Development libraries and headers for libreport
Requires: libreport = %{version}-%{release}

Provides:  %{name}-web-devel = %{version}-%{release}
Obsoletes: %{name}-web-devel < %{version}-%{release}

Provides:  %{name}-gtk-devel = %{version}-%{release}
Obsoletes: %{name}-gtk-devel < %{version}-%{release}

%description devel
Development libraries and headers for libreport

%if %{with python2_libreport}
%package -n python2-libreport
Summary:   Python2 bindings for report-libs
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

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
./autogen.sh

CFLAGS="%{optflags}"
%configure --enable-import-rhtsupport-cert  --enable-doxygen-docs --disable-silent-rules

%make_build

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
#web
%{_libdir}/libreport-web.so.*
#cli
%{_bindir}/report-cli
#newt
%{_bindir}/report-newt
#gtk
%{_bindir}/report-gtk
%{_libdir}/libreport-gtk.so.*
%config(noreplace) %{_sysconfdir}/libreport/events.d/emergencyanalysis_event.conf
%{_datadir}/%{name}/events/report_EmergencyAnalysis.xml

#plugin-kerneloops
%{_datadir}/%{name}/events/report_Kerneloops.xml
%{_bindir}/reporter-kerneloops

#plugin-logger
%config(noreplace) %{_sysconfdir}/libreport/events/report_Logger.conf
%{_datadir}/%{name}/events/report_Logger.xml
%{_datadir}/%{name}/workflows/workflow_Logger.xml
%{_datadir}/%{name}/workflows/workflow_LoggerCCpp.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/print_event.conf
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_logger.conf
%{_bindir}/reporter-print

#plugin-systemd-journal
%{_bindir}/reporter-systemd-journal

#plugin-mantisbt
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt.conf
%{_datadir}/%{name}/conf.d/plugins/mantisbt.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_format.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_formatdup.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_format_analyzer_libreport.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_formatdup_analyzer_libreport.conf
%{_bindir}/reporter-mantisbt

#compat
%{_bindir}/report

#plugin-reportuploader
%{_bindir}/reporter-upload
%{_datadir}/%{name}/events/report_Uploader.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/uploader_event.conf
%{_datadir}/%{name}/workflows/workflow_Upload.xml
%{_datadir}/%{name}/workflows/workflow_UploadCCpp.xml
%config(noreplace) %{_sysconfdir}/libreport/plugins/upload.conf
%{_datadir}/%{name}/conf.d/plugins/upload.conf
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_uploader.conf
%config(noreplace) %{_sysconfdir}/libreport/events/report_Uploader.conf


#anaconda
%{_datadir}/%{name}/workflows/workflow_AnacondaUpload.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/anaconda_event.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_anaconda_event.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_anaconda.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_formatdup_anaconda.conf

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
# Public api headers:
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
#web-devel
%{_libdir}/libreport-web.so
%{_includedir}/libreport/libreport_curl.h
%{_libdir}/pkgconfig/libreport-web.pc
#gtk-devel
%{_libdir}/libreport-gtk.so
%{_includedir}/libreport/internal_libreport_gtk.h
%{_libdir}/pkgconfig/libreport-gtk.pc

%if %{with python2_libreport}
%files -n python2-libreport
%{python2_sitearch}/report/
%{python2_sitearch}/reportclient/
%endif

%files -n python3-libreport
%{python3_sitearch}/report/
%{python3_sitearch}/reportclient/

%files help
%{_mandir}/man1/report-cli.1.gz
%{_mandir}/man1/report-newt.1.gz
%{_mandir}/man1/report-gtk.1.gz
%{_mandir}/man5/emergencyanalysis_event.conf.5.*
%{_mandir}/man*/reporter-kerneloops.*
%{_mandir}/man5/report_Logger.conf.5.*
%{_mandir}/man5/print_event.conf.5.*
%{_mandir}/man5/report_logger.conf.5.*
%{_mandir}/man*/reporter-print.*
%{_mandir}/man*/reporter-systemd-journal.*
%{_mandir}/man1/reporter-ureport.1.gz
%{_mandir}/man5/ureport.conf.5.gz
%{_mandir}/man1/reporter-mantisbt.1.gz
%{_mandir}/man5/mantisbt.conf.5.*
%{_mandir}/man5/mantisbt_format.conf.5.*
%{_mandir}/man5/mantisbt_formatdup.conf.5.*
%{_mandir}/man5/mantisbt_format_analyzer_libreport.conf.5.*
%{_mandir}/man5/mantisbt_formatdup_analyzer_libreport.conf.5.*
%{_mandir}/man1/reporter-rhtsupport.1.gz
%{_mandir}/man5/rhtsupport.conf.5.*
%{_mandir}/man5/rhtsupport_event.conf.5.*
%{_mandir}/man1/report.1.gz
%{_mandir}/man*/reporter-upload.*
%{_mandir}/man5/uploader_event.conf.5.*
%{_mandir}/man1/reporter-rhtsupport.1.gz
%{_mandir}/man5/rhtsupport.conf.5.*
%{_mandir}/man5/rhtsupport_event.conf.5.*
%{_mandir}/man5/anaconda_event.conf.5.*
%{_mandir}/man5/bugzilla_anaconda_event.conf.5.*
%{_mandir}/man5/bugzilla_format_anaconda.conf.5.*
%{_mandir}/man5/bugzilla_formatdup_anaconda.conf.5.*
%{_mandir}/man5/libreport.conf.5*
%{_mandir}/man5/report_event.conf.5*
%{_mandir}/man5/forbidden_words.conf.5*
%{_mandir}/man5/ignored_words.conf.5*
%{_mandir}/man1/reporter-bugzilla.1.gz
%{_mandir}/man5/report_Bugzilla.conf.5.*
%{_mandir}/man5/bugzilla_event.conf.5.*
%{_mandir}/man5/bugzilla.conf.5.*
%{_mandir}/man5/bugzilla_format.conf.5.*
%{_mandir}/man5/bugzilla_formatdup.conf.5.*
%{_mandir}/man5/bugzilla_format_analyzer_libreport.conf.5.*
%{_mandir}/man5/bugzilla_format_kernel.conf.5.*
%{_mandir}/man5/report_rhel.conf.5.*

%changelog
* Wed Aug 25 2021 panxiaohe <panxiaohe@huawei.com> - 2.10.1-10
- Split filesystem package and add version limit for some provides symbol

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
