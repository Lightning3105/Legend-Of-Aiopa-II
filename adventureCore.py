#####
#The main core function/script file for the Legend Of Aiopa Text Adventure
#Most of the functions included in the game are here
#####

#####
#All Module Imports

#Core Import All
from lightCore import * #@UnusedWildImport
import player
import world
from Classes import *
#General Modules
#import time #@UnusedImport
#import random #@UnusedImport
#import easygui #@UnresolvedImport @UnusedImport
#import sys #@UnusedImport @Reimport
#import atexit #@UnusedImport

#End Module Imports
#####

#####
#Setup print and pprint
#####

def print(string):  # @DontTrace @ReservedAssignment
    #easygui print
    easygui.msgbox(msg=string, title=turns())

def pprint(pic, string):
    #easygui picture print
    easygui.msgbox(image=pic, msg=string, title=turns())

#####
#Pictures
#####
Full_Bag = "Images/Bag Full.png"
Fight_Symbol = "Images/Fight.png"
Coin = "Images/BronzeCoin.png"

#####
#PLAYER
#####

def player_damage(attacker, attackType, amount):
    #Deals damage to the player, displaying who did it
    print(attacker + " " + attackType + " " + player.Name + ". " + player.Name + " takes " + str(amount) + " damage")
    player.Health -= amount

    if player.Health < 1:
        player_die()

def player_die():
    #Displays the death message, and then returns you to your previous spot
    print("You collapse to the ground.")
    print("The world tumbles around you.")
    print("Your vision gets brighter and brighter, until...")
    #run(Last_Point)

def player_refresh():
    #Does a check of multiple player variables, checking if they make sense.
    if player.Health < 1:
        player_die()

    if player.Health > player.MaxHealth:
            player.Health = player.MaxHealth

    if player.Mana > player.MaxMana:
        player.Mana = player.MaxMana

    player.Health = int(player.Health)

def player_Xpa(xp):
    #Adds 'xp' XP to the players xp, checking if the player level can be increased
    player.Xp += xp
    while player.Xp > player.Xpn:
        if player.Xp > player.Xpn:
            player.Xpl += 1
            player.Xp -= player.Xpn
            player.Xpn *= 1.2
            player.Xpn = int(player.Xpn)

def player_defence():
    #Calculates the defence of a player
    TheOut = 0
    try:
        TheOut += int(player.Helmet.defence)
    except:
        TheOut += 0
    try:
        TheOut += int(player.Shirt.defence)
    except:
        TheOut += 0
    try:
        TheOut += int(player.Boots.defence)
    except:
        TheOut += 0

    return int(TheOut)

def player_speed():
    return player.Speed #TODO: Add together weights

def player_unEquip(item):
    #Unequips an item from the player
    debug("Un Equip")

    if item.type == "Helmet":
        inventory_add(player.Helmet)
        player.Helmet = None

    if item.type == "Shirt":
        inventory_add(player.Shirt)
        player.Shirt = ""

    if item.type == "Boots":
        inventory_add(player.Boots)
        player.Boots = None

def player_equip(item):
    #Equips an item to the player
    debug("equiping:")
    debug(item)
    debug(item.type)

    if item.type == "Helmet":
        if player.Helmet == None:
            player.Helmet = item
            inventory_remove(item)

        else:
            inventory_remove(item)
            inventory_add(player.Helmet)
            player.Helmet = item
        return

    if item.type == "Shirt":
        if player.Shirt == None:
            player.Shirt = item
            inventory_remove(item)

        else:
            inventory_remove(item)
            inventory_add(player.Shirt)
            player.Shirt = item
        return

    if item.type == "Boots":
        if player.Boots == None:
            player.Boots = item

            inventory_remove(item)

        else:
            inventory_remove(item)
            inventory_add(player.Boots)
            player.Boots = item
        return

    else:
        print("Cannot equip a " + str(item.name))

