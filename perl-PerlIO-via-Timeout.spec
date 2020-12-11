#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	PerlIO
%define		pnam	via-Timeout
Summary:	PerlIO::via::Timeout - a PerlIO layer that adds read & write timeout to a handle
#Summary(pl.UTF-8):
Name:		perl-PerlIO-via-Timeout
Version:	0.32
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/PerlIO/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	f18328a39a5eaa386e34df80f066039b
# generic URL, check or change before uncommenting
#URL:		https://metacpan.org/release/PerlIO-via-Timeout
BuildRequires:	perl-Module-Build
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
%if %{with tests}
BuildRequires:	perl-Test-TCP
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package implements a PerlIO layer, that adds read / write
timeout. This can be useful to avoid blocking while accessing a handle
(file, socket, ...), and fail after some time.

The timeout is implemented by using <select> on the handle before
reading/writing.

WARNING the handle won't timeout if you use sysread or syswrite on it,
because these functions works at a lower level. However if you're
trying to implement a timeout for a socket, see IO::Socket::Timeout
that implements exactly that.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Build.PL \
	--destdir=$RPM_BUILD_ROOT \
	--installdirs=vendor
./Build

%{?with_tests:./Build test}

%install
rm -rf $RPM_BUILD_ROOT

./Build install \
	--prefix=%{_prefix} \
	--destdir=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/PerlIO/via/*.pm
%{_mandir}/man3/*
