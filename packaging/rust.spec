%bcond_with bootstrap

Name:           @@PKG_NAME@@
Version:        @@PKG_VERSION@@
Release:        @@PKG_RELEASE@@%{?dist}
Summary:        The Rust Programming Language
License:        ASL 2.0, MIT
URL:            http://www.rust-lang.org
# Sources go above
Source0:        @@PKG_NAME@@-@@PKG_VERSION@@-@@PKG_RELEASE@@.tar.gz

BuildRequires:  python
BuildRequires:  make
BuildRequires:  gcc-c++

%if %{with bootstrap}
BuildRequires:  curl
%else
BuildRequires:  rust
%endif

%filter_from_requires /%{_target_cpu}-unknown-linux-gnu/d
%filter_requires_in -P bin/(rust|cargo).*
%filter_setup

%description
Rust is a fast systems programming language that guarantees memory
safety and offers painless concurrency (no data races). It does not
employ a garbage collector and has minimal runtime overhead.

%package        docs
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    docs
This is the documenation package for Rust.

%prep
%setup -q

# Extracing tarballs above

%build

export CFG_EXTRACTED_VERSION="@@CFG_EXTRACTED_VERSION@@"

./configure \
%if %{without bootstrap}
   --enable-local-rust \
%endif

make
make dist-tar-bins

mkdir -p dist/extract
cd dist/extract
ls -l ..
tar -zvxf ../rust-docs-*.tar.gz
tar -zvxf ../rustc-*.tar.gz
cd -

%check

# TODO

%install

export CFG_EXTRACTED_VERSION="@@CFG_EXTRACTED_VERSION@@"

rm -rf %{buildroot}
cd dist/extract/rustc-*
./install.sh \
    --prefix=%{buildroot}/%{_prefix} --libdir=%{buildroot}/%{_libdir} \
    --disable-verify
cd -

cd dist/extract/rust-docs-*
./install.sh \
    --prefix=%{buildroot}/%{_prefix} --libdir=%{buildroot}/%{_libdir} \
    --disable-verify
cd -

mkdir -p %{buildroot}/%{_sysconfdir}/ld.so.conf.d
cat <<EOF | tee /%{buildroot}/%{_sysconfdir}/ld.so.conf.d/rust-%{_target_cpu}.conf
%{_libdir}/rustlib/
%{_libdir}/rustlib/%{_target_cpu}-unknown-linux-gnu/lib/
EOF

sed -i "s#%{buildroot}##g" %{buildroot}/%{_libdir}/rustlib/manifest-rustc
sed -i "s#%{buildroot}##g" %{buildroot}/%{_libdir}/rustlib/manifest-rust-docs
sed -i "s#%{buildroot}##g" %{buildroot}/%{_libdir}/rustlib/install.log

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_sysconfdir}/ld.so.conf.d/rust-*.conf
%{_bindir}/rust*
%{_libdir}/lib*
%{_libdir}/rustlib/*
%{_datadir}/man/*

%files docs
%{_datarootdir}/doc

%changelog