def battle(t):
    #Player attacks 'tgt'
    world.Turn += 1

    global tlife

    debug("ATTACKING")
    target = t.name

    weapons = []

    for i in player.InvContents:
        spl = i.type
        if spl == "Weapon":
            weapons.append(i)
    weapons.append(Weapon("Your Fists", "", "", player.Strength, 0, "", "Images/Fist01.png"))

    #pprint(Fight_Symbol, player.Name + " (" + str(player.Health) + ", " + str(player_defence()) + ")" + " Attacks " + target + " (" + str(tlife) + ", " + str(tdef) + ")" + "!")
    pprint(Fight_Symbol, player.Name + " (Level " + str(player.Xpl) + ")" + " Attacks " + str(target) + " (Level " + str(t.level) + ")" + "! Choose your weapon!")
    #att_weapon = easygui.choicebox(msg="Chose your weapon", choices=(weapons))
    patt = weaponselect(weapons)
    patt = int(patt + int(player.Strength / 2))

    #Calculate personality
    total = t.attack + t.defence + t.magic
    mgcp = int((t.magic / total) * 100)
    attp = int((t.attack / total) * 100) + mgcp
    defp = int((t.defence / total) * 100) + attp

    global tempdef
    global tartempdef

    tempdef = 0
    tartempdef = 0

    while True:
        debug("PATT " + str(patt))
        debug("TDEF " + str(t.defence))
        debug("PDEF " + str(player_defence() + tempdef))
        tlife = int(t.health)
        Pcrit = False
        Ecrit = False
        if t.speed + random.randint(-2, 2) > player.Speed + random.randint(-2, 2):
            order = "target"
        else:
            order = "player"
        debug(order)

        #NPC decide action
        rdn = random.randint(1, 100)
        if rdn <= attp:
            taction = "Attack"
        elif rdn <= defp:
            taction = "Defend"
        elif rdn <= mgcp:
            taction = "Magic"
        else:
            debug("npc ai error")
            debug("rdn: " + str(rdn))
            debug("defp: " + str(defp))
            debug("attp: " + str(attp))
            debug("mgcp: " + str(mgcp))

        des = easygui.buttonbox(msg="Your Turn!", choices=("Attack", "Defend", "Magic", "Retreat", "Change Weapon"))

        if order == "player":
            tempdef = 0
            PtE = int( patt * (1 + random.random())- (t.defence + tartempdef))
            if PtE < 0:
                PtE = 0
            if random.randint(0, 100) < player.Luck:
                if PtE == 0:
                    PtE = 1
                PtE = PtE * ((player.Luck + 10) / 10)
                Pcrit = True
            if player_attack(des, Pcrit, PtE, target, t, tartempdef) == "Retreat":
                return "retreat"
            t.health = tlife
            debug("tempdef" + str(tempdef))

            if tlife < 1:
                print("You defeat " + target + ".")
                pxp = int((int(t.level) + 1) * (random.randint(1, 3) + random.random()))
                print("you gain " + str(pxp) + " XP!")
                pka = int(int(t.level) * (random.randint(1, 2) + random.random()))
                player_Xpa(pka)
                if t.alignment == "G":
                    print(target + " was good. " + "You lose " + str(pka) + " karma")
                    debug("Pre karma: " + str(player.Karma))
                    player.Karma -= pka
                    debug("Post karma: " + str(player.Karma))
                if t.alignment == "E":
                    print(target + "was evil. " + "You gain " + str(pka) + " karma")
                    player.Karma += pka
                world.Places[world.Location].remove(t)
                return "win"
            tartempdef = 0
            EtP = int( int (t.attack) * (1 + random.random()) - (player_defence() + tempdef))
            debug("ETP " + str(EtP))
            debug("ETP without tempdef " + str(EtP + tempdef))

            if EtP < 0:
                EtP = 0
            if random.randint(0, 100) < t.luck:
                if EtP == 0:
                    EtP = 1
                EtP = EtP * ((t.luck + 10) / 10)
                Ecrit = True

            enemy_attack(taction, Ecrit, target, t.luck, EtP, t.defence, t.attack, tlife, t.maxhealth, t.magic, t.spells, tempdef)
            player_refresh()

        if order == "target":
            tartempdef = 0
            EtP = int( int (t.attack) * (1 + random.random()) - (player_defence() + tempdef))
            debug("ETP " + str(EtP))
            debug("ETP without tempdef " + str(EtP + tempdef))
            if EtP < 0:
                EtP = 0
            if random.randint(0, 100) < t.luck:
                if EtP == 0:
                    EtP = 1
                EtP = EtP * ((t.luck+ 10) / 10)
                Ecrit = True
            enemy_attack(taction, Ecrit, target, t.luck, EtP, t.defence, t.attack, tlife, t.maxhealth, t.magic, t.spells, tempdef)

            player_refresh()
            tempdef = 0
            PtE = int( patt * (1 + random.random())- (t.defence + tartempdef))

            if PtE < 0:
                PtE = 0
            if random.randint(0, 100) < player.Luck:
                if PtE == 0:
                    PtE = 1
                PtE = PtE * ((player.Luck + 10) / 10)
                Pcrit = True
            if player_attack(des, Pcrit, PtE, target, t, tartempdef) == "Retreat":
                return "retreat"

            t.health = tlife
            debug("tempdef" + str(tempdef))

            if tlife < 1:
                print("You defeat " + target + ".")
                pxp = int((int(t.level) + 1) * (random.randint(1, 3) + random.random()))
                print("you gain " + str(pxp) + " XP!")
                pka = int(int(t.level) * (random.randint(1, 2) + random.random()))
                player_Xpa(pka)
                if t.alignment == "Good":
                    print(target + " was good. " + "You lose " + str(pka) + " karma")
                    debug("Pre karma: " + str(player.Karma))
                    player.Karma -= pka
                    debug("Post karma: " + str(player.Karma))
                if t.alignment == "Evil":
                    print(target + "was evil. " + "You gain " + str(pka) + " karma")
                    player.Karma += pka
                world.Places[world.Location][0].remove(t)
                return "win"

