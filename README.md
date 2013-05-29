blc.py
======

An easy-peasy to use BlooCoin library using standard libraries.

Usage
-----

Most of the commands are abstracted, so you can easily use them with only a small understanding of the BLC protocol.  
In general, you can use commands like this:
```python
q = Query(foo="bar", this="that")
payload = q()
payload['baz']
```

There are various commands implemented, here's a list:

+ `blcpy.Check`
+ `blcpy.CheckAddr`
+ `blcpy.GetCoin`
+ `blcpy.MyCoins`
+ `blcpy.Register`
+ `blcpy.SendCoin`
+ `blcpy.TotalCoins`
+ `blcpy.Transactions`

For a more thorough understanding of each of the commands, you can run `help()` on the classes in a Python REPL (like: `help(blcpy.Check)`).  
Commands have a `required` list on them, which are the pieces required for this command to succeed on the server. If any of these are missing, a `blcpy.MissingFields` exception will be raised.
