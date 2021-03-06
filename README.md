mypass
======

[![Build Status](https://travis-ci.org/snoack/mypass.svg?branch=master)](https://travis-ci.org/snoack/mypass)

A password manager that can be used conviniently from the command line. I
prefer the command line over the GUI, and the lack of password managers that
serve this use case, motivated me to write my own. It also comes with a browser
extension in order to conviniently but securely fill out logins on the web.


Installation
------------

### On Debian/Ubuntu

A package is available from the author's PPA, which can be installed by running
following commands (as root):

```
add-apt-repository ppa:s.noack/ppa
apt-get update
apt-get install mypass
```


### Using pip

Make sure you have Python 3, *pip* and *git* installed. Then run following
command (as root):

```
pip3 install git+https://github.com/snoack/mypass
```

If you want completion for subcommands, contexts and usernames when you hit
*tab* in Bash, copy [`bash-completion/mypass`][1] to `/etc/bash_completion.d/`.

Usage
-----

When you run most of the commands below, you will be prompted for the passhprase
to decrypt/encrypt the credentials with. If the encrypted file doesn't exist yet,
it will be created when you store any credentials for the first time.
By default, a daemon is spawned and shuts down after 30 minutes of inactivity,
so that you don't have to enter your passphrase again when performing multiple
actions within that period.


#### `mypass add <context> [<username>] [<password>]`

Stores credentials for the given *context*.

The *context* can be any unique keyword which you relate to these credentials. But
if the credentials are for a website, it is recommended to use the corresponding
domain as *context*, so that the browser extension finds the credentials, see below.

The *username* is optional, but specifying a username if there is any, allows you
to store multiple username/password pairs for the same context. Also, if a username
is given, it will be used by the browser extension when filling out web forms.

If *password* is omitted you will be prompted for the password. **Passing the
password on the command line is NOT recommeded**, except for import scripts,
as it will end up in your shell's history.


#### `mypass new <context> [<username>]`

Same as `mypass add`, but stores a new random secure password and prints it.


#### `mypass get <context>`

Prints the credentials for the given *context*.


#### `mypass list`

Prints each context (one per line) that any credentials have been stored for.
In order to filter the list, just pipe the output to programs like `grep`.


#### `mypass remove <context> [<username>]`

Deletes credentials from the encrypted storage. If *username* is given, only
this username and the associated password is removed. If *username* is omitted,
the whole *context* is wiped.


#### `mypass rename --new-{context|username}=<newvalue> <context> [<username>]`

Moves credentials around within the encrypted storage.


##### Examples

Renaming a context:

```
mypass rename --new-context=new.example.com old.example.com
```

Changing the username for *example.com* from *john* to *rose*:

```
mypass rename --new-username=rose example.com john
```

Adding a username to a password which has been stored without an associated username:

```
mypass rename --new-username=rose example.com
```


#### `mypass changepw`

Prompts you for a new passphrase. Existing credentials are re-encrypted
using this passphrase.


#### `mypass lock`

Forces the daemon to immediately shutdown, if it is running,
so that you'd have to enter the passphrase again, from now on.


Configuration
-------------

Optionally, you can create a config file under `~/.config/mypass`, in order to
override any of the following presets:

```ini
[daemon]
# If set to true, the daemon won't spawn, and you have to enter the
# passphrase, the credentials are encrypted with, every time.
disabled = false

# Minutes of inactivity after which the daemon shuts down, and you have
# to enter the passphrase, the credentials are encrypted with, again.
timeout = 30

[database]
# Path to the encrypted file storing the credentials.
path = /home/user/.config/mypass/db
```


Integration with Chrome and Firefox
-----------------------------------

If you installed `mypass` on Debian/Ubuntu from the PPA above, next time you
start Chromium or Firefox, the extension should be active. You can also install
the extension from the [Chrome Web Store][2]. Note that while the browser
extension is optional, it cannot be used standalone but requires the command
line utility to be installed as well.

The extension adds a button to the browser bar that when clicked, fills out login
forms in the active tab, if the document's domain and path (partially) match the
*context* of any stored credentials. If the document's URL is `https://www.example.com/foo/bar`
for example, credentials from following contexts are considered, in this order:

1. `www.example.com/foo/bar`
2. `www.example.com/foo`
3. `www.example.com`
4. `example.com`

The browser extension is intentionally kept simple and doesn't provide functionality
to manage credentials. Please use the command line utility therefore.

[1]: https://raw.githubusercontent.com/snoack/mypass/master/bash-completion/mypass
[2]: https://chrome.google.com/webstore/detail/mypass/ddbeciaedkkgeiaellofogahfcolmkka
