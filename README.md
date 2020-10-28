# PassGen
A small random password generator written in Python. If you're on a Mac it copies the password to the clipboard, then deletes it after 60 seconds.

This is very helpful if you find that you have to create and paste a lot of new passwords for web apps and you want to have time to paste the new password into a web app and into your password manager app, but then have the password deleted from the clipboard so that you don't later paste it someplace insecure, like into a Slack channel or something.

## Requirements

* Python 3
* [pyperclip 1.7.0](https://pypi.org/project/pyperclip/1.7.0/)

## Setup

1. Clone this repository.
2. Change into the repo directory that you just cloned.
3. Install the `pyperclip` module, which is the only thing listed inside the `requirements.txt` file. This is how the passwords get copied to your Mac's clipboard.

```
$ git clone git@github.com:tcpiplab/PassGen.git
$ cd PassGen
$ pip install -r requirements.txt
```

### Optional: Setup a Bash alias

Add an alias to your `.bash_profile` file so you can run this from the shell without having to call Python. Here is an example. You may or may not want to be using a `venv` in your path. That is not required. The point here is that the alias calls Python, wherever you have it installed, and the argument to Python is the path to `passgen.py`. The example below shows the alias on my Mac.

```
$ grep passgen ~/.bash_profile
alias passgen='/Users/lsheppard/PassGen/venv/bin/python /Users/lsheppard/PassGen/passgen.py'
```

After editing your `.bash_profile`, don't forget to source it again.

```
$ cd ~
$ . .bash_profile
```

## Usage

You have to give a password length when you run it. For example, if you want 10 character passwords to choose from, run this:

```
$ passgen 10
```

In the example below, the user invoked `passgen.py` asking for 10 character passwords. The terminal then filled up with 14 passwords to choose from. This example was generated inside a small terminal window. If you want a lot of passwords to choose from you need a bigger terminal window. The user selected password number 3 by typing in `03` and hitting Enter. This copied the password `ep0+?8%%vi` to the Mac's clipboard and started a 60 second timer, printing the remaining seconds as it counted down. When the countdown ended the password was deleted from the clipboard. 

```
$ passgen 10
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
60 59 58 57 56 55 54 53 52 51 50 49 48 47 46 45 44 43 42 41 40 39 38 37 36 35 34 33 32 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 
```

Here is a color screenshot. The colors help you choose a password containing all character classes. For example, although password number 11, like the others, was generated at random, you can see that is contains too many lowercase letters (red), and it does not contain any uppercase letters (white).

![Screen Shot 2020-10-27 at 8.47.27 PM.png](https://github.com/tcpiplab/PassGen/blob/master/Screen%20Shot%202020-10-27%20at%208.47.27%20PM.png)

Pull requests are welcome.