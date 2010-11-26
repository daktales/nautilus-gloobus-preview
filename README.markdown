# nautilus-gloobus-preview

This extension map any key to gloobus-preview (http://gloobus.net/)
and create a relative menu entry in nautilus.

## What's gloobus-preview?
"Gloobus-Preview is an extension for the Gnome Desktop Environment 
designed to enable a full screen preview of any kind of file. It's based 
on Apple's Quicklook."

With my extension there's no need to install patched nautilus 
(nautilus-elementary), simply run:

    python setup.py install

Internalization support (for now only IT and EN (default))

Only dependence: dev-python/nautilus-python
(on gentoo it's called like above, in other distro dont'know)

## TODO:
* Write more localization (help :P )
* Testing (more)
* Gentoo ebuild

## For user:

Extract provided archive and run as root:

    python setup.py install

After you can change hotkey from 'System preferences' (default hotkey is 'space')
Restart Nautilus:

    nautilus -q
    nautilus --no-desktop


## For packagers:

Build system done, email me (or fill an issue) for anything.


Walter Da Col <walter.dacol AT gmail.com>
