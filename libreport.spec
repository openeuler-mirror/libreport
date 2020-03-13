%define _unpackaged_files_terminate_build 0
%bcond_with python2_libreport

Name:    libreport
Version: 2.10.1
Release: 6
License: GPLv2+
Summary: Generic library for reporting various problems
URL:     https://abrt.readthedocs.org/
Source:  https://github.com/abrt/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

Patch9000: fix-bug-delete-gtk-deprecation-warnings.patch

BuildRequires: dbus-devel gtk3-devel curl-devel desktop-file-utils python2-devel python3-devel
BuildRequires: gettext libxml2-devel libtar-devel intltool libtool texinfo asciidoc xmlto
BuildRequires: newt-devel libproxy-devel satyr-devel >= 0.24 glib2-devel >= 2.43 git doxygen
BuildRequires: glibc-all-langpacks xmlrpc-c-devel systemd-devel augeas-devel augeas xz lz4
BuildRequires: sed json-c-devel

Requires: python-rhsm
Requires: python3-subscription-manager-rhsm
Requires: satyr >= 0.24
Requires: glib2 >= 2.43
Requires: xz
Requires: lz4
Requires: libreport = %{version}-%{release}
Requires: fros >= 1.0
Requires: curl

Provides:  %{name}-filesystem
Obsoletes: %{name}-filesystem

Provides:  %{name}-web
Obsoletes: %{name}-web

Provides:  %{name}-cli
Obsoletes: %{name}-cli

Provides:  report-newt = 0:0.23-1
Obsoletes: report-newt < 0:0.23-1

Provides:  %{name}-newt
Obsoletes: %{name}-newt

Provides: report-gtk = 0:0.23-1
Obsoletes: report-gtk < 0:0.23-1

Provides:  %{name}-gtk
Obsoletes: %{name}-gtk

Provides:  %{name}-plugin-kerneloops
Obsoletes: %{name}-plugin-kerneloops

Provides:  %{name}-plugin-logger
Obsoletes: %{name}-plugin-logger

Provides:  %{name}-plugin-systemd-journal
Obsoletes: %{name}-plugin-systemd-journal

Provides:  %{name}-plugin-ureport
Obsoletes: %{name}-plugin-ureport

Provides:  %{name}-plugin-bugzilla
Obsoletes: %{name}-plugin-bugzilla

Provides:  %{name}-plugin-mantisbt
Obsoletes: %{name}-plugin-mantisbt


Provides:  %{name}-plugin-rhtsupport
Obsoletes: %{name}-plugin-rhtsupport

Provides:  %{name}-compat
Obsoletes: %{name}-compat

Provides:  %{name}-plugin-reportuploader
Obsoletes: %{name}-plugin-reportuploader

Provides:  %{name}-anaconda
Obsoletes: %{name}-anaconda

%description
Generic library for reporting various problems to destinations like mailing lists, regular files, remote servers and bug tracking tools.
The library operates on problem data stored in the form of regular files in a directory (so called dump directory).
The library provides a low level API (dump_dir.h) for creating and modifying dump directories, a high level API allowing to avoid the need to work with dump directories (problem_data.h), and a set of tools that file reports.
The library also provides an infrastructure (run_event.h, report_event.conf) for automatic execution of shell scripts working with dump directories.

%package devel
Summary: Development libraries and headers for libreport
Requires: libreport = %{version}-%{release}

Provides:  %{name}-web-devel
Obsoletes: %{name}-web-devel

Provides:  %{name}-gtk-devel
Obsoletes: %{name}-gtk-devel

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

%package rhel
Summary: Default configuration for reporting bugs via Red Hat infrastructure
Requires: %{name} = %{version}-%{release}

%description rhel
Default configuration for reporting bugs via Red Hat infrastructure.
It is used to easily configure the reporting process for Red Hat systems.

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
make check|| {
    # find and print the logs of failed test
    # do not cat tests/testsuite.log because it contains a lot of bloat
    find tests/testsuite.dir -name "testsuite.log" -print -exec cat '{}' \;
    exit 1
}

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
#filesystem
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

#plugin-ureport
%config(noreplace) %{_sysconfdir}/libreport/plugins/ureport.conf
%{_datadir}/%{name}/conf.d/plugins/ureport.conf
%{_bindir}/reporter-ureport
%{_datadir}/%{name}/events/report_uReport.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.ureport.xml

#plugin-bugzilla
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla.conf
%{_datadir}/%{name}/conf.d/plugins/bugzilla.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_formatdup.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_analyzer_libreport.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_kernel.conf
%{_datadir}/%{name}/events/report_Bugzilla.xml
%{_datadir}/%{name}/events/watch_Bugzilla.xml
%config(noreplace) %{_sysconfdir}/libreport/events/report_Bugzilla.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_event.conf
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.bugzilla.xml
%{_bindir}/reporter-bugzilla

#plugin-mantisbt
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt.conf
%{_datadir}/%{name}/conf.d/plugins/mantisbt.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_format.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_formatdup.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_format_analyzer_libreport.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_formatdup_analyzer_libreport.conf
%{_bindir}/reporter-mantisbt

#plugin-rhtsupport
%config(noreplace) %{_sysconfdir}/libreport/plugins/rhtsupport.conf
%{_datadir}/%{name}/conf.d/plugins/rhtsupport.conf
%{_datadir}/%{name}/events/report_RHTSupport.xml
%{_datadir}/%{name}/events/report_RHTSupport_AddData.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.rhtsupport.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/rhtsupport_event.conf
%{_bindir}/reporter-rhtsupport

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

%files rhel
%{_datadir}/%{name}/workflows/workflow_RHELCCpp.xml
%{_datadir}/%{name}/workflows/workflow_RHELKerneloops.xml
%{_datadir}/%{name}/workflows/workflow_RHELPython.xml
%{_datadir}/%{name}/workflows/workflow_RHELvmcore.xml
%{_datadir}/%{name}/workflows/workflow_RHELxorg.xml
%{_datadir}/%{name}/workflows/workflow_RHELLibreport.xml
%{_datadir}/%{name}/workflows/workflow_RHELJava.xml
%{_datadir}/%{name}/workflows/workflow_RHELJavaScript.xml
%{_datadir}/%{name}/workflows/workflow_RHELAddDataCCpp.xml
%{_datadir}/%{name}/workflows/workflow_RHELAddDataJava.xml
%{_datadir}/%{name}/workflows/workflow_RHELAddDataKerneloops.xml
%{_datadir}/%{name}/workflows/workflow_RHELAddDataLibreport.xml
%{_datadir}/%{name}/workflows/workflow_RHELAddDataPython.xml
%{_datadir}/%{name}/workflows/workflow_RHELAddDatavmcore.xml
%{_datadir}/%{name}/workflows/workflow_RHELAddDataxorg.xml
%{_datadir}/%{name}/workflows/workflow_RHELAddDataJavaScript.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_rhel.conf
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_rhel_add_data.conf

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
