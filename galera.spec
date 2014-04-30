Name:           galera
Version:        25.3.5
Release:        5%{?dist}
Summary:        Synchronous multi-master wsrep provider (replication engine)

License:        GPLv2
URL:            http://www.codership.com/
Source0:        https://launchpad.net/%{name}/3.x/%{version}/+download/%{name}-%{version}-src.tar.gz
Source1:        garbd.service
Source2:        garbd-wrapper

Patch1:         galera-verify.patch

BuildRequires:  boost-devel check-devel openssl-devel scons systemd
Requires:       nmap-ncat

# comes from ./chromium/build_config.h
ExclusiveArch:  %{ix86} x86_64 %{arm}


Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description
Galera is a fast synchronous multi-master wsrep provider (replication engine)
for transactional databases and similar applications. For more information
about wsrep API see http://launchpad.net/wsrep. For a description of Galera
replication engine see http://www.codership.com.


%prep
%setup -q -n %{name}-%{version}-src

%patch1 -p1


%build
export CPPFLAGS="%{optflags}"
scons %{?_smp_mflags} strict_build_flags=0


%install
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/garbd.service
install -D -m 755 %{SOURCE2} %{buildroot}%{_sbindir}/garbd-wrapper
install -D -m 755 garb/garbd %{buildroot}%{_sbindir}/garbd
install -D -m 755 libgalera_smm.so %{buildroot}%{_libdir}/galera/libgalera_smm.so
install -D -m 644 garb/files/garb.cnf %{buildroot}%{_sysconfdir}/sysconfig/garb
install -D -m 644 COPYING %{buildroot}%{_docdir}/galera/COPYING
install -D -m 644 chromium/LICENSE %{buildroot}%{_docdir}/galera/LICENSE.chromium
install -D -m 644 asio/LICENSE_1_0.txt %{buildroot}%{_docdir}/galera/LICENSE.asio
install -D -m 644 www.evanjones.ca/LICENSE %{buildroot}%{_docdir}/galera/LICENSE.crc32
install -D -m 644 scripts/packages/README %{buildroot}%{_docdir}/galera/README
install -D -m 644 scripts/packages/README-MySQL %{buildroot}%{_docdir}/galera/README-MySQL


%post
/sbin/ldconfig
%systemd_post garbd.service


%preun
%systemd_preun garbd.service


%postun
/sbin/ldconfig
%systemd_postun_with_restart garbd.service


%files
%defattr(-,root,root,-)
%config(noreplace,missingok) %{_sysconfdir}/sysconfig/garb
%dir %{_docdir}/galera
%dir %{_libdir}/galera
%{_sbindir}/garbd
%{_sbindir}/garbd-wrapper
%{_unitdir}/garbd.service
%{_libdir}/galera/libgalera_smm.so
%doc %{_docdir}/galera/COPYING
%doc %{_docdir}/galera/LICENSE.asio
%doc %{_docdir}/galera/LICENSE.crc32
%doc %{_docdir}/galera/LICENSE.chromium
%doc %{_docdir}/galera/README
%doc %{_docdir}/galera/README-MySQL


%changelog
* Wed Apr 30 2014 Dan Horák <dan[at]danny.cz> - 25.3.5-5
- set ExclusiveArch

* Thu Apr 24 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.5-4
- Use strict_build_flags=0 to avoid -Werror
- Remove unnecessary %clean section

* Thu Apr 24 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.5-3
- Include galera directories in file list
- Set CPPFLAGS to optflags

* Wed Apr 23 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.5-2
- Fix client certificate verification (#1090604)

* Thu Mar 27 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.5-1
- Update to version 25.3.5

* Mon Mar 24 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.3-2
- Add systemd service

* Sun Mar 09 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.3-1
- Initial build