def player_attack(des, Pcrit, PtE, target, tgt, tartempdef):
    global tempdef
    global tlife
    debug(tlife)
    tempstr = ""
    if tartempdef > 0:
        tempstr = " (" + str(tartempdef) + " extra defence)"

    if des == "Attack":
        print(player.Name + " Attacks!")
        if Pcrit == True:
            print("Critical Hit! x" + str(((player.Luck + 10) / 10)))
        print(player.Name + " Deals " + str(PtE) + " Damage To " + target + tempstr)
        tlife -= PtE #TODO update target health
        print(target + " Is Now On " + str(tlife) + " Health.")

    if des == "Defend":
        print(player.Name + " Is Defending.")
        tempdef = int(player.Strength / 2)
        debug("tempdef " + str(tempdef))
        #return int(player.Strength / 2)


    if des == "Magic":
        if not player.Spells == []:
            spl = easygui.choicebox(msg="Choose A Spell To Cast", title=turns(), choices=player.Spells)
            player_magicCast(spl)
        else:
            print("You have no spells")

    if des == "Retreat":
        world.Places[world.Location][0][lfind(world.Places[world.Location][0], tgt)][4]["hlt"] = tlife
        print(target + " watches you as you scamper away...")
        return "Retreat"

    if des == "Change Weapon":
        weapons = []
        wdamage = []
        wpics = []
        for i in range(0, len(player.InvContents)):
            spl = player.InvContents[i].type
            if spl == "weapon":
                weapons.append(player.InvContents[i].name)
                wdamage.append(player.InvContents[i].name)
                wpics.append(getpic(player.InvContents[i]))
        weapons.append("Your Fists")
        wdamage.append(player.Strength)
        wpics.append("Pics/Fist01.png")
        patt = weaponselect(weapons, wdamage, wpics)
        patt = int(patt + player.Strength)



