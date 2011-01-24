Summary:	Hard Disk Health Inspection Tool
Name:		gsmartcontrol
Version:	0.8.5
Release:	1%{?dist}

License:	GPLv3
Url:		http://gsmartcontrol.berlios.de
Group:		System Environment/Libraries
Source:		http://download.berlios.de/gsmartcontrol/%{name}-%{version}.tar.bz2
Source1:	gsmartcontrol.pam
Source2:	gsmartcontrol.consoleapp
Source3:	gsmartcontrol.desktop
Patch1:		gsmartcontrol-blacklist-dm.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libstdc++-devel
BuildRequires:	pcre-devel
BuildRequires:	gtkmm24-devel >= 2.6.0
BuildRequires:	libglademm24-devel >= 2.4.0

Requires:	smartmontools
Requires:	usermode-gtk


%description
GSmartControl is a graphical user interface for smartctl, which is a tool for
querying and controlling SMART (Self-Monitoring, Analysis, and Reporting
Technology) data in hard disk drives. It allows you to inspect the drive's
SMART data to determine its health, as well as run various tests on it.


%prep
%setup -q
%patch1 -p1


%build
%configure --enable-optimize-options=auto
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make DESTDIR=%buildroot install-strip

rm -f %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache
rm -rf %{buildroot}%{_datadir}/doc
rm -f %{buildroot}%{_bindir}/%{name}-root

install -dD %{buildroot}/%{_sysconfdir}/{pam.d,security/console.apps}
install -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/pam.d/%{name}
install -m644 %{SOURCE2} \
	%{buildroot}/%{_sysconfdir}/security/console.apps/%{name}

install -dD %{buildroot}/%{_sbindir}
mv %{buildroot}/%{_bindir}/* %{buildroot}/%{_sbindir}
ln -s consolehelper %{buildroot}%{_bindir}/%{name}


install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/applications


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :


%posttrans
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root)
%doc AUTHORS.txt COPYING ChangeLog INSTALL LICENSE* README.txt TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0755,root,root) %{_sbindir}/%{name}
%{_datadir}/gsmartcontrol/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/gsmartcontrol.png
%{_datadir}/pixmaps/gsmartcontrol.*
%{_mandir}/man1/gsmartcontrol*



%changelog
* Mon Jan 24 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.8.5-1
- initial build for Fedora
