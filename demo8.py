# -*- coding: utf-8 -*-
import os
import codecs

def SplitMeasure(durations, cSumDurations):
    SumDur= 0
    measureGroup= []
    idxGroup=[]
    for noteIdx, duration in enumerate(durations):
        SumDur+= int(duration)
        idxGroup.append(noteIdx)
        if cSumDurations== SumDur:
            measureGroup.append(idxGroup)
            idxGroup=[]
            SumDur= 0
    return measureGroup

def RemoveStub(wkDir, stubType):
    stubPath= wkDir+stubType
    if os.path.exists(stubPath):
        os.remove(stubPath)
        return True
    return False

def SelectMusic(fInputMusic):
    chosenMusic= ''
    with open(fInputMusic, 'r') as inputMusic:
        chosenMusic= inputMusic.readline()
        chosenMusic= chosenMusic.strip('\n')
    return int(chosenMusic)
    
def SelectVoice(fInputVoice):
    chosenVoice= ''
    with open(fInputVoice, 'r') as inputVoice:
        chosenVoice= inputVoice.readline()
        chosenVoice= chosenVoice.strip('\n')
    return int(chosenVoice)

if __name__ == '__main__':
    workDir= '.\\Stub\\'
    materialDir= '.\\Material\\'
    sectionStub=['stub', 'materialStub', 'musicXMLtoLabelStub', 'neutrinoStub', 'worldStub']
    # CreateStub(workDir)
    

    beats = 4 
    beat_type = 4 
    speed = 100

    voiceType= ['ITAKO', 'JSUT', 'KIRITAN', 'YOKO']
    # fill with the file that record the music we have
    # diy不管，从左到右（索引顺序）：歳月-雲流れ（1）、穿越时空的思念（2）、千与千寻（3）、送别（4）
    pitchType= ['diyPitch', 'liuyunPitch', 'cyPitch', 'qyqxPitch', 'sbPitch']
    octaveType= ['diyOctave', 'liuyunOctave', 'cyOctave', 'qyqxOctave', 'sbOctave']
    durationType= ['diyDuration', 'liuyunDuration', 'cyDuration', 'qyqxDuration', 'sbDuration']
    durSum=[8, 4, 4, 16, 4]
    divisionsType=[2, 1, 1, 2, 1]
    numVoice= len(voiceType)
    numMusic= len(pitchType)

    # file type, record information used for construct xml
    fInputLyric= materialDir+'inputLyric'# TODO
    fInputMusic= materialDir+'inputMusic'# TODO
    fLyric= materialDir+'lyric'
    # python test.py <inputfile> <outputfile>
    os.system("python scrapy.py {} {}".format(fInputLyric, fLyric))
    # Select with music to play
    chosenMusic= SelectMusic(fInputMusic)
    fPitch= materialDir+pitchType[chosenMusic]
    fOctave= materialDir+octaveType[chosenMusic]
    fDuration= materialDir+durationType[chosenMusic]

    # output xml here
    fDemoXml= '.\\score\\musicxml\\demo.musicxml'
    fDemoXmlForRunB = 'demo.musicxml'

    # store the contents in the file
    texts=[]
    steps=[]
    octaves=[]
    durations=[]

    # file type, record information used for construct batch
    fInputVoice= materialDir+'inputVoice'
    voice= voiceType[SelectVoice(fInputVoice)]
    # output batch here
    fRunBat='Run.bat'

    # store the elements for batch
    basename, suffix= fDemoXmlForRunB.split('.')

    # material for construct xml
    xmlFrameHead= '''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="3.1">
    <identification>
        <encoding>
            <software>MuseScore 3.3.2</software>
            <encoding-date>2020-02-12</encoding-date>
            <supports element="accidental" type="yes"/>
            <supports element="beam" type="yes"/>
            <supports element="print" attribute="new-page" type="yes" value="yes"/>
            <supports element="print" attribute="new-system" type="yes" value="yes"/>
            <supports element="stem" type="yes"/>
        </encoding>
    </identification>
    <defaults>
        <scaling>
            <millimeters>7.05556</millimeters>
            <tenths>40</tenths>
        </scaling>
        <page-layout>
            <page-height>1683.78</page-height>
            <page-width>1190.55</page-width>
            <page-margins type="even">
                <left-margin>56.6929</left-margin>
                <right-margin>56.6929</right-margin>
                <top-margin>56.6929</top-margin>
                <bottom-margin>113.386</bottom-margin>
            </page-margins>
            <page-margins type="odd">
                <left-margin>56.6929</left-margin>
                <right-margin>56.6929</right-margin>
                <top-margin>56.6929</top-margin>
                <bottom-margin>113.386</bottom-margin>
            </page-margins>
        </page-layout>
        <word-font font-family="FreeSerif" font-size="10"/>
        <lyric-font font-family="FreeSerif" font-size="11"/>
    </defaults>
    <part-list>
        <score-part id="P1">
            <part-name>ピアノ, Okinakurino-Kinoshitade</part-name>
            <part-abbreviation>Pno.</part-abbreviation>
            <score-instrument id="P1-I1">
            <instrument-name>ピアノ</instrument-name>
            </score-instrument>
            <midi-device id="P1-I1" port="1"></midi-device>
            <midi-instrument id="P1-I1">
            <midi-channel>1</midi-channel>
            <midi-program>1</midi-program>
            <volume>78.7402</volume>
            <pan>0</pan>
            </midi-instrument>
        </score-part>
    </part-list>
    <part id="P1">'''

    xmlFrameRear='''
    </part>
</score-partwise>'''

    measureStart= '''
    <measure number="1" width="115.07">
        <print>
            <system-layout>
                <system-margins>
                    <left-margin>0.00</left-margin>
                    <right-margin>0.00</right-margin>
                </system-margins>
                <top-system-distance>70.00</top-system-distance>
            </system-layout>
        </print>
        <attributes>
            <divisions>%d</divisions>
            <key>
                <fifths>0</fifths>
                <mode>major</mode>
                <fifths>0</fifths>
            </key>
            <time>
                <beats>%d</beats>
                <beat-type>%d</beat-type>
            </time>
            <clef>
                <sign>G</sign>
                <line>2</line>
            </clef>
        </attributes>
    </measure>'''%(divisionsType[chosenMusic], beats,beat_type)
    breathMark='''
            <notations>
                <articulations>
                    <breath-mark/>
                </articulations>
            </notations>'''

    quarterRest='''
        <note>
            <rest/>
            <duration>{}</duration>
            <voice>1</voice>
            <type>quarter</type>
        </note>'''
    
    # material for construct Run.bat
    Run='''\
@echo off
setlocal enabledelayedexpansion
cd /d %~dp0

: Project settings
set BASENAME={}
set NumThreads=3

: musicXML_to_label.exe
set SUFFIX={}

: NEUTRINO.exe
set ModelDir={}
set StyleShift=0

: WORLD.exe
set PitchShift=1.0
set FormantShift=1.0


echo %date% %time% : start MusicXMLtoLabel
bin\\musicXMLtoLabel.exe score\\musicxml\\%BASENAME%.%SUFFIX% score\\label\\full\\%BASENAME%.lab score\\label\\mono\\%BASENAME%.lab
del {}

echo %date% %time% : start NEUTRINO
bin\\NEUTRINO.exe score\\label\\full\\%BASENAME%.lab score\\label\\timing\\%BASENAME%.lab output\\%BASENAME%.f0 output\\%BASENAME%.mgc output\\%BASENAME%.bap model\\%ModelDir%\\ -n %NumThreads% -k %StyleShift% -m -t
del {}

echo %date% %time% : start WORLD
bin\\WORLD.exe output\\%BASENAME%.f0 output\\%BASENAME%.mgc output\\%BASENAME%.bap -f %PitchShift% -m %FormantShift% -o output\\%BASENAME%_syn.wav -n %NumThreads% -t
del {}

echo %date% %time% : start NSF
bin\\NSF_IO.exe score\\label\\full\\%BASENAME%.lab score\\label\\timing\\%BASENAME%.lab output\\%BASENAME%.f0 output\\%BASENAME%.mgc output\\%BASENAME%.bap %MODELDIR% output\\%BASENAME%_nsf.wav -t

echo %date% %time% : end
'''.format(basename, suffix, voice, workDir+sectionStub[2], workDir+sectionStub[3], workDir+sectionStub[4])

    with codecs.open(fDemoXml, 'w', 'utf-8') as demoXml:
        demoXml.write(xmlFrameHead)
        demoXml.write(measureStart)
        with open(fLyric, 'r', encoding='utf-8') as lyric:
            for line in lyric.readlines():
                line= line.strip('\n')
                texts.extend(line)
        with open(fPitch, 'r') as pitch:
            for line in pitch.readlines():
                line= line.strip('\n')
                steps.extend(line)

        with open(fOctave, 'r') as octave:
            for line in octave.readlines():
                line= line.strip('\n')
                octaves.extend(line)

        with open(fDuration, 'r') as duration:
            for line in duration.readlines():
                line= line.strip('\n')
                durations.extend(line)
        
        numText= len(texts)
        biasIdx= 0
        measureGroup= SplitMeasure(durations, durSum[chosenMusic])
        for cntMeasure, notesPerMeasure in enumerate(measureGroup):
            measureHead= '''
    <measure number="{}" width="136.20">'''.format(cntMeasure+2)
            measureRear= '''
    </measure>'''
            notes=[]
            for noteIdx in notesPerMeasure:
                if steps[noteIdx].islower():
                    Breath= breathMark
                    steps[noteIdx]= steps[noteIdx].upper()
                else:
                    Breath=''

                if steps[noteIdx].isdecimal():
                    # if '4'== steps[noteIdx]:
                    note= quarterRest.format(durations[noteIdx])
                    biasIdx-= 1
                else:    
                    note='''
        <note default-x="13.62" default-y="-30.00">
            <pitch>
                <step>{}</step>
                <octave>{}</octave>
            </pitch>
            <duration>{}</duration>
            <voice>1</voice>
            <type>quarter</type>
            <stem>up</stem>{}
            <lyric number="1" default-x="6.58" default-y="-53.60" relative-y="-30.00">
                <syllabic>single</syllabic>
                <text>{}</text>
            </lyric>
        </note>'''.format(steps[noteIdx], octaves[noteIdx+biasIdx], durations[noteIdx], Breath, texts[(noteIdx+biasIdx)%numText])    
                notes.append(note)

            demoXml.write(measureHead)
            for note in notes:
                demoXml.write(note)
            demoXml.write(measureRear)
        demoXml.write(xmlFrameRear)

    with codecs.open(fRunBat, 'w', 'utf-8') as runBat:
        runBat.write(Run)

    # section one end
    RemoveStub(workDir, sectionStub[1])
    
    
    os.system(fRunBat)

    # process end
    RemoveStub(workDir, sectionStub[0])