def enemy_attack(taction, Ecrit, target, tlck, EtP, tdef, tatt, tlife, tmhlt, tmgc, tspl, tempdef):
    global tartempdef

    tempstr = ""
    if tempdef > 0:
        tempstr = " (" + str(tempdef) + " extra defence)"

    if taction == "Attack":
        print(target + " Attacks!")
        if Ecrit == True:
            print("Critical Hit! x" + str(((tlck + 10) / 10)))

        print(target + " Deals " + str(EtP) + " Damage To " + player.Name + tempstr)
        player.Health -= EtP
        print(player.Name + " Is Now On " + str(int(player.Health)) + " Health.")

    if taction == "Defend":
        print(target + " Is Defending.")
        tartempdef = int(tatt / 2)
        #return int(tatt / 2)

    if taction == "Magic":
        spell = target_magicCast(target, tlife, tmhlt, tmgc, tspl)
        if spell == "heal":
            amount = tmgc * random.randint(1, 2)
            print(target + "casts 'heal' and recovers " + str(amount) + " health")
            tlife += amount
            if tlife > tmhlt:
                tlife = tmhlt
            print(target + "is now on " + str(tlife) + " Health")

def player_magicCast(spell):
    if player.Spells.__contains__(spell) == False:
        return "No Spell"
    if spell == "heal":
        if player.Mana >= 3:
            player.Mana -= 3
            player_refresh()
            amount = player.Magic * random.randint(1, 2)
            print("You cast 'heal' recovering " + str(amount) + " health")
            player.Health += amount
            player_refresh()
            print("You now have " + str(player.Health) + " Health")
        else:
            print("You do not have enough Mana to cast the spell heal! You only have " + player.Mana + " Mana!")

def player_addMana():
    amount = player.Magic + int(player.Luck / 10)
    player.Mana += amount
    player_refresh()
#####
#END PLAYER
#####

def target_magicCast(name, tlife, tmlife, tmgc, tspl):
    if tspl.__contains__("heal") == True:
        if tlife < tmlife / 2:
            return "heal"

#####
#INVENTORY
#####

class oblist(list):
    def onremove(self, name):
        for i in self:
            debug(i.name)
            if i.name == name:
                debug("same")
                self.remove(i)
    def otremove(self, type):
        for i in self:
            debug(i.type)
            if i.type == type:
                debug("same")
                self.remove(i)

def inventory_add(item): #TODO multiple of a single item

    debug("ADD TO INVENTORY:")
    debug(player.InvContents)
    #This bit will have problems with lists of items due to the 1
    if 1 + len(player.InvContents) > player.InvSize:
        debug(player.InvSize)
        pprint(Full_Bag, "You can't fit anything else into a bag that can only hold " + str(player.InvSize) + " items!")

        INV_A_DC = easygui.choicebox(msg="What to drop: (cancel to not drop anything)", choices=(getnam(player.InvContents))) #TODO: re make getnam
        if not INV_A_DC == None:
            INV_A_DC = find_tup(INV_A_DC, player.InvContents)
            inventory_remove(INV_A_DC)
        if INV_A_DC == None:
            return False

    player.InvContents.append(item)
    return True




