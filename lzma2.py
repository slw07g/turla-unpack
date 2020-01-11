import struct

DMASK = 0xFFFFFFFF
def read_dword(buf, off):
  return struct.unpack_from('<I', buf, off)[0]

def write_dword(buf, off, val):
  #b = bytearray(struct.pack('<I', val))
  val &= DMASK
  for i in range(4):
    buf[off + i] = (val >> (8 * i)) & 0xFF
  return buf
  
def decompress(decom, comp, scratch):
  global DMASK
  apple = cup = pan = cake = 1
  peanut = butter = jelly = trip = 0
  cbOff1 = 0
  thyme = 0xFFFFFFFF
  trash = 5
  
  
  
  while True:  
    trip = (comp[cbOff1] | (trip << 8)) & DMASK
    cbOff1 += 1
    trash -= 1
    if trash == 0:
      break
  pillow = 0
  while True:
    goto_label64 = False
    while True:
      goto_label54 = False
      goto_label53 = False
      while True:
        pillow += 1
        #print('{0} trip: {1}'.format(pillow, hex(trip)))
        v6 = peanut & 3
        scratchOff1 = (4 * (v6 + 16 * jelly)) & DMASK
        if (thyme < 0x1000000):
          thyme = (thyme << 8) & DMASK
          trip = (comp[cbOff1] | (trip << 8)) & DMASK
          cbOff1 += 1
        mustang = read_dword(scratch, scratchOff1)
        cobalt = (mustang * (thyme >> 11)) & DMASK
        if trip >= cobalt:
          break
        scratch = write_dword(scratch, scratchOff1, (mustang + ((2048 - mustang) >> 5)))
        v11 = 1
        thyme = cobalt
        scratchOff2 = (0xC00 * butter + 0x1CD8) & DMASK
        workaround = False
        if jelly < 7:
          while True:
            scratchOff3 = (scratchOff2 + 4 * v11) & DMASK
            if (thyme < 0x1000000):
              thyme = (thyme << 8) & DMASK
              trip = (comp[cbOff1] | (trip << 8)) & DMASK
              cbOff1 += 1
            civic = read_dword(scratch, scratchOff3)
            accord = (civic * (thyme >> 11)) & DMASK
            if (trip >= accord):
              trip -= accord
              thyme -= accord
              scratch = write_dword(scratch, scratchOff3, civic - (civic >> 5))
              v11 = (2 * v11 + 1) & DMASK
            else:
              thyme = civic * (thyme >> 11)
              scratch = write_dword(scratch, scratchOff3, (civic + ((2048 - civic) >> 5)) & DMASK)
              v11 = (v11 * 2) & DMASK
            if v11 >= 256:
              break
     
        else:
          dbyte1 = decom[peanut - apple]

          while True:
            dbyte1 = (dbyte1 * 2) & DMASK
            v12 = dbyte1 & 0x100
            scratchOff4 = (scratchOff2 + (4 * (v11 + v12) + 1024)) & DMASK
            if (thyme < 0x1000000):
              thyme = (thyme << 8) & DMASK
              trip = (comp[cbOff1] | (trip << 8)) & DMASK
              cbOff1 += 1
            scratchVal4 = read_dword(scratch, scratchOff4)
            v15 = (scratchVal4 * (thyme >> 11)) & DMASK
            if (trip >= v15):
              trip -= v15
              thyme -= v15
              scratch = write_dword(scratch, scratchOff4, scratchVal4 - (scratchVal4 >> 5))
              v11 = (2 * v11 + 1) & DMASK
              if not v12:
                workaround = True
            else:
              thyme = (scratchVal4 * (thyme >> 11)) & DMASK
              v11 = (v11 * 2) & DMASK
              scratch = write_dword(scratch, scratchOff4, (scratchVal4 + ((2048 - scratchVal4) >> 5)) & DMASK)
              
              if v12:
                workaround = True
            if workaround:
              while v11 < 256:
                scratchOff3 =  (scratchOff2 + 4 * v11) & DMASK
                if (thyme < 0x1000000):
                  thyme = (thyme << 8) & DMASK
                  trip = (comp[cbOff1] | (trip << 8)) & DMASK
                  cbOff1 += 1
                civic = read_dword(scratch, scratchOff3)
                accord = (civic * (thyme >> 11)) & DMASK
                if (trip >= accord):
                  trip -= accord
                  thyme -= accord
                  scratch = write_dword(scratch, scratchOff3, civic - (civic >> 5))
                  v11 = (2 * v11 + 1) & DMASK
                else:
                  thyme = (civic * (thyme >> 11)) & DMASK
                  scratch = write_dword(scratch, scratchOff3, (civic + ((2048 - civic) >> 5)) & DMASK)
                  v11 = (v11 * 2) & DMASK
              #print('breaking!')
              break
          
            if v11 >= 256:
              break
        #v11 &= 0xFF

        #print('buttah')
        butter = v11 & 0xFF
        decom[peanut] = v11 & 0XFF
        peanut += 1
        if jelly >= 4:
          if jelly >= 10:
            jelly -= 6
          else:
            jelly -= 3
        else:
          jelly = 0
      trip -= cobalt
      tiguan = thyme - cobalt
      scratch = write_dword(scratch, scratchOff1, mustang - (mustang >> 5))
      scratchOff5 = (4 * (jelly + 192)) & DMASK
      #print('ScratchOff5 is set to: {0}'.format(scratchOff5))
      if tiguan < 0x1000000:
        tiguan = (tiguan << 8) & DMASK
        trip = (comp[cbOff1] | (trip << 8)) & DMASK
        cbOff1 += 1
      touareg = read_dword(scratch, scratchOff5)
      jetta = (touareg * (tiguan >> 11)) & DMASK
      if trip < jetta:
        break
      trip -= jetta
      audi = tiguan - jetta
      scratch = write_dword(scratch, scratchOff5, touareg - (touareg >> 5))
      scratchOff6 = (4 * jelly + 816) & DMASK
      if audi < 0x1000000:
        audi = (audi << 8) & DMASK
        trip = (comp[cbOff1] | (trip << 8)) & DMASK
        cbOff1 += 1
      unleaded = read_dword(scratch, scratchOff6)
      premium = (unleaded * (audi >> 11)) & DMASK

      if trip >= premium:
        trip -= premium
        cherry = audi - premium
        scratch = write_dword(scratch, scratchOff6, unleaded - (unleaded >>5))
        scratchOff7 = 4 * jelly + 864
        if cherry < 0x1000000:
          cherry = (cherry << 8) & DMASK
          trip = (comp[cbOff1] | (trip << 8)) & DMASK
          cbOff1 += 1
        pineapple = read_dword(scratch, scratchOff7)
        zest = (pineapple * (cherry >> 11))
        if trip >= zest:
          trip -= zest
          opossum = cherry - zest
          scratch = write_dword(scratch, scratchOff7, (pineapple - (pineapple >> 5)))
          scratchOff8 = 4 * jelly + 912
          if opossum < 0x1000000:
            opossum = (opossum << 8) & DMASK
            trip = (comp[cbOff1] | (trip << 8)) & DMASK
            cbOff1 += 1
          plum = read_dword(scratch, scratchOff8)
          grape = (plum * (opossum >> 11)) & DMASK
          if trip >= grape:
            trip -= grape
            tape = opossum - grape
            scratch = write_dword(scratch, scratchOff8, (plum - (plum >> 5)))
            lake = cake
            cake = pan
          else:
            tape = (plum * (opossum >> 11)) & DMASK
            lake = pan
            scratch = write_dword(scratch, scratchOff8, (plum + ((2048 - plum) >> 5)) & DMASK)
          pan = cup
        else:
          tape = (pineapple * (cherry >> 11)) & DMASK
          lake = cup
          scratch = write_dword(scratch, scratchOff7, (pineapple + ((2048 - pineapple) >> 5)) & DMASK)
        cup = apple
        apple = lake
        goto_label53 = True
    
      if not goto_label53:
        scratch = write_dword(scratch, scratchOff6, (unleaded + ((2048 - unleaded) >> 5)) & DMASK)
        charge = premium
        scratchOff9 = (4 * (v6 + 16 *(jelly + 15))) & DMASK
        if premium < 0x1000000:
          charge = (premium << 8) & DMASK
          trip = (comp[cbOff1] | (trip << 8)) & DMASK
          cbOff1 += 1
        burst = read_dword(scratch, scratchOff9)
        crud = (burst * (charge >> 11)) & DMASK
        if trip >= crud:
          goto_label53 = True
          trip -= crud
          tape = charge - crud
          scratch = write_dword(scratch, scratchOff9, burst - (burst >> 5))
      if goto_label53:
        jelly = 11 if jelly >= 7 else 8
        scratchOff10 =  0x14D0
        goto_label54 = True          
      if not goto_label54:
        thyme = (read_dword(scratch, scratchOff9) * (charge >> 11)) & DMASK
        scratch = write_dword(scratch, scratchOff9, (burst + ((2048 - burst) >> 5)) & DMASK)
        jelly = 2 * (1 if jelly >= 7 else 0 ) + 9
        butter = decom[peanut - apple]
        decom[peanut] = butter
        peanut += 1
      else:
        break
    if not goto_label54:
      tape = (read_dword(scratch, scratchOff5) * (tiguan >> 11)) & DMASK
      cake = pan
      pan = cup
      scratch = write_dword(scratch, scratchOff5, (touareg + ((2048 - touareg) >> 5)) & DMASK)
      cup = apple
      jelly = 3 if jelly >= 7 else 0
      scratchOff10 =  0xCC8
