# PassGen
A small random password generator written in Python. If you're on a Mac it copies the password to the clipboard, then deletes it after 60 seconds.


This is very helpful if you find that you have to create and paste a lot of new passwords for websites, and you want to have time to paste the new password into a web app and into your password manager app, but then have the password deleted from the clipboard so that you don't later paste it somewhere insecure, like into a Slack channel or something.

There is also a colorful interactive mode where you can choose from a list of passwords. See screenshots below.

## Requirements

* Python 3
* [pyperclip 1.7.0](https://pypi.org/project/pyperclip/1.7.0/)
* [termcolor 1.1.0](https://pypi.org/project/termcolor/)

## Setup

1. Clone this repository.
2. Change into the repo directory that you just cloned.
3. Install the `pyperclip` module and the `termcolor` module, these are listed inside the `requirements.txt` file. These modules handle how the passwords get copied to your computer's clipboard, and color output, respectively.

```
$ git clone git@github.com:tcpiplab/PassGen.git
$ cd PassGen
$ pip3 install -r requirements.txt
```

### Optional: Set up a Bash alias

Add an alias to your `.bash_profile` file so that you can run this from the shell without having to call Python. Here is an example. You may or may not want to be using a `venv` in your path. That is not required. The point here is that the alias calls Python, wherever you have it installed, and the argument to Python is the path to `passgen.py`. The example below shows the alias on my Mac.

```
$ grep passgen ~/.bash_profile
alias passgen='/Users/lsheppard/PassGen/venv/bin/python /Users/lsheppard/PassGen/passgen.py'
```

After editing your `.bash_profile`, don't forget to source it again.

```
$ cd ~
$ . .bash_profile
```

## Usage and cli options

### Default behavior with no arguments

```
$ passgen
The clipboard will be cleared in 60 seconds 
```
Silent mode is the default behavior, meaning that you run the command and a randomly generated password is silently copied to your clipboard. Then you have 60 seconds before the clipboard is erased. 


### `-l --length n` Specifying Password Length
You can specify a password length when you run it by using the `-l` or `--length` options followed by an integer. For example, if you want a 10 character password, run this:

```
$ passgen --length 10
```

If `passgen` is called without specifying the length the password(s) will default to 20 characters.

### `-i --interactive` Interactive Mode
Interactive mode is invoked using the `-i` or `--interactive` options. The output will display a list of numbered rows of passwords for you to choose from. Enter the number of a row and the corresponding password will be copied to the clipboard. Then, 60-seconds later the clipboard will be erased.

In the example below, the user invoked `passgen.py` in interactive mode asking for 10 character passwords. The terminal then filled up with 14 passwords to choose from. This example was generated inside a small terminal window. If you want a lot of passwords to choose from you need a bigger terminal window. The user selected password number 3 by typing in `03` and hitting Enter. This copied the password `ep0+?8%%vi` to the Mac's clipboard and started a 60-second timer, printing the remaining seconds as it counted down. When the countdown ended the password was deleted from the clipboard. 

```
$ passgen --interactive --length 10
10
00   >HO'Q5GR'p
01   ~q0ByACEW'
02   -Y,6v9s'Cv
03   ep0+?8%%vi
04   cRW{gvJ0cz
05   4~bxs4v`?S
06   n/.%;mk-Wh
07   KwnD%%XN?(
08   BF8<yA/jDH
09   $c'7mZnvHU
10   c-],4t&W8P
11   srsma\7';h
12   VWl2%e.OY_
13   ":7m5UID#4
14   Sp_dy$NfWt
Enter the number of the password you want sent to the clipboard: 03
The clipboard will be cleared in 60 seconds 
```

Here is a color screenshot. The colors help you choose a password containing all character classes. For example, although password number 7, like the others, was generated at random, you can see that is does not contain numbers (cyan).

![passgen-interactive-10-screenshot.png](https://github.com/tcpiplab/PassGen/blob/master/passgen-interactive-10-screenshot.png "This is a screenshot of the passgen script being used in interactive mode. The user has asked for 10 character passwords.")

### `-j --japanese` Include Japanese Hiragana characters in the passwords
Thanks to GitHub user [Tunl-Lite](https://github.com/Tunl-Lite) for this feature. Note that if you use a password with Japanese or other languages' characters you might encounter problems when trying to enter that password in some software, for example what happened to [this guy](https://answers.microsoft.com/en-us/windows/forum/all/inputting-and-ime-password-for-wifi-not-allowed/322eba17-c568-4e84-b36c-5e83da63608e). This feature works in silent or interactive mode.

![passgen-japanese-screenshot.png](https://github.com/tcpiplab/PassGen/blob/master/passgen-japanese-screenshot.png "This screenshot shows passgen creating passwords containing Japanese characters.")

### `-w --random-words` Embed a random English word within each password.
This feature will make the passwords easier to type and remember. But the password length must be at least 20 characters because of the threat of dictionary attacks. This feature works in silent or interactive mode.

![passgen-random-words-screenshot.png](https://github.com/tcpiplab/PassGen/blob/master/passgen-random-words-screenshot.png "This is a screenshot of passgen creating passwords with random words embedded inside each password.")

Pull requests and feature requests are welcome.