def inventory_get():
    debug("INVENTORY")
    player.InvContents = oblist(player.InvContents)
    ##Finding Money##
    for i in range(0, len(player.InvContents)):
        spl = player.InvContents[i].type
        if spl == "Money":
            debug(player.Money)
            amt = player.InvContents[i].amount
            amti = int(amt)
            type(amti)
            player.Money += amti
            del player.InvContents[i]
            debug(player.Money)
            break


    ##adding money string to inventory###
    player.InvContents.append(InventoryString("You Have: " + str(player.Money) + " Gold", "MoneyStr", "Your small bag of money full of coins that are known as 'gold' by the comoners"))

    ##done money##

    ##adding equipped items to inventory##

    player.InvContents.append(Equipped(player.Boots, "Boots"))
    player.InvContents.append(Equipped(player.Shirt, "Shirt"))
    player.InvContents.append(Equipped(player.Leggins, "Leggins"))
    player.InvContents.append(Equipped(player.Helmet, "Helmet"))

    ##adding player stats##

    player.InvContents.append(InventoryString("Your Statistics", "Stats"))

    ##showing inventory##

    selected = easygui.choicebox(msg = "Your Inventory:", choices=(getnam(player.InvContents)))

    selected = find_tup(selected, player.InvContents)

    player.InvContents.otremove("MoneyStr")  # @UndefinedVariable
    player.InvContents.onremove("Your Statistics") # @UndefinedVariable
    player.InvContents.otremove("Equiped " + "Boots") # @UndefinedVariable
    player.InvContents.otremove("Equiped " + "Shirt") # @UndefinedVariable
    player.InvContents.otremove("Equiped " + "Leggins") # @UndefinedVariable
    player.InvContents.otremove("Equiped " + "Helmet") # @UndefinedVariable

    player.InvContents.otremove("UnEquiped " + "Boots") # @UndefinedVariable
    player.InvContents.otremove("UnEquiped " + "Shirt") # @UndefinedVariable
    player.InvContents.otremove("UnEquiped " + "Leggins") # @UndefinedVariable
    player.InvContents.otremove("UnEquiped " + "Helmet") # @UndefinedVariable

    debug("\n selected:")
    debug(selected)

    if selected == None:
        return "exit"

    IgI = None
    verb = "Use"

    if type(selected) == list:
        selected = selected[0]


    if selected.type == "Stats": #STATS
        statistics()

    elif selected.type == "MoneyStr": #MONEY
        pprint(Coin, selected.description)

    elif selected.type.split(" ")[0] == "UnEquiped": #EQUIPPED ITEM
        #Is it an equipped item?
        IgI = easygui.buttonbox(msg=selected.description, choices=(["Back"]))

    elif selected.type.split(" ")[0] == "Equiped": #EQUIPPED ITEM
        #Is it an equipped item?
        IgI = easygui.buttonbox(image=getpic(selected), msg=selected.description, choices=("Back", "Un Equip"))
        if IgI == "Un Equip":
            player_unEquip(selected.item)

    elif selected.type in ["Shirt", "Helmet", "Leggins", "Boots"]: #EQUIPABLE
        #Is it an eqipable item?
        IgI = easygui.buttonbox(image=getpic(selected), msg=selected.description, choices=("Back", "Equip", "Discard"))
        if IgI == "Equip":
            player_equip(selected)
        if IgI == "Discard":
            inventory_remove(selected)

    elif selected.cat == "Item":
        IgI = easygui.buttonbox(image=getpic(selected), msg=selected.description, choices=("Back", "Discard"))
        if IgI == "Discard":
            inventory_remove(selected)

    """elif searchmet("u", selected): #USABLE
        if searchmet("book", selected) == True:
            verb = "Read"
        if searchmet("map", selected) == True:
            verb = "Read"
        IgI = easygui.buttonbox(image = getpic(selected), msg = getdes(selected), choices =("Back", verb, "Discard"))
    else:
        IgI = easygui.buttonbox(image=getpic(selected), msg=getdes(selected), choices=("Back", "Discard"))
    if IgI == "Discard":
        inventory_remove(selected)
    if IgI == verb:
        if getmet(selected, 0) == "book":
            read(selected)
        if getmet(selected, 0) == "map":
            read(selected)"""
        #other items


    inventory_get()
    return

