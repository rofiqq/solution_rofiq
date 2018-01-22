# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:44:42 2018

@author: ainurrofiq
"""

# Matching String
from difflib import SequenceMatcher
import sys

class Score(object):
    def __init__ (self, input_kota, input_penghasilan, input_umur,
                  input_kelamin, input_pekerjaan, input_tinggal,
                  input_hutang):
        self.input_kota = input_kota
        self.input_penghasilan = input_penghasilan
        self.input_umur = input_umur
        self.input_kelamin = input_kelamin
        self.input_pekerjaan = input_pekerjaan
        self.input_tinggal = input_tinggal
        self.input_hutang = input_hutang

    def kota (self):
        if self.input_kota in ['Jakarta' , 'Bogor' , \
                                'Depok' , 'Tangerang' , 'Bekasi']:
            return 10
        elif self.input_kota == 'Surabaya':
            return 5
        else:
            return 2
    
    def penghasilan (self):
        if self.input_penghasilan <= 3000000 :
            return 3
        elif self.input_penghasilan > 3000000 and \
        self.input_penghasilan <= 6000000 :
            return 8
        elif self.input_penghasilan > 6000000:
            return 12
    
    def umur (self):
        if self.input_umur < 21 :
            return 0
        elif self.input_umur >= 21 and self.input_umur <= 40 :
            if self.input_kelamin == 'Wanita' and \
            (self.input_umur >= 22 and self.input_umur <=25):
                return 15
            else:
                return 10
        elif self.input_umur > 40 and self.input_umur <= 65 :
            return 12
        elif self.input_umur > 65:
            return 0
        
    def kelamin (self):
        if self.input_kelamin == 'Wanita':
            return 5
        elif self.input_kelamin == 'Pria':
            return 3
    
    def pekerjaan (self):
        if self.input_pekerjaan == 'Pegawai Swasta':
            return 8
        if self.input_pekerjaan == 'Wiraswasta':
            return 4
        if self.input_pekerjaan == 'Ibu Rumah Tangga':
            return 6
        else:
            return 0
        
    def tinggal (self):
        if self.input_tinggal == 'Milik Sendiri':
            return 15
        if self.input_tinggal == 'Kontrak':
            return 10
        if self.input_tinggal == 'Kost':
            return 5
        
    def hutang (self):
        if self.input_hutang == 0:
            return 0
        if self.input_hutang > 0  and self.input_hutang <= 5000000:
            return -5
        if self.input_hutang > 5000000 :
            return -15

class Data(object):
    def __init__(self,data):
        self.data = data
    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    def FixedData(self):
        inp = open(self.data,'r')
        inp = inp.read().split('\n')
        ListKota = ['Jakarta' , 'Bogor' ,'Depok' , 'Tangerang' , 'Bekasi', 'Surabaya']
        ListKelamin = ['Pria', 'Wanita']
        ListTinggal = ['Milik Sendiri', 'Kontrak', 'Kost'] 
        ListPekerjaan = ['Pegawai Swasta', 'Wiraswasta', 'Ibu Rumah Tangga']
        AllData=[]
        for i in range(len(inp)):
            input_data=inp[i].split('|')
            if inp[i].split('|') != [''] and len(inp[i].split('|')) == 8:
                # assume empty int data is zero (0)
                if input_data[2] == '':
                    input_data[2] = 0
                else:
                    input_data[2] = int(input_data[2])
                    
                if input_data[3] == '':
                    input_data[3] = 0
                else:
                    input_data[3] = int(input_data[3])
                    
                if input_data[7] == '':
                    input_data[7] = 0   
                else:
                    input_data[7] = int(input_data[7])
                # string matching (avoid typo)
                # if there is no similarity value more than 0.8, variable means other

                lskt , lspk = [] , []      
                for p in ListKota :
                    lskt.append(self.similar(input_data[1],p))
                if max(lskt)>=0.8:
                    input_data[1] = ListKota[lskt.index(max(lskt))]
                else:
                    input_data[1] = 'Other'
                    
                for r in ListPekerjaan :
                    lspk.append(self.similar(input_data[5],r))
                if max(lspk)>=0.8:
                    input_data[5] = ListPekerjaan[lspk.index(max(lspk))]
                else:
                    input_data[5] = 'Other'
                        
                # variable is chosen based on relative similarity value (because fix list)
                lstg , lskl = [] , []      
                for s in ListTinggal :
                    lstg.append(self.similar(input_data[6],s))
                    
                for q in ListKelamin :
                    lskl.append(self.similar(input_data[4],q))
                    
                input_data[6] = ListTinggal[lstg.index(max(lstg))]
                input_data[4] = ListKelamin[lskl.index(max(lskl))]
                
                AllData.append(input_data)
            elif inp[i].split('|') != [''] and len(inp[i].split('|')) < 8:
                AllData.append(input_data)
        return AllData


class Error(Exception):
    pass
class ArgumentError(Error):
    pass
class CommandError(Error):
    pass
    
try :
    if len(sys.argv)!= 3 :
        raise ArgumentError,'Solution needs 3 arguments instead {:}'\
        .format(len(sys.argv))
    else:
        if sys.argv[1] not in ['--file','--f']:
            raise CommandError, 'Use "--file" instead "{:}"'.format(sys.argv[1])
        else:
            alldata=Data(sys.argv[2]).FixedData()
            output = '{:12}{:}\n'.format('NAMA','TOTAL SCORE')
            for i in range(len(alldata)):
                if len(alldata[i]) == 8:
                    score=Score(alldata[i][1],alldata[i][2],alldata[i][3],alldata[i][4],
                                alldata[i][5],alldata[i][6],alldata[i][7])
                                    
                    TotalScore = score.kota()+score.penghasilan()+ \
                    score.umur()+score.kelamin()+score.pekerjaan()+ \
                    score.tinggal()+score.hutang()
                    output+='{:16}{:3d}\n'.format(alldata[i][0],TotalScore )
                    
                else :
                    output+='{:12}{:>13}\n'.format(alldata[i][0],'Data Kurang!' )
            f = open('output.txt','w')
            f.write(output)
            f.close() 
except ArgumentError as e:
    print "\nARGUMENT error : {:}\n".format(e)
    
except CommandError as e:
    print "\nARGUMENT error : {:}\n".format(e)
    
except IOError as e:
    print "\nI/O error : '{:}' is not in directory\n".format(e.filename)
