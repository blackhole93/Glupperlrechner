#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
# Generiert zufaellige Glupperlbestellung aus unserem (noch eingeschraenktem) Sortiment und berechnet deren Preis.
# Schwierigkeitsgrad anpassbar ('easy', 'medium', 'hard').
# Je schwerer, desto mehr Klammern werden im Mittel gewählt, ab medium kann der Kunde zusätzlich eine Bedienung sein und ab hard kann er bei einzelnen Klammern auch die Rückseite beschriften lassen.

# Singleplayer: Bei korrektem Ergebnis im hard modus wird ein geheimer Kunde freigeschaltet
# Multiplayer: - Jede Bestellung hat identische Werte für Bedienung, Anzahl Glupperl, Anzahl doppelseitig
#              - Man wird nur bei korrekter Antwort ins ranking aufgenommen

import numpy as np
import os
import timeit
import time

clear = lambda: os.system('cls')

## Array of glupperl designs that can be chosen
# Even indices: 1D list of designs
# Odd indices: various features: frequency of order, price
glupperlarr = ['Herz rot gebrannt',[15,3], 
               'Herz blau gebrannt',[5,3],
               'Holzherz rot',[2,3],
               'Holzherz rosa',[1,3],
               'Schleife rot',[2,3],
               'Schleife blau',[2,3],
               'Käfer Klee',[1,3],
               'Strassherz Lila',[3,3],
               'Enzian',[1,3],
               'Lebkuchenherz',[4,4],
               'Breze Radi...oder Blume?!',[3,4],
               'Bierkrug weiß-blau',[6,4],
               'Staatswappen Holz',[3,4],
               'Münchner Kindl',[2,4],
               'Hut grün',[4,4],
               'Dom',[1,4],
               'Schleife-Breze',[3,4],
               'Schleife-Strassherz',[3,4],
               'Holzherz Strassrand',[5,6],
               'Astrind Herz rot',[2,4],
               'Astrinde Stempel Vogel',[4,4],
               'Metallpin Ludwig',[4,6],
               'Glocke rot',[2,6],
               'Hirsch acryl grün',[2,5],
               'Krone Holz',[1,4],
               'Krone Strass blau',[3,6],
               'Edelweiss Filzherz grün',[4,5],
               'Herz groß blau + Schleife',[2,5],
               'Ösi Fahne',[3,4],
               'Klammer breit - Herz rot',[2,5],
               'Breze',[2,4],
               'Selfiequeen',[1,4],
               'Anstecker Emaille',[1,12],
               #"Brett 'Liebesherz'",[1,12],
               'Kugelschreiber Holzknopf',[1,5],
               'Kugelschreiber Metallknopf',[1,6],
               'Lesezeichen Frauenkirche',[2,4],
               'Glasfinder Lederhose',[1,3]]
              
             
## Randomly choose the designs the customer wants and calcuate total price
  # Allocate array of all pegs weighted by their frequency
def get_bounds():
  freq_tot = 0
  glupperl_bounds = np.zeros(int(0.5*len(glupperlarr)))
  for i in range(int(0.5*len(glupperlarr))):
    freq_tot += glupperlarr[1+2*i][0]
    glupperl_bounds[i] = freq_tot
  return freq_tot,glupperl_bounds


def print_n(n):
  for a in range(n):
    print

def print_welcome():
  print ("{0:^50}".format('__________________________________________________'))
  print ("{0:^50}".format('Servus beim original Glupperlrechner'))
  print ("{0:^50}".format('-'))
  print ("{0:^50}".format('Der neusten Errungeschaft des Brotzeitbrettlzelts'))
  print ("{0:^50}".format('__________________________________________________'))

def modify_for_fritz():
  print
  print "Fritz nähert sich...gleich ist er do..."
  play_fritzm = input("Willst du seine Bestellung annehmen? ('yes','no')")
  print
  if play_fritzm == 'no':
    print 'Ok...'
  if play_fritzm == 'yes':
    freq_tot = 0
    for i in range(int(0.5*len(glupperlarr))):
      freq_tot += glupperlarr[1+2*i][0]
    glupperlarr.append('Schnauzer')
    glupperlarr.append([freq_tot,3])
    print 'Vui Spaß ;)'