def inventory_remove(item):
    world.Places[world.Location].append(item)
    player.InvContents.onremove(item.name) # @UndefinedVariable

#####
#END INVENTORY
#####

#####
#WORLD
#####

def turns():
    return world.TurnString + str(world.Turn)

def world_refresh():
    for i in world.Places[world.Location]:
        debug(i)
        if i.type == "Person":
            if i.health < 1:
                world.Places[world.Location].remove(i)

def var():
    return world.Variables

#####
#END WORLD
#####

def removeob(name, list):
    return [item for item in list if item.name != name]

def getnam(lis):
    debug(lis)
    debug(lis[0])
    debug(lis[0].__dict__)
    TheOut = []
    for i in lis:
        TheOut.append(i.name)
    return TheOut

def getpic(item):
    try:
        TheOut = "Images/" + item.image
        return TheOut
    except:
        return None

def input(string):  # @ReservedAssignment
    #Creates an enter box with a string, and the time as the title
    TheInput = easygui.enterbox(msg=string, title=turns())
    return TheInput

def options(pic, string, op1, op2, op3=None, op4=None):
    #creates an button box with 2, up to 4 choices
    if not op4 == None:
        TheOut = easygui.buttonbox(choices=(op1, op2, op3, op4, "Inventory"), msg=string, image=pic, title=turns())
    if op4 == None:
        TheOut = easygui.buttonbox(choices=(op1, op2, op3, "Inventory"), msg=string, image=pic, title=turns())
    if op4 and op3 == None:
        TheOut = easygui.buttonbox(choices=(op1, op2, "Inventory"), msg=string, image=pic, title=turns())

    if TheOut == "Inventory":
        inventory_get()
        TheOut = options(pic, string, op1, op2, op3, op4)

    return TheOut

def move(choices):
    world.Turn += 1
    #Shows a choicebox with places that the player can move to
    #returns the selection

    choices = [i for i in choices if i.type == "Place"]

    TheOut = easygui.choicebox(msg="Move To:", choices=(t(choices, 0)))

    TheOut = find_tup(TheOut, choices)

    debug(TheOut.Location)
    world.Location = TheOut.Location
    newPlace()

    return TheOut

def find_tup(item, lis):
    #gets a one or multiple string/s
    #item = the string/s
    #lis = the list it has to search through
    TheOut = []

    if type(item) == list:

        for i in range(0, len(item)):

            for t in range(0, len(lis)):

                if lis[t].name == item[i]:

                    TheOut.append(lis[t])
                    break
        return TheOut

    if type(item) == str:


        for t in range(0, len(lis)):

            if lis[t].name == item:

                TheOut = lis[t]

                return TheOut

def view(items, string="You Can See:"):
    #Creates a choicebox from a list
    #Can use a string, by default shows 'you can see:'

    while True:
        TheOut = ""
        str(TheOut)
        if len(items) == 0:
            items.append(InventoryString("Nothing Here", "None", "There is nothing to be seen here"))

        TheOut = easygui.choicebox(msg=string, choices=(getnam(items)), title=turns())

        if TheOut == None:
            return

        TheOut = find_tup(TheOut, items)

        if TheOut.cat == "Item":
            choice = easygui.buttonbox(image=getpic(TheOut), msg=TheOut.description, choices=("Take", "Back"))
        elif TheOut.cat == "Empty":
            choice = easygui.buttonbox(msg=TheOut.description, choices=["Back"])
        else:
            try:
                choice = easygui.buttonbox(image=getpic(TheOut), msg=TheOut.description, choices=("Back"))
            except:
                easygui.buttonbox(msg="Oh dear. " + TheOut.name + " doesn't seem to exist.", choices=("Back"))
                debug("ITEM ERROR")

        if choice == "Take":
            if inventory_add(TheOut) == True:
                world.Places[world.Location].remove(TheOut)
                world.Turn += 1
                return "Take"
        else:
            return

