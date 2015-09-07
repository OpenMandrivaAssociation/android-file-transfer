%define _appdatadir %{_datadir}/appdata

Summary:	Interactive MTP client with Qt GUI
Name:		android-file-transfer
Version:	2.3
Release:	2
License:	GPLv2+
Group:		File tools
Url:		https://github.com/whoozle/android-file-transfer-linux/
# From git by tag https://github.com/whoozle/android-file-transfer-linux/
Source0:	%{name}-linux-%{version}.tar.gz
# Provided upstream by the developer :
# https://github.com/whoozle/android-file-transfer-linux/commit/ada01cf7bc57fcfb99f540cc098e5393937a0436
Source1:	android-file-transfer.appdata.xml

BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	qt5-qtbase-devel
BuildRequires:	desktop-file-utils
BuildRequires:	appstream-util

%description
Interactive MTP client with Qt GUI.

%files
%doc LICENSE README.md
%{_bindir}/%{name}
%{_bindir}/aft-mtp-cli
%{_bindir}/aft-mtp-mount
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_appdatadir}/%{name}.appdata.xml

#----------------------------------------------------------------------------

%prep
%setup -qn %{name}-linux-%{version}
cp -R %{SOURCE1} android-file-transfer.appdata.xml

%build
%cmake_qt5
%make

%install
%makeinstall_std -C build

# install menu entry
desktop-file-install qt/%{name}.desktop \
  --dir=%{buildroot}%{_datadir}/applications
  
# install menu icons
for N in 16 32 48 64 128 256;
do
convert qt/%{name}.png -scale ${N}x${N} $N.png;
install -D -m 0644 $N.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done

#appdata
mkdir -p %{buildroot}%{_appdatadir}
cp -R %{SOURCE1} %{buildroot}%{_appdatadir}/android-file-transfer.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_appdatadir}/*.xml

