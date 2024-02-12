#
%define		kfname	qtkeychain
Summary:	Qt API to store passwords and other secret data securely
Summary(pl.UTF-8):	API Qt do bezpiecznego przechowywania haseł i innych tajnych danych
Name:		Qt6Keychain
Version:	0.14.2
Release:	1
License:	Modified BSD License
Group:		Libraries
#Source0Download: https://github.com/frankosterfeld/qtkeychain/releases
Source0:	https://github.com/frankosterfeld/qtkeychain/archive/refs/tags/%{version}.tar.gz
# Source0-md5:	7f75753541784068400d903e0e7a0d55
URL:		https://github.com/frankosterfeld/qtkeychain
BuildRequires:	Qt6Core-devel >= 5
BuildRequires:	Qt6DBus-devel >= 5
BuildRequires:	cmake >= 2.8.11
BuildRequires:	libsecret-devel
BuildRequires:	libstdc++-devel
BuildRequires:	qt6-build >= 5
BuildRequires:	qt6-linguist >= 5
BuildRequires:	qt6-qmake >= 5
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

%description devel
This package contains the header files for developing applications
that use Qt6Keychain.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę Qt6Keychain.

%prep
%setup -q -n qtkeychain-%{version}

%build
install -d build-qt6
cd build-qt6
%cmake .. \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DECM_MKSPECS_INSTALL_DIR=%{_libdir}/qt6/mkspecs/modules
%{__make}

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

%files devel
%defattr(644,root,root,755)
%{_includedir}/qt6keychain
%{_libdir}/cmake/Qt6Keychain
%{_libdir}/libqt6keychain.so
%{_libdir}/qt6/mkspecs/modules/qt_Qt6Keychain.pri
