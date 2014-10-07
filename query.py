#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('petetwitt.db')
c = conn.cursor()

print
print 'Print all users'
for row in c.execute('SELECT * FROM users'):
  print row

print
print 'All subscriptions'
for row in c.execute('SELECT * FROM subscriptions'):
  print row

print
print 'All tweets'
for row in c.execute('SELECT * FROM tweets'):
  print row

print
print 'Sessions'
for row in c.execute('SELECT * FROM sessions'):
  print row

print
print "Print peter's password"
t = ('peter@gmail.com',)
c.execute('SELECT * FROM users WHERE email=?', t)
print c.fetchone()[1]

