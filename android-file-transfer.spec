%define _appdatadir %{_datadir}/appdata

Summary:	Interactive MTP client with Qt GUI
Name:		android-file-transfer
Version:	4.3
Release:	2
License:	GPLv2+
Group:		File tools
Url:		https://github.com/whoozle/android-file-transfer-linux/
Source0:  https://github.com/whoozle/android-file-transfer-linux/archive/v%{version}/%{name}-linux-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(taglib)
BuildRequires:	desktop-file-utils
BuildRequires:	appstream-util
BuildRequires:	pkgconfig(fuse)
BuildRequires:	readline-devel
BuildRequires:	ninja

%patchlist
android-file-transfer-4.3-qt6.patch

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