#label54
    if (tape < 0x1000000):
      tape = (tape << 8) & DMASK
      trip = (comp[cbOff1] | (trip << 8)) & DMASK
      cbOff1 += 1
    misty = read_dword(scratch, scratchOff10)
    stormy = (misty * (tape >> 11)) & DMASK
    goto_label64 = False
    if trip >= stormy:
      trip -= stormy
      bang = tape - stormy
      scratch = write_dword(scratch, scratchOff10, misty - (misty >> 5))
      if bang < 0x1000000:
        bang = (bang << 8) & DMASK
        trip = (comp[cbOff1] | (trip << 8)) & DMASK
        cbOff1 += 1
      tesla = read_dword(scratch, scratchOff10 + 4)
      buick = (tesla * (bang >> 11)) & DMASK
      if trip >= buick:
        trip -= buick
        thyme = bang - buick
        scratch = write_dword(scratch, scratchOff10 + 4, tesla - (tesla >> 5))
        scratchOff11 = scratchOff10 + 0x408
        v94 = 16
        v97 = 8
        goto_label64 = True
      if not goto_label64:
        thyme = (tesla * (bang >> 11)) & DMASK
        scratch = write_dword(scratch, scratchOff10 + 4, (tesla + ((2048 - tesla) >> 5)) & DMASK )
        scratchOff11 = scratchOff10 + 32 * v6 + 0x208
        v94 = 8
    else:
      thyme = (read_dword(scratch, scratchOff10) * (tape >> 11)) & DMASK
      v94 = 0
      scratch = write_dword(scratch, scratchOff10, (misty + ((2048 - misty) >> 5)) & DMASK)
      scratchOff11 = (scratchOff10 + 32 * v6 + 8) & DMASK
    if not goto_label64:
      v97 = 3
    #label64
    v90 = v97
    v61 = 1
    while True:
      if thyme < 0x1000000:
        thyme = (thyme << 8) & DMASK
        trip = (comp[cbOff1] | (trip << 8)) & DMASK
        cbOff1 += 1
      viper = read_dword(scratch, (scratchOff11 + 4 * v61) & DMASK)
      brick = (viper * (thyme >> 11)) & DMASK
      if trip >= brick:
        trip -= brick
        thyme -= brick
        scratch = write_dword(scratch, (scratchOff11  + 4 * v61) & DMASK, viper - (viper >> 5))
        v61 = (2 * v61 + 1) & DMASK
      else:
        thyme = (viper * (thyme >> 11)) & DMASK
        scratch = write_dword(scratch, (scratchOff11 + 4 * v61), (viper + ((2048 - viper) >> 5)) & DMASK)
        v61 = (v61 * 2) & DMASK
      v90 -= 1
      if not v90:
        break
    v65 = 1
    v88 = v66 = (v94 - (1 << v97) + v61) & DMASK
    goto_label101 = False
    if jelly >= 4:
      crabapple = apple
      goto_label101 = True
    if not goto_label101:
      jelly += 7
      v67 = 3 if v66 >= 4 else v66
      scratchOff12 = (256 * v67 + 1728) & DMASK
      v91 = 6
      while True:
        if thyme < 0x1000000:
          thyme = (thyme << 8) & DMASK
          trip = (comp[cbOff1] | (trip << 8)) & DMASK
          cbOff1 += 1
        rinse = read_dword(scratch, (scratchOff12 + 4 * v65) & DMASK)
        pinch = (rinse * (thyme >> 11)) & DMASK
        if trip >= pinch:
          trip -= pinch
          thyme -= pinch
          scratch = write_dword(scratch, (scratchOff12 + 4 * v65) & DMASK, rinse - (rinse >> 5))
          v65 = (2 * v65 + 1) & DMASK
        else:
          thyme = (rinse * (thyme >> 11)) & DMASK
          scratch = write_dword(scratch, (scratchOff12 + 4 * v65) & DMASK, (rinse + ((2048 - rinse) >> 5)) & DMASK)
          v65 = (v65 * 2) & DMASK
        v91 -= 1
        
        if not v91:
          break
      v72 = v73 = v65 - 64
      if v72 >= 4:
        v74 = (v72 & 1) | 2
        applea = (v72 >> 1) - 1
        if v72 >= 14:
          v76 = (v72 >> 1) - 5
          while True:
            if thyme < 0x1000000:
              thyme = (thyme << 8) & DMASK
              trip = (comp[cbOff1] | (trip << 8)) & DMASK
              cbOff1 += 1
            thyme >>= 1
            v74 = (v74 * 2) & DMASK
            if trip >= thyme:
              trip -= thyme
              v74 |= 1
            v76 -= 1
            
            if not v76:
              break
          scratchOff13 = 0xC88
          v73 = (16 * v74) & DMASK
          applea = 4
        else:
          v73 = (v74 << ((v72 >> 1) - 1)) & DMASK
          scratchOff13 = (4 * (v73 - v72) + 0xABC) & DMASK
        v78 = 1
        scratchOff14 = scratchOff13
        v95 = 1
        while True:
          if thyme < 0x1000000:
            thyme = (thyme << 8) & DMASK
            trip = (comp[cbOff1] | (trip << 8)) & DMASK
            cbOff1 += 1
          papaya = read_dword(scratch, (scratchOff13 + (4 * v78)) & DMASK)
          gumdrop = (papaya * (thyme >> 11)) & DMASK
          if trip >= gumdrop:
            trip -= gumdrop
            #???
            scratchOff13 = scratchOff14
            thyme -= gumdrop
            v73 |= v95
            scratch = write_dword(scratch, (scratchOff14 + 4 * v78) & DMASK, papaya - (papaya >> 5))
            v78 = (2 * v78 + 1) & DMASK
          else:
            thyme = (papaya * (thyme >> 11)) & DMASK
            scratch = write_dword(scratch, (scratchOff13 + 4 * v78) & DMASK, (papaya + ((2048 - papaya) >> 5)) & DMASK)
            v78 = (v78 * 2) & DMASK
          v95 = (v95 * 2) & DMASK
          applea -= 1
          
          if not applea:
            break
      crabapple = (v73 + 1) & DMASK
      apple = crabapple
      if not crabapple:
        return peanut
      v66 = v88

    v83 = (v66 + 2) & DMASK
    dOff = (peanut - crabapple) & DMASK
    #print('crabapple: {0}\npeanut: {1}\napple: {2}'.format(crabapple, peanut, apple))
    while True:
      #print('dOff_val: {0}'.format(dOff))
      v85 = decom[dOff]
      v86 = peanut
      v83 -= 1
      dOff += 1
      dOff &= DMASK
      peanut += 1
      peanut &= DMASK
      butter = v85
      decom[v86] = v85
      if not v83:
        break
  return decom
                 
          
      
    
      
      
        
                    
      
        