def take(choices, mmax=0, string="You Can Take:"):
    world.Turn += 1
    #Takes an item and places it into the players inventory
    #Returns the item
    debug("TAKING")

    choices = [i for i in choices if i.cat == "Item"]

    TheOut = easygui.multchoicebox(msg=string, choices=(t(choices, 0)))
    debug(TheOut)

    if TheOut == None:
        return

    if len(TheOut) > mmax:
        if not mmax == 0:
            print("You can only take " + mmax + " items.")
            return

    inventory_add(find_tup(TheOut, choices))
    return find_tup(TheOut, choices)

def read(item):
    world.Turn += 1
    book = item.contents
    book = "Books/" + book
    importVar(book)
    if item.type == "Book":
        print("Knowledge Acquired! " + item.knowlege + "!")
        player.Knowledge.append(item.knowlege)

def player_picture():
    pic1 = "Images/Player_1.png"
    pic2 = "Images/Player_2.png"
    pic3 = "Images/Player_3.png"
    pic4 = "Images/Player_4.png"

    picno = 1

    while True:
        if picno == 1:
            c = easygui.buttonbox(msg="What will you look like?", title="Character Creation", choices=("<---", "SELECT", "--->"), image=pic1)
            if c == "<---":
                picno = 4
            if c == "SELECT":
                player.Picture = pic1
                return
            if c == "--->":
                picno += 1
        if picno == 2:
            c = easygui.buttonbox(msg="What will you look like?", title="Character Creation", choices=("<---", "SELECT", "--->"), image=pic2)
            if c == "<---":
                picno -= 1
            if c == "SELECT":
                player.Picture = pic2
                return
            if c == "--->":
                picno += 1
                if picno > 4:
                    picno = 1
        if picno == 3:
            c = easygui.buttonbox(msg="What will you look like?", title="Character Creation", choices=("<---", "SELECT", "--->"), image=pic3)
            if c == "<---":
                picno -= 1
            if c == "SELECT":
                player.Picture = pic3
                return
            if c == "--->":
                picno += 1
                if picno > 4:
                    picno = 1
        if picno == 4:
            c = easygui.buttonbox(msg="What will you look like?", title="Character Creation", choices=("<---", "SELECT", "--->"), image=pic4)
            if c == "<---":
                picno -= 1
            if c == "SELECT":
                player.Picture = pic4
                return
            if c == "--->":
                picno += 1
                if picno > 4:
                    picno = 1

def player_name():
    player.Name = easygui.enterbox(msg="What will you be known as?", title="Character Creation", image=player.Picture)
    if player.Name == "":
        player.Name = "Person"
    return

def choices(things):
    player_refresh()
    world_refresh()
    while True:
        chs = ["Look Around", "Move Somewhere", "View Inventory"]
        for i in things:
            if i.type == "Person":
                chs.append("Interact With Something")
                break

        des = easygui.buttonbox(msg="What Will You Do?", title=turns(), choices=(chs))
        if des == "Look Around":
            view(things)
        if des == "Move Somewhere":
            move(things)
        if des == "View Inventory":
            inventory_get()
        if des == "Interact With Something":
            soth = []
            for i in things:
                if i.type == "Person":
                    soth.append(i)
            something = easygui.choicebox(msg="You can interact with...", title=turns(), choices=getnam(soth))
            something = find_tup(something, things)
            if something.type == "Person":
                des = easygui.buttonbox(msg="Interact With " + something.name, title=turns(), choices=("Talk", "Attack"))
                if des == "Talk":
                    talk(something)
                if des == "Attack":
                    debug("pre bat")
                    battle(something)
                    debug("post bat")

        if des == None:
            exit()

def newPlace():
    l = world.Places[world.Location]
    choices(l)




