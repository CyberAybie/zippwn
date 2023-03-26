from colorama import Fore,Back,Style
from itertools import chain,product
from optparse import OptionParser
from zipfile import ZipFile
import string
import signal
import time
import sys
import os

banner='''
 _______  ___   _______  _______  _     _  __    _
|       ||   | |       ||       || | _ | ||  |  | |
|____   ||   | |    _  ||    _  || || || ||   |_| |
 ____|  ||   | |   |_| ||   |_| ||       ||       |
| ______||   | |    ___||    ___||       ||  _    |
| |_____ |   | |   |    |   |    |   _   || | |   |
|_______||___| |___|    |___|    |__| |__||_|  |__|'''


class main():
    def __init__(self):
        self.passFound_print = lambda tries,word: f"{Fore.LIGHTGREEN_EX}Pwned!!!! Password was found after {Fore.LIGHTGREEN_EX+str(tries)} {Style.RESET_ALL}combinations. The password is: {Fore.LIGHTGREEN_EX+word}"
        self.tries_print = lambda tries,word: f"{Fore.LIGHTCYAN_EX}Combination: {tries} > {word}"
        self.saves_dir = os.path.dirname(os.path.abspath(__file__))+"/stateSaves"
        self.passFound = False
        self.done = False

    def signal_handler(self, signal, frame):
        self.done=True

    def wlist_crack(self, tries, wordlist, z, stream, archive_dir, wordlist_inp):
        content = z.namelist()
        for word in wordlist:
            try:
                if self.done==True:
                    confirm = input("\nAre you sure you want to stop (y/n) > ").lower()
                    if confirm == "y": self.save_state(archive_dir, wordlist_inp, word, stream, wordlist); return
                    self.done = False

                tries += 1
                if stream: print(self.tries_print(tries,word))
                z.setpassword(word.encode('utf8', errors='ignore'))
                z.read(content[0])
                self.passFound = True
                print(self.passFound_print(tries,word))
                print(Fore.CYAN + banner)
                return
            except:
                pass

    def wlist_crack_entry(self, archive_dir, wordlist_inp, showoutput_b, resume_index):
        tries = 0
        try:
            try: _archive = ZipFile(archive_dir, "r")
            except Exception as ex: print(ex); sys.exit(1)
            print("Getting all the words from dictionary ^_^")
            _wordlist = open(wordlist_inp, 'r', encoding="utf8", errors='ignore')
            wordlist = _wordlist.read().splitlines()
            _wordlist.close()
            if resume_index != None:
                wordlist = wordlist[resume_index-1:]
                tries = resume_index-1
            print("Bring it on!!!")

            self.wlist_crack(tries, wordlist, _archive, showoutput_b, archive_dir, wordlist_inp)
        except IOError:
            print("Wordlist Doesen't Exist - Make sure it is in the same directory as this file")
            sys.exit(1)

    def save_state(self, archive_dir, wordlist_inp, current_word, showoutput_b, generated_list):
        while True:
            saveState = input("\nDo you want to save the Current State and continue from here later? [--restore]  (y/n) > ").lower()
            if saveState == "y":
                try:
                    print("[+] Saving Current State")
                    if not os.path.exists(self.saves_dir): os.makedirs(self.saves_dir)

                    name = f"{self.saves_dir}/{time.strftime('%b-%d-%Y-%H-%M-%S')}-wordlist.txt"
                    f = open(name,"w")
                    f.write(f"{os.path.abspath(archive_dir)},{os.path.abspath(wordlist_inp)},{int(showoutput_b)},{generated_list.index(current_word)}")
                    f.close()
                    print(f"[finished] {name}")
                    break
                except IOError as ex:
                    print(f"Error when saving file: {ex}")
                except Exception as ex:
                    print(f"Unexpected error: {ex}")
            elif saveState == "n":
                break


    def restore(self):
        try:
            savefiles = [f for f in os.listdir("./stateSaves") if os.path.isfile(os.path.join("./stateSaves", f))]
            restoreNbr = int(options.restore)
            print(savefiles[restoreNbr])
            f = open(f"./stateSaves/{savefiles[restoreNbr]}")
            resfile = f.read().split(',')
            f.close()

            self.wlist_crack_entry(resfile[0], resfile[1], bool(int(resfile[2])), int(resfile[3]))
        except FileNotFoundError:
            print("No restore files found")
        except IndexError as ex:
            print(f"Restore file index given is not valid or the restorefile is broken {ex}")
        except Exception as ex:
            print(f"Unexpected error: {ex}")

    def _noargs(self):
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "\n\n\tMade by Aybie")
        archive_dir = input('\nEnter .zip file name : ')
        wordlist_inp = input("Enter dictionary name : ")
        self.wlist_crack_entry(archive_dir, wordlist_inp, True, None)


    def main(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        if len(sys.argv[1:]) == 0:
            self._noargs()
        else:
            self._args()
        print(Style.RESET_ALL)

        if self.passFound == False:
            print("Couldnt Crack The Password With The Current Options")


if __name__ == "__main__":
    main().main()