class Singleplayer:

  def __init__(self,my_difficulty):
    self.diff = my_difficulty
  
  def params_order(self):  
    if self.diff == 's':
      n_glupperl = np.random.randint(2,5)
      is_bedienung = 'False'
      n_doppelseitig = 0.
    if self.diff == 'm':
      n_glupperl = np.random.randint(5,10)
      bed = np.random.rand(1)
      if bed>0.5:
        is_bedienung = 'True'
      else:
        is_bedienung = 'False'
      n_doppelseitig = 0.
    if self.diff == 'h':
      n_glupperl = np.random.randint(5,15)
      bed = np.random.rand(1)
      if bed>0.5:
        is_bedienung = 'True'
      else:
        is_bedienung = 'False'
      n_doppelseitig = np.random.randint(1,int(n_glupperl/2))
    if self.diff == 'fritz_mode':
      n_glupperl = np.random.randint(20,30)
      is_bedienung = 'False'
      n_doppelseitig = np.random.randint(1,int(n_glupperl/2))
      
    return n_glupperl, is_bedienung, n_doppelseitig
  
  # calculates price of randomly generated order 
  def calc_price(self,n_glupperl,is_bedienung,n_doppelseitig):
    sortiment = get_bounds()
    glupperl_names = []
    glupperl_prices = []
    price_tot = 0
    rand = sortiment[0]*np.random.rand(n_glupperl)
    for b,c in enumerate(rand):
      for i,j in enumerate(sortiment[1]):
        if (c>j):
          i += 1
        else:
          break
      glupperl_names.append(glupperlarr[2*i])
      price = glupperlarr[2*i+1][1]
      if is_bedienung == 'True':
        price-=0.5
      glupperl_prices.append(price)
      # This is the raw price without any extras.
      price_tot += glupperlarr[2*i+1][1]
    
    # Take care of price adjustments
    if is_bedienung == 'True':
      price_tot -= 0.5*n_glupperl
    price_tot += 1.0*n_doppelseitig
    if self.diff == 'fritz_mode':
      price_tot *= .9
      price_tot = int(price_tot / 5.)*5
          
    return price_tot, glupperl_names, glupperl_prices
    
  ## Phrase order to be printed to console
  # Standard beginning. For few glupperl we may print a variant of this beginning.
  def phrase_order(self,n_glupperl,is_bedienung,n_doppelseitig):

    if is_bedienung == 'True':
      beertents = [' vom Hacker', ' von da Fischer Vroni', ' vom Marstall', ' ausm Löwenbräu',' zu füllen']
    my_glupperl_names = self.calc_price(n_glupperl,is_bedienung,n_doppelseitig)
        
    order_start = 'Servus, i hätt gern folgende Glupperl:'
    if (n_glupperl >2 and n_glupperl < 7) and (np.random.rand(1) > 0.8):
      order_start = 'Servus, i hob a Großbestellung:'
      
    if is_bedienung == 'True':    
      rand_beertents = (len(beertents)-1)*np.random.rand(1)
      for b,c in enumerate(beertents):
        if (rand_beertents>b+1):
          b+=1
        else:
          tent = beertents[b]
          break
      opt_bedienung = 'I bin' +tent + '! '
    else:
      opt_bedienung = ''
  
    # Randomly choose which pegs get a two sided engraving 
    order_designs = []
    two_sided_pos = []
    opt_doppel = []
    val_before = 0
    for b in range(n_glupperl):
        opt_doppel.append('')
 
    if n_doppelseitig > 0:
      for b in range(n_doppelseitig):
        val = val_before + max(1,np.random.randint(n_glupperl-(n_doppelseitig-b )-val_before)-1)
        two_sided_pos.append(val)
        val_before = val
   
      for b in two_sided_pos:
        opt_doppel[b] = ' (doppelseitig)'
        my_glupperl_names[2][b] += 1
            
    for b,c in enumerate (my_glupperl_names[1]):
      #print c+opt_doppel[b]
      order_designs.append(c+opt_doppel[b])
      
    return order_start, opt_bedienung, order_designs, my_glupperl_names[0], my_glupperl_names[2]
    
  
  ## Play the game and print out the result
  def play_game(self,n_glupperl,is_bedienung,n_doppelseitig):
    
    fritz = 'False'
    phrasing = self.phrase_order(n_glupperl,is_bedienung,n_doppelseitig)    
    print_n(3)

    # Print out phrasing of order
    print phrasing[0] 
    for b in range(n_glupperl):
      print phrasing[2][b]
    if self.diff != 'fritz_mode':
      print phrasing[1] + 'Vui Spaß beim zamrechnen ;)'
    if self.diff == 'fritz_mode':
      print 'Da Chef macht mir doch sicher an guadn Preis'
      print 'Chef (zu Fritz): Logo, mach ma 10% Skonto.'
      print 'Chef (zu dir): ... Und rund noch auf an nächsten 5er ab.' 
    
    print_n(2)
    
    # Player enters order. Check if its correct and print according message.
    # If hard mode is on fritz is set to 'True'
    time_start = timeit.default_timer()
    guess = input('Ergebnis eintippen')
    time_end = timeit.default_timer()
    float_player_time = round(time_end - time_start,2)
    player_time = str(round(time_end - time_start,2))
    player_time_per = str(round((time_end - time_start)/n_glupperl,2))

    # Correct result
    if guess == phrasing[3]:

      if self.diff != 'fritz_mode':
        print 'Perfekt, ois richtig!'
        print 'Benötigte Zeit: '+player_time + ' Sekunden  (~' + player_time_per +' Sekunden pro Glupperl).'
        if self.diff != 'h':
          return 0
        if self.diff == 'h':
          fritz = 'True' 
          return fritz

      if self.diff == 'fritz_mode':
        print 'Du bist da Wahnsinn! Merci :)'
        print 'Benötigte Zeit: '+player_time + ' Sekunden  (~' + player_time_per +' Sekunden pro Glupperl).'
        return 0
     
    # Incorrect result --> Print detailed calculation to console   
    if guess > phrasing[3]:
      print 'Wuist mi aussackin?!'
    if guess < phrasing[3]:
      print 'Schenken mussts mia fei ned ;)'

    if guess != phrasing[3]:
      price=np.zeros(n_glupperl)
      print_n(2)
      print 'Hier die Aufschlüsselung:'
      for a,b in enumerate(phrasing[2]):
        price[a]=phrasing[4][a]
        print b + ' --> ' + str(price[a]) + ' Euro'
      print_n(2)  
      if self.diff != 'fritz_mode':
        print 'Das macht in der Summe ' + str(phrasing[3]) + ' Euro.'
      if self.diff == 'fritz_mode':
        print 'Abzüglich des 10% Rabatts und des Abrundens macht das ' + str(phrasing[3]) + ' Euro.'
      return 0
       
  

  
