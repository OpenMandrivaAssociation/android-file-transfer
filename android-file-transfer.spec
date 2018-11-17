%define _appdatadir %{_datadir}/appdata

Summary:	Interactive MTP client with Qt GUI
Name:		android-file-transfer
Version:	3.7
Release:	1
License:	GPLv2+
Group:		File tools
Url:		https://github.com/whoozle/android-file-transfer-linux/
Source0:  https://github.com/whoozle/android-file-transfer-linux/archive/v%{version}/%{name}-linux-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	qt5-qtbase-devel
BuildRequires:	desktop-file-utils
BuildRequires:	appstream-util
BuildRequires:	pkgconfig(fuse)
BuildRequires:	readline-devel
BuildRequires:	ninja

%description
Interactive MTP client with Qt GUI.

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-linux-%{version}

%build
%cmake -GNinja

%ninja_build

%install
%ninja_install -C build

find %{buildroot} -name '*.a' -delete

desktop-file-install                                       \
    --remove-category="System"                             \
    --remove-category="Filesystem"                         \
    --delete-original                                      \
    --dir=%{buildroot}%{_datadir}/applications             \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml

%files
%doc README.md FAQ.md
%license LICENSE
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_iconsdir}/hicolor/*/apps/%{name}.png
