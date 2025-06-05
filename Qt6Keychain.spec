#
# Conditional build:
%bcond_with	tests	# test suite

Summary:	Qt API to store passwords and other secret data securely
Summary(pl.UTF-8):	API Qt do bezpiecznego przechowywania haseł i innych tajnych danych
Name:		Qt6Keychain
Version:	0.15.0
Release:	1
License:	Modified BSD License
Group:		Libraries
#Source0Download: https://github.com/frankosterfeld/qtkeychain/releases
Source0:	https://github.com/frankosterfeld/qtkeychain/archive/%{version}/qtkeychain-%{version}.tar.gz
# Source0-md5:	00b01588862ba1ed4e6cb81a959108c3
URL:		https://github.com/frankosterfeld/qtkeychain
BuildRequires:	Qt6Core-devel >= 6
BuildRequires:	Qt6DBus-devel >= 6
%{?with_tests:BuildRequires:	Qt6Test-devel >= 6}
BuildRequires:	cmake >= 3.16
BuildRequires:	libsecret-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	qt6-build >= 6
BuildRequires:	qt6-linguist >= 6
BuildRequires:	qt6-qmake >= 6
BuildRequires:	rpmbuild(find_lang) >= 1.37
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt6Keychain a Qt API to store passwords and other secret data
securely.

How the data is stored depends on the platform:
- Mac OS X: Passwords are stored in the OS X Keychain.
- Linux/Unix: If running, GNOME Keyring is used, otherwise qtkeychain
  tries to use KWallet (via D-Bus), if available.
- Windows: Windows does not provide a service for secure storage.
  Qt6Keychain uses the Windows API function

%description -l pl.UTF-8
API Qt do bezpiecznego przechowywania haseł i innych tajnych danych.

Sposób przechowywania danych zależy od platformy:
- Mac OS X: hasła są przechowywanie poprzez usługę OS X Keychain
- Linux/Unix: używany jest GNOME Keyring jeśli jest uruchomiony, w
  przeciwnym wypadku używany jest KWallet (przez DBus), o ile jest
  dostępny
- Windows: system nie udostępnia usługi do bezpiecznego przechowywania
  danych; Qt6Keychain używa funkcji Windows API

%package devel
Summary:	Development files for Qt6Keychain
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Qt6Keychain
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= 6

%description devel
This package contains the header files for developing applications
that use Qt6Keychain.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę Qt6Keychain.

%prep
%setup -q -n qtkeychain-%{version}

%build
%cmake -B build-qt6 \
	%{!?with_tests:-DBUILD_TESTING:BOOL=OFF} \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DECM_MKSPECS_INSTALL_DIR=%{_libdir}/qt6/mkspecs/modules
%{__make} -C build-qt6

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-qt6 install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang qtkeychain --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f qtkeychain.lang
%defattr(644,root,root,755)
%doc COPYING ChangeLog
%attr(755,root,root) %{_libdir}/libqt6keychain.so.*.*
%ghost %{_libdir}/libqt6keychain.so.1
%dir %{_datadir}/qt6keychain
%dir %{_datadir}/qt6keychain/translations

%files devel
%defattr(644,root,root,755)
%{_includedir}/qt6keychain
%{_libdir}/cmake/Qt6Keychain
%{_libdir}/libqt6keychain.so
%{_libdir}/qt6/mkspecs/modules/qt_Qt6Keychain.pri