class Multiplayer:
  
  def __init__(self,my_difficulty,my_n_players):
    self.diff = my_difficulty
    self.n_players = my_n_players
  
  def params_order(self):  
    if self.diff == 's':
      n_glupperl = np.random.randint(2,5)
      is_bedienung = 'False'
      n_doppelseitig = 0.
    if self.diff == 'm':
      n_glupperl = np.random.randint(5,10)
      bed = np.random.rand(1)
      if bed>0.5:
        is_bedienung = 'True'
      else:
        is_bedienung = 'False'
      n_doppelseitig = 0.
    if self.diff == 'h':
      n_glupperl = np.random.randint(5,15)
      bed = np.random.rand(1)
      if bed>0.5:
        is_bedienung = 'True'
      else:
        is_bedienung = 'False'
      n_doppelseitig = np.random.randint(1,int(n_glupperl/2))
      
    return n_glupperl, is_bedienung, n_doppelseitig
  
  # calculates prices for all players  
  def calc_prices(self,n_glupperl,is_bedienung,n_doppelseitig):
    prices = []
    all_glupperl_names = []
    sortiment = get_bounds()
    for a in range(self.n_players):
      print 
      player_glupperl_names = []
      price_tot = 0
      rand = sortiment[0]*np.random.rand(n_glupperl)
      for b,c in enumerate(rand):
        for i,j in enumerate(sortiment[1]):
          if (c>j):
            i += 1
          else:
            break
        player_glupperl_names.append(glupperlarr[2*i])
        # This is the raw price without any extras.
        price_tot += glupperlarr[2*i+1][1]
    
      # Take care of price adjustments
      if is_bedienung == 'True':
        price_tot -= 0.5*n_glupperl
      price_tot += 1.0*n_doppelseitig
      
      prices.append(price_tot)
      all_glupperl_names.append(player_glupperl_names)
      
    return prices, all_glupperl_names
    
  ## Phrase order to be printed to console
  # Standard beginning. For few glupperl we may print a variant of this beginning.
  def phrase_orders(self,n_glupperl,is_bedienung,n_doppelseitig):

    all_order_start = []
    all_opt_bedienung = []
    all_order_designs = []
    if is_bedienung == 'True':
      beertents = [' vom Hacker', ' von da Fischer Vroni', ' vom Marstall', ' ausm Löwenbräu',' zu füllen']
    my_glupperl_names = self.calc_prices(n_glupperl,is_bedienung,n_doppelseitig)
        
    for a in range(self.n_players):
      order_start = 'Servus, i hätt gern folgende Glupperl:'
      if (n_glupperl >2 and n_glupperl < 7) and (np.random.rand(1) > 0.8):
        order_start = 'Servus, i hob a Großbestellung:'
      
      if is_bedienung == 'True':    
        rand_beertents = (len(beertents)-1)*np.random.rand(1)
        for b,c in enumerate(beertents):
          if (rand_beertents>b+1):
            b+=1
          else:
            tent = beertents[b]
            break
        opt_bedienung = 'I bin' +tent + '! '
      else:
        opt_bedienung = ''
  
      # Randomly choose which pegs get a two sided engraving 
      order_designs = []
      two_sided_pos = []
      opt_doppel = []
      val_before = 0
      for b in range(n_glupperl):
        opt_doppel.append('')
 
      if n_doppelseitig > 0:
        for b in range(n_doppelseitig):
          val = val_before + max(1,np.random.randint(n_glupperl-(n_doppelseitig-b )-val_before)-1)
          two_sided_pos.append(val)
          val_before = val
   
        for b in two_sided_pos:
          opt_doppel[b] = ' (doppelseitig)'
            
      for b,c in enumerate (my_glupperl_names[1][a]):
        #print c+opt_doppel[b]
        order_designs.append(c+opt_doppel[b])
        
      all_order_start.append(order_start)
      all_opt_bedienung.append(opt_bedienung)
      all_order_designs.append(order_designs)
      
    return all_order_start, all_opt_bedienung, all_order_designs, my_glupperl_names[0]
    
  
  ## Play the game for n players and print out the result
  def play_game(self,n_glupperl,is_bedienung,n_doppelseitig):
    
    phrasing = self.phrase_orders(n_glupperl,is_bedienung,n_doppelseitig)
    #prices = self.calc_prices(n_glupperl,is_bedienung,n_doppelseitig)
    times = [None]*self.n_players
    winners = []
    truewinners = []
    all_true = 'True'
    all_false = 'True'
    
    # Play game for each player. Store if correct result given and the time needed. Correct results stored in separate array.
    for a in range(self.n_players):
      print_n(2)
      print 'Get ready...'
      print
      time.sleep(5.0)
      print phrasing[0][a]
      print 
      for b in range(n_glupperl):
        print phrasing[2][a][b]
      print 
      print phrasing[1][a] + 'Vui Spaß beim zamrechnen ;)'
      print
      time_start = timeit.default_timer()
      guess = input('Ergebnis eintippen')
      time_end = timeit.default_timer()
      float_player_time = round(time_end - time_start,2)
      player_time = str(round(time_end - time_start,2))
      player_time_per = str(round((time_end - time_start)/n_glupperl,2))
      if guess == phrasing[3][a]:
        all_false = 'False'
        correct = 'True'
      else:
        correct = 'False'
        all_true = 'False'
      winners.append([a,correct,player_time,player_time_per])
      if correct == 'True':
        truewinners.append([a,correct,float_player_time,player_time,player_time_per])

    # Sort correct results by time   
    truewinners = sorted(truewinners, key=lambda x: x[2])
    
    # Print out results
    print_n(2)
    if (all_true == 'True'):
      print 'Super Leistung, ois richtig!'
      time.sleep(2.0)
      print_n(2)
      print 'Hier sind die Ergebnisse:'
      for a in range(len(truewinners)):
        print 'Platz %i: Spieler %i mit %s Sekunden (~ %s Sekunden pro Glupperl)'%(a+1, truewinners[a][0]+1, str(truewinners[a][3]), str(truewinners[a][4]))
      return 0
      
    if all_false == 'True':
      print 'Ois falsch...des wa joa gar nix...spuid hier Yan-Yan?'
      return 0
    
    else:
      print 'Des woar teilweise ganz guad!'
      time.sleep(2.0)
      print_n(2)
      print 'Hier sind die Egebnisse:'
      for a in range(len(truewinners)):
        print 'Platz %i: Spieler %i mit %s Sekunden (~ %s Sekunden pro Glupperl)'%(a+1, truewinners[a][0]+1, str(truewinners[a][3]), str(truewinners[a][4]))
      print_n(2)
      print 'Da Rest hats leider foisch gmachd...'
      return 0
      
      
      
def main():
  print_welcome()
  print_n(3)
  
  mode = input("Spielmodus wählen (Singleplayer: 's', Multiplayer: 'm')")
  if mode == 'm':
    n_players = input("Wie viele Spieler? (Zahl eintippen, z.B. 2)")
  diff = input("Schwierigkeitsgrad wählen (simple: 's', medium: 'm', hard: 'h')")
  print_n(3)

  if mode == 's':
    Game = Singleplayer(diff)
    order_params = Game.params_order()
    free_fritz=Game.play_game(order_params[0], order_params[1], order_params[2])
    if free_fritz == 'True':
      modify_for_fritz()
      NewGame = Singleplayer('fritz_mode')
      order_params = NewGame.params_order()
      NewGame.play_game(order_params[0], order_params[1], order_params[2])
  
  if mode == 'm':
    Game = Multiplayer(diff,n_players)
    order_params = Game.params_order()
    Game.play_game(order_params[0], order_params[1], order_params[2])

main()