def selector(things, pictures, string, attribute, title):
    #insert %m in string to replace that with output from metno
    #insert %t in string to replace that with thing name
    items = []
    names = []
    nmax = len(things)
    for i in range(0, len(things)):
        item = things[i].name
        met = exec(things[i] + "." + attribute)
        line = string
        line.replace("%m", met)
        line.replace("%t", item)
        items.append(line)
        names.append(item)

    num = 0
    while True:

        out = easygui.buttonbox(msg=items[num], title=title, choices=("<---", "SELECT", "--->"), image=pictures[num])
        if out == "<---":
            num -= 1
            if num < 0:
                num = nmax
            if out == "SELECT":
                for i in names:
                    for t in things:
                        if getnam(t) == i[num]:
                            TheOut = t
                return TheOut
        if out == "--->":
            num += 1
            if num > nmax:
                num = 0

def weaponselect(weapons):
    nmax = len(weapons) - 1
    num = 0
    while True:
        string = str(weapons[num].name) + ": Does " + str(weapons[num].damage) +  " Damage."
        out = easygui.buttonbox(msg=string, title="Choose Your Weapon:", choices=("<---", "SELECT", "--->"), image=weapons[num].image)
        if out == "<---":
            num -= 1
            if num < 0:
                num = nmax
        if out == "SELECT":
            return int(weapons[num].damage)
        if out == "--->":
            num += 1
            if num > nmax:
                num = 0

def talk(person):
    world.Turn += 1
    dic = person[5]
    printTree(dic)
    #rdm = random.randint(1, len(dic))
    otn = []
    otndic = []
    for key in dic:
        if list(key)[0] == "O":
            otn.append(dic[key]["B"])
            otndic.append(dic[key])
    c = easygui.buttonbox(msg=dic["T"], title=turns(), choices=otn)

    for d in otndic:
        if d["B"] == c:
            cur = d

    while True:
        otn = []
        otndic = []
        end = False
        debug(cur)
        for key in cur:
            if list(key)[0] == "O":
                otn.append(cur[key]["B"])
                otndic.append(cur[key])

            if list(key)[0] == "R":
                exec(cur[key]["R"])

            if list(key)[0] == "E":
                if cur[key] == "E":
                    return
                if type(cur[key]) == list:
                    cur = reduce(lambda a, b: a[b], cur[key], dic)
                    end = True
        if end == False:
            if cur.get("T") == None:
                return
            if type(cur["T"]) == list:
                for i in cur["T"]:
                    c = easygui.buttonbox(msg=i, title=turns(), choices=otn)
            else:
                c = easygui.buttonbox(msg=cur["T"], title=turns(), choices=otn)

            for d in otndic:
                if d["B"] == c:
                    cur = d

def statistics():
    cur = 0
    items = ["Your Physical Attributes:" + "\nStrength: " + str(player.Strength) + "\nHealth: " + str(player.Health) + "/" + str(player.MaxHealth) + "\nSpeed: " + str(player.Speed) + "\nDefence: " + str(player_defence()),
             "Your Mental Attributes:" + "\nMagical Strength: " + str(player.Magic) + "\nMana: " + str(player.Mana) + "/" + str(player.MaxMana) + "\nKarma: " + str(player.Karma) + "\nLuck: " + str(player.Luck),
             "Your Spells:\n" + '\n'.join(player.Spells),
             "Your Knowledge:\n" + '\n'.join(player.Knowledge)]
    while True:
        debug(cur)
        choice = easygui.buttonbox(msg=items[cur], title=turns(), choices=("<---", "Back", "--->"), image=player.Picture)

        if choice == "<---":
            cur -= 1
        if choice == "--->":
            cur += 1
        if choice == "Back":
            return

        if cur > len(items) - 1:
            cur = 0
        if cur < 0:
            cur = len(items) - 1

def exit():  # @ReservedAssignment
    if easygui.ynbox(msg="Are You Sure You Want To Exit? The Game Will Save.") == True:
        #player.save()
        #inventory.save()
        #world.save()
        sys.exit()
