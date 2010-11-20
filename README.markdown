# nautilus-gloobus-preview

This extension map 'space' key to gloobus-preview (http://gloobus.net/)
and create a relative menu entry in nautilus.

## What's gloobus-preview?
"Gloobus-Preview is an extension for the Gnome Desktop Environment 
designed to enable a full screen preview of any kind of file. It's based 
on Apple's Quicklook."

With my extension there's no need to install patched nautilus 
(nautilus-elementary), simply put it in nautilus-python extension dir 
and restart Nautilus.

    default on gentoo x86: /usr/lib/nautilus/extensions-2.0/python/

It support localization, using "locale" dir (currently IT and EN only 
but feel free to contribuite). (VERY BAD IMPLEMENTATION)

Only dependence: dev-python/nautilus-python
(on gentoo it's called like above, in other distro dont'know)

## TODO:
* Provide gentoo ebuild
* Support user-defined keybinding (with some nice GUI )
* Rewrite localization support ( i18n )
* Provide package

## For user:

I push only working code, so for now you can try my extension without big issues (I hope). 

## For packagers:

Soon I'll release it with distutils support, Please wait.

Walter Da Col <walter.dacol AT gmail.com>
