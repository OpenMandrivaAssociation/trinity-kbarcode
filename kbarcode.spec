%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg kbarcode
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		2.0.7
Release:		%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:		barcode and label printing application for Trinity
Group:			Applications/Utilities
URL:			http://www.kbarcode.net

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/utilities/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DWITH_NATIVE_GNU_BARCODE=OFF
BuildOption:    -DWITH_JAVASCRIPT=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

# PCRE2 support
BuildRequires:  pkgconfig(libpcre2-posix)


BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)

Requires:		%{name}-tdefile-plugin = %{?epoch:%{epoch}:}%{version}-%{release}


%description
KBarcode is a barcode and label printing application for Trinity. It can be used
to print everything from simple business cards up to complex labels with
several barcodes (e.g. article descriptions).

KBarcode comes with an easy to use WYSIWYG label designer, a setup wizard,
batch import of data for batch printing labels (directly from the delivery
note), thousands of predefined labels, database management tools and
translations in many languages. Even printing more than 10.000 labels in one
go is no problem for KBarcode. Data for printing can be imported from several
different data sources, including SQL databases, CSV files and the TDE address
book.

Additionally it is a simple barcode generator (similar to the old xbarcode you
might know). All major types of barcodes like EAN, UPC, CODE39 and ISBN are
supported. Even complex 2D barcodes are supported using third party tools. The
generated barcodes can be directly printed or you can export them into images
to use them in another application.

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{tde_prefix}/bin/kbarcode
%{tde_prefix}/share/applications/tde/kbarcode-batch.desktop
%{tde_prefix}/share/applications/tde/kbarcode-editor.desktop
%{tde_prefix}/share/applications/tde/kbarcode-single.desktop
%{tde_prefix}/share/applications/tde/kbarcode.desktop
%{tde_prefix}/share/mimelnk/application/kbarcode-label.desktop
%{tde_prefix}/share/apps/kbarcode/
%{tde_prefix}/share/icons/hicolor/*/actions/barcode.png
%{tde_prefix}/share/icons/hicolor/*/actions/kbarcodeellipse.png
%{tde_prefix}/share/icons/hicolor/*/actions/kbarcodegrid.png
%{tde_prefix}/share/icons/hicolor/*/actions/kbarcodelinetool.png
%{tde_prefix}/share/icons/hicolor/*/actions/kbarcoderect.png
%{tde_prefix}/share/icons/hicolor/*/apps/kbarcode.png
%{tde_prefix}/share/man/man1/*.1*
%{tde_prefix}/share/doc/tde/HTML/en/kbarcode/

##########

%package tdefile-plugin
Summary:		tdefile-plugin for %{name}
Group:			Applications/Utilities

%description tdefile-plugin
%{summary}.

%files tdefile-plugin
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/trinity/tdefile_kbarcode.la
%{tde_prefix}/%{_lib}/trinity/tdefile_kbarcode.so
%{tde_prefix}/share/services/tdefile_kbarcode.desktop

%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%find_lang %{tde_pkg}

# Fix invalid icon path
%__sed -i "%{buildroot}%{tde_prefix}/share/applications/tde/kbarcode.desktop" -e "s|Icon=.*|Icon=kbarcode|"

