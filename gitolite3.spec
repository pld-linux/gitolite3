%include	/usr/lib/rpm/macros.perl
Summary:	Software for hosting git repositories
Summary(pl.UTF-8):	Narzędzie do hostowania repozytoriów git
Name:		gitolite3
Version:	3.6.5
Release:	2
License:	GPL v2
Group:		Development/Tools
Source0:	https://github.com/sitaramc/gitolite/tarball/v%{version}/gitolite-%{version}.tar.gz
# Source0-md5:	62d15150914084a37e6fcab6fdf63d34
Source1:	gitolite.pl
Patch0:		%{name}-README.patch
Patch1:		REF_OR_FILENAME_PATT.patch
URL:		https://github.com/sitaramc/gitolite
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	git-core >= 1.6.6
Requires:	openssh-server >= 5.0
Conflicts:	gitolite
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gitolite allows a server to host many git repositories and provide
access to many developers, without having to give them real userids on
the server. The essential magic in doing this is ssh's pubkey access
and the authorized_keys file, and the inspiration was an older program
called gitosis.

Gitolite can restrict who can read from (clone/fetch) or write to
(push) a repository. It can also restrict who can push to what branch
or tag, which is very important in a corporate environment. Gitolite
can be installed without requiring root permissions, and with no
additional software than git itself and Perl.

Gitolite 3.x is a total rewrite of Gitolite 2.x, see the online
documentation for upgrade instructions.

%description -l pl.UTF-8
Gitolite pozwala na hostowanie wielu repozytoriów git na jednym
serwerze i udostępnianie ich wielu deweloperom bez potrzeby nadawania
tworzenia dla nich rzeczywistych użytkowników na serwerze. Cała magia
polega na dostępie przy użyciu kluczy SSH oraz pliku authorized_keys,
a inspiracją był starszy program o nazwie gitosis.

Gitolite pozwala na ograniczenie, kto może odczytywać (operacje
clone/fetch) i zapisywać (operacja push) do repozytorium. Pozwala
także kontrolować, kto może zapisywać na daną gałąź lub etykietę, co
może być bardzo ważne w środowisku korporacyjnym. Gitolite może być
zainstalowany bez dostępu do konta roota i bez dodatkowego
oprogramowania poza samym gitem i Perlem.

Gitolite 3.x to kod Gitolite napisany od nowa, dokumentacja online
wyjaśnia proces aktualizacji.

%package contrib
Summary:	Contributed scripts for Gitolite
Group:		Networking
Requires:	%{name} = %{version}-%{release}

%description contrib
Contributed scripts for Gitolite.

%prep
%setup -qc
mv sitaramc-gitolite-*/* .
%{__rm} -r sitaramc-gitolite-*

%patch0 -p1
%patch1 -p1

echo "v%{version}" > src/VERSION # add '-pld' suffix or something if patched

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir},%{perl_vendorlib}}
install -p check-g2-compat convert-gitosis-conf $RPM_BUILD_ROOT%{_bindir}

cp -a src $RPM_BUILD_ROOT%{_datadir}/gitolite
mv $RPM_BUILD_ROOT%{_datadir}/gitolite/lib/* $RPM_BUILD_ROOT%{perl_vendorlib}
rmdir $RPM_BUILD_ROOT%{_datadir}/gitolite/lib

ln -sf %{_datadir}/gitolite/gitolite $RPM_BUILD_ROOT%{_bindir}
ln -sf %{_datadir}/gitolite/gitolite-shell $RPM_BUILD_ROOT%{_bindir}

cp -a contrib $RPM_BUILD_ROOT%{_datadir}/gitolite
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/gitolite

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG CONTRIBUTING README.markdown
%attr(755,root,root) %{_bindir}/gitolite
%attr(755,root,root) %{_bindir}/gitolite-shell
%attr(755,root,root) %{_bindir}/check-g2-compat
%attr(755,root,root) %{_bindir}/convert-gitosis-conf

%dir %{_datadir}/gitolite
%{_datadir}/gitolite/gitolite.pl

%attr(755,root,root) %{_datadir}/gitolite/gitolite
%attr(755,root,root) %{_datadir}/gitolite/gitolite-shell
%{_datadir}/gitolite/VERSION

%dir %{_datadir}/gitolite/VREF
%attr(755,root,root) %{_datadir}/gitolite/VREF/*

%dir %{_datadir}/gitolite/commands
%attr(755,root,root) %{_datadir}/gitolite/commands/*

%dir %{_datadir}/gitolite/syntactic-sugar
%{_datadir}/gitolite/syntactic-sugar/*

%dir %{_datadir}/gitolite/triggers
%dir %{_datadir}/gitolite/triggers/post-compile
%attr(755,root,root) %{_datadir}/gitolite/triggers/bg
%attr(755,root,root) %{_datadir}/gitolite/triggers/partial-copy
%attr(755,root,root) %{_datadir}/gitolite/triggers/renice
%attr(755,root,root) %{_datadir}/gitolite/triggers/repo-specific-hooks
%attr(755,root,root) %{_datadir}/gitolite/triggers/set-default-roles
%attr(755,root,root) %{_datadir}/gitolite/triggers/upstream
%attr(755,root,root) %{_datadir}/gitolite/triggers/expand-deny-messages
%attr(755,root,root) %{_datadir}/gitolite/triggers/post-compile/*

%{perl_vendorlib}/Gitolite

%files contrib
%defattr(644,root,root,755)
%{_datadir}/gitolite/contrib
