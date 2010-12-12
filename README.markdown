# nautilus-gloobus-preview

## What's gloobus-preview?
"Gloobus-Preview is an extension for the Gnome Desktop Environment 
designed to enable a full screen preview of any kind of file. It's based 
on Apple's Quicklook."

## Extension (this project):
This extension map any key to gloobus-preview (http://gloobus.net/)
and create a relative menu entry in nautilus.
With my extension there's no need to install patched nautilus 
(nautilus-elementary).
Internalization support (more coming)

## Dependences: 
Gentoo:

* dev-python/nautilus-python
* dev-util/pkgconfig
* sys-devel/gettext

Other distro:

* python-nautilus (runtime)
* pkg-config (build time)
* gettext (build time)

## TODO:

* Write more localization (help :P )
* Testing (more)
* Fix Issues

## For user (gentoo):
Extract provided archive and run as root:

    python setup.py install

Or wait for sunrise-overlay (better)

After you can change hotkey from 'System preferences' (default hotkey is 'space')
To see changes restart Nautilus:

    nautilus -q
    nautilus --no-desktop

## For user (other)
Please wait until i'll understand ubuntu/debian --install-layout=deb option

If you can't wait use:

    sudo python setup.py install --install-layout=deb

## For packagers:
Build system done, email me (or fill an issue) for anything.


Walter Da Col <walter.dacol AT gmail.com>
