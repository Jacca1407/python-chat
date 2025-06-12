# python-chat
A **python TUI chat application** built with _socket_ and _textual_.

Once you run it it asks Remote IP and port and local listening port and then starts the TUI. 

For every folder there's the **python file**, the .tcss file (**Textual stylesheet**) and a **Windows standalone executable**

## V1
The difference between v1 and v2 is the security: **v1 doesn't use RSA encryption**. 

The messages can be **easily sniffed** with programs like **Wireshark**

## V2
**In the second version** as soon as the connection is established it sends the **RSA 1024 byte public keys** to the peer and since then, every message is encrypted.

If a hacker tries to sniff with Wireshark the packages **will not be understandable.**

## GNU LICENSE
**Freedom to use, modify, and share:** You can freely use, modify, and distribute the software.

**Copyleft requirement:** Any distributed modified versions must also be licensed under the GPL, keeping the software open source.

> **Author:** Andrea J.