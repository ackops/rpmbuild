%global _python_bytecompile_errors_terminate_build 1
%define debug_package %{nil}
%define __name MarkupSafe
%define version 0.23
%define unmangled_version 0.23
%define unmangled_version 0.23
%define release 1

Summary: Implements a XML/HTML/XHTML Markup safe string for Python
Name: cb-python-%{__name}
Version: %{version}
Release: %{release}
Source0: %{__name}-%{unmangled_version}.tar.gz
License: BSD
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{__name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
Vendor: Armin Ronacher <armin.ronacher@active-4.com>
Packager: Adam Kinney <akinney@cloudbolt.io>
Url: http://github.com/mitsuhiko/markupsafe
BuildRequires: cb-python
AutoReq: 0

%description
MarkupSafe
==========

Implements a unicode subclass that supports HTML strings:

>>> from markupsafe import Markup, escape
>>> escape("<script>alert(document.cookie);</script>")
Markup(u'&lt;script&gt;alert(document.cookie);&lt;/script&gt;')
>>> tmpl = Markup("<em>%s</em>")
>>> tmpl % "Peter > Lustig"
Markup(u'<em>Peter &gt; Lustig</em>')

If you want to make an object unicode that is not yet unicode
but don't want to lose the taint information, you can use the
`soft_unicode` function.  (On Python 3 you can also use `soft_str` which
is a different name for the same function).

>>> from markupsafe import soft_unicode
>>> soft_unicode(42)
u'42'
>>> soft_unicode(Markup('foo'))
Markup(u'foo')

HTML Representations
--------------------

Objects can customize their HTML markup equivalent by overriding
the `__html__` function:

>>> class Foo(object):
...  def __html__(self):
...   return '<strong>Nice</strong>'
...
>>> escape(Foo())
Markup(u'<strong>Nice</strong>')
>>> Markup(Foo())
Markup(u'<strong>Nice</strong>')

Silent Escapes
--------------

Since MarkupSafe 0.10 there is now also a separate escape function
called `escape_silent` that returns an empty string for `None` for
consistency with other systems that return empty strings for `None`
when escaping (for instance Pylons' webhelpers).

If you also want to use this for the escape method of the Markup
object, you can create your own subclass that does that::

    from markupsafe import Markup, escape_silent as escape

    class SilentMarkup(Markup):
        __slots__ = ()

        @classmethod
        def escape(cls, s):
            return cls(escape(s))

New-Style String Formatting
---------------------------

Starting with MarkupSafe 0.21 new style string formats from Python 2.6 and
3.x are now fully supported.  Previously the escape behavior of those
functions was spotty at best.  The new implementations operates under the
following algorithm:

1.  if an object has an ``__html_format__`` method it is called as
    replacement for ``__format__`` with the format specifier.  It either
    has to return a string or markup object.
2.  if an object has an ``__html__`` method it is called.
3.  otherwise the default format system of Python kicks in and the result
    is HTML escaped.

Here is how you can implement your own formatting::

    class User(object):

        def __init__(self, id, username):
            self.id = id
            self.username = username

        def __html_format__(self, format_spec):
            if format_spec == 'link':
                return Markup('<a href="/user/{0}">{1}</a>').format(
                    self.id,
                    self.__html__(),
                )
            elif format_spec:
                raise ValueError('Invalid format spec')
            return self.__html__()

        def __html__(self):
            return Markup('<span class=user>{0}</span>').format(self.username)

And to format that user:

>>> user = User(1, 'foo')
>>> Markup('<p>User: {0:link}').format(user)
Markup(u'<p>User: <a href="/user/1"><span class=user>foo</span></a>')


%prep
%setup -n %{__name}-%{unmangled_version} -n %{__name}-%{unmangled_version}

%build
env CFLAGS="$RPM_OPT_FLAGS" /opt/cb/bin/python setup.py build

%install
/opt/cb/bin/python